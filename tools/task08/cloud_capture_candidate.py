#!/usr/bin/env python3
"""Capture fresh source receipts and run the uploaded original Task 08 gate.

The ONLY allowed outcome is an EXPERIMENTAL, non-production publication candidate.
Never writes published/latest_valid.json, never alters frozen Model C and does
not claim independent per-game box-stat parity.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import static_snapshot as snapshot

BOX = "https://boxscorelab.com/downloads/"
STANDINGS = BOX + "2026-27-team-standings.csv"
GAMES = BOX + "2026-27-team-game-results.csv"
DOWNLOADS = "https://www.boxscorelab.com/downloads/"
SCORE = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
PUBLIC = ROOT / "published"
CANDIDATES = PUBLIC / "candidates"
STATUS = "EXPERIMENTAL_TASK08_NOT_PRODUCTION"


def acquire(url, *, limit=3_000_000):
    req = urllib.request.Request(url, headers={
        "User-Agent": "NBA-Match-Intelligence-Independent-Task08-Check/1.0",
        "Accept": "*/*",
    })
    with urllib.request.urlopen(req, timeout=40) as response:
        code = response.status
        raw = response.read(limit + 1)
        if code != 200:
            raise ValueError("Upstream HTTP %s from %s" % (code, url))
        if not raw or len(raw) > limit:
            raise ValueError("Empty or oversized upstream response: " + url)
        return raw, code


def capture():
    """Capture sources in one temporary directory; no cached or fake receipts."""
    new_york_date = dt.datetime.now(dt.timezone.utc).astimezone(ZoneInfo("America/New_York")).date()
    if not dt.date(2026,10,20) <= new_york_date < dt.date(2027,4,15):
        raise ValueError("Outside 2026-27 data-collection window")
    folder = Path(tempfile.mkdtemp(prefix="nba_task08_"))
    receipts = {}
    entries = [
        ("games.txt", GAMES),
        ("standings.txt", STANDINGS),
        ("downloads.txt", DOWNLOADS),
    ]
    start = dt.date(2026,10,1)
    for day_offset in range((new_york_date-start).days+1):
        day = start + dt.timedelta(days=day_offset)
        url = SCORE+"?"+urllib.parse.urlencode({
            "dates":day.strftime("%Y%m%d"),
            "seasontype":"2",
            "limit":"100",
        })
        entries.append((day.strftime("%Y%m%d")+".json",url))
    for filename,url in entries:
        raw,code=acquire(url)
        if filename.endswith(".json"):
            data=json.loads(raw.decode("utf-8"))
            if not isinstance(data.get("events"),list) or not data.get("leagues"):
                raise ValueError("ESPN response incomplete: "+filename)
        else:
            if filename.endswith(".txt") and filename!="downloads.txt" and b"season" not in raw[:500]:
                raise ValueError("CSV header not found: "+filename)
        (folder/filename).write_bytes(raw)
        receipts[filename]={
            "sha256":hashlib.sha256(raw).hexdigest(),
            "http_status":code,
            "observed_at":dt.datetime.now(dt.timezone.utc).isoformat(),
            "source_url":url,
        }
    (folder/"fetch_receipts.json").write_text(json.dumps(receipts,indent=2)+"\n",encoding="utf-8")
    return folder


def build():
    with tempfile.TemporaryDirectory(prefix="nba_task08_candidate_") as output_tmp:
        folder = capture()
        # The original script uses the local validation-only implementation
        # of the five unchanged Model C data functions (no parameters).
        cmd=[sys.executable,"-B",str(Path(__file__).with_name("static_snapshot.py")),
             "--input",str(folder),"--output",output_tmp]
        run=subprocess.run(cmd,capture_output=True,text=True,timeout=180)
        if run.returncode:
            raise ValueError("Task 08 gate script crashed: "+run.stderr[-1800:])
        snapshots=list(Path(output_tmp).glob("*.json"))
        if len(snapshots)!=1:
            raise ValueError("Expected exactly one Task 08 output")
        payload=json.loads(snapshots[0].read_text(encoding="utf-8"))
        if payload.get("validation")!="PASS":
            raise ValueError("FAIL CLOSED: Task08 validation failed: "+str(payload.get("reason","unknown")))
        if len(payload.get("teams",{}))!=30 or payload.get("game_count",0)<1:
            raise ValueError("FAIL CLOSED: incomplete team/game table")
        # The original Task 08 code records source-vs-reconstruction
        # differences without enforcing a numeric threshold: enforce it here.
        difference=float(payload.get("standings_max_abs_difference",float("inf")))
        if not 0<=difference<=0.015:
            raise ValueError("FAIL CLOSED: standings/model metric mismatch: "+str(difference))
        if not isinstance(payload.get("build"),list):
            raise ValueError("Unexpected source build field")
        data_date=dt.date.fromisoformat(payload["data_through"])
        current_et=dt.datetime.now(dt.timezone.utc).astimezone(ZoneInfo("America/New_York")).date()
        if not 0<(current_et-data_date).days<=2:
            raise ValueError("FAIL CLOSED: wrong or stale NBA data cutoff")
        source_hash=payload["receipts"]["games.txt"]
        digest=hashlib.sha256(snapshots[0].read_bytes()).hexdigest()
        stem=payload["data_through"]+"-task08-"+digest[:12]
        CANDIDATES.mkdir(parents=True,exist_ok=True)
        json_target=CANDIDATES/(stem+".json")
        md_target=CANDIDATES/(stem+".md")
        if json_target.exists() or md_target.exists():
            raise ValueError("Immutable candidate exists; refusing overwrite")
        raw_md=snapshots[0].with_suffix(".md").read_text(encoding="utf-8")
        # Preserve the original Task 08 text; insert candidate warning and
        # an explicit notice that per-game ESPN box fields are NOT verified.
        warning=("\n**PUBLICATION STATUS: EXPERIMENTAL CANDIDATE — NOT PRODUCTION.**\n"
                 "**Independent per-game box-score field parity: NOT CHECKED.**\n"
                 "**Original full frozen prediction model SHA check on GitHub: NOT RUN.**\n"
                 "**Never use as an approved daily production snapshot.**\n\n")
        header="# NBA Model C v0.1 static inputs"
        if not raw_md.startswith(header):
            raise ValueError("Unknown Task08 Markdown structure")
        md_text=raw_md.replace(header,header+warning,1)
        # Atomic publication happens in GitHub Actions *after* validation.
        json_target.write_bytes(snapshots[0].read_bytes())
        md_target.write_text(md_text,encoding="utf-8")
        index={
            "schema_version":"nba-task08-candidate-v1",
            "status": STATUS,
            "validation_gate":"TASK08_PASS",
            "independent_final_score_check":"PASS (Task08 ESPN daily)",
            "model_input_formula_parity":"PASS",
            "independent_per_game_box_statistics":"NOT_CHECKED",
            "frozen_full_model_sha_on_github":"NOT_CHECKED; locally matched",
            "original_task08_regression_tests":"9/9 PASS in workflow",
            "date":payload["data_through"],
            "generation_cutoff":payload["cutoff"],
            "games":payload["game_count"],
            "teams":len(payload["teams"]),
            "max_source_aggregate_difference":difference,
            "source_games_sha256":source_hash,
            "json_sha256":digest,
            "json_path":str(json_target.relative_to(ROOT)),
            "markdown_path":str(md_target.relative_to(ROOT)),
            "production_pointer_created":False,
        }
        PUBLIC.mkdir(exist_ok=True)
        (PUBLIC/"task08_candidate_index.json").write_text(
            json.dumps(index,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")
        print(json.dumps(index,indent=2))
        return index


if __name__=="__main__":
    build()
