#!/usr/bin/env python3
"""Publish only an EXPLICITLY NON-PRODUCTION candidate of Model C daily inputs.

Requires two verified gates in SAME build:
  1. Every NBA regular-season final through yesterday ET matches ESPN score/result.
  2. Every team's BoxScore Lab standings GP/W/L/ORtg/DRtg/Pace matches
     game-by-game recomputation with frozen Model C mathematical definitions.

Not yet checked: independent ESPN boxscore *stat fields* on each game, original
Task 08 validator/tests, frozen Python SHA. NEVER create latest_valid.json here.
"""
from __future__ import annotations
import csv
import datetime as dt
import hashlib
import io
import json
from pathlib import Path
from zoneinfo import ZoneInfo

import independent_coverage_probe as cov
import model_input_parity_probe as parity

OUT = Path("published")
CANDIDATES = OUT / "candidates"


def build():
    through = dt.datetime.now(dt.timezone.utc).astimezone(ZoneInfo("America/New_York")).date() - dt.timedelta(days=1)
    raw_games = cov.get_bytes(cov.BOX)
    raw_standings = cov.get_bytes(parity.STANDINGS_URL)
    source_games, rows = cov.bsl_games(raw_games, through)
    independent, checked_days = cov.esn_games(through)
    coverage = cov.compare(source_games, independent)
    if not coverage["pass"]:
        raise ValueError("FAIL CLOSED: ESPN final-game coverage/score mismatch: %s" % coverage)

    standings_rows = list(csv.DictReader(io.StringIO(raw_standings.decode("utf-8-sig"))))
    standings = {cov.canonical(r["team"]): r for r in standings_rows}
    if len(standings_rows) != len(standings):
        raise ValueError("FAIL CLOSED: duplicated standings team")
    rates = parity.reconstruct(rows)
    differences = parity.audit(standings, rates)
    if differences:
        raise ValueError("FAIL CLOSED: Model C parity differences: %s" % differences[:10])

    actual_through = max(r["game_date"] for r in rows)
    generated = dt.datetime.now(dt.timezone.utc).isoformat()
    snapshot = {
        "schema_version": "nba-model-c-candidate-v1",
        "publication_status": "EXPERIMENTAL_CANDIDATE_NOT_PRODUCTION",
        "quality": {
            "independent_full_season_score_coverage": "PASS",
            "model_c_algebra_30_team_parity": "PASS",
            "independent_espn_box_stat_field_parity": "NOT_CHECKED",
            "original_task08_nine_tests": "NOT_EXECUTED",
            "frozen_python_sha_comparison": "NOT_EXECUTED",
            "official_daily_production_approval": "NO_GO",
        },
        "season": "2026-27",
        "data_through_nba_date": actual_through,
        "forecast_cutoff_nba_date": through.isoformat(),
        "generated_at_utc": generated,
        "source_attribution": "BoxScore Lab (CC BY 4.0), transformed by NBA Match Intelligence; independent final scores checked against ESPN",
        "source_urls": {"standings": parity.STANDINGS_URL, "team_games": cov.BOX},
        "sha256_source_standings": hashlib.sha256(raw_standings).hexdigest(),
        "sha256_source_team_games": hashlib.sha256(raw_games).hexdigest(),
        "independent_final_games": len(independent),
        "boxscorelab_final_games": len(source_games),
        "independent_days_checked": checked_days,
        "model_input_definitions": {
            "estimated_possessions_per_game": "P = avg_two_teams(FGA + 0.44*FTA - OREB + TOV)",
            "ortg": "arithmetic mean over team games of 100*team_points/P",
            "drtg": "arithmetic mean over team games of 100*opponent_points/P",
            "pace": "arithmetic mean over team games of P, overtime inclusive, not per-48 normalized",
        },
        "teams": {t: rates[t] for t in sorted(cov.TEAM_SET)},
    }
    canonical = (json.dumps(snapshot, indent=2, ensure_ascii=False, sort_keys=True, allow_nan=False) + "\n").encode()
    digest = hashlib.sha256(canonical).hexdigest()
    CANDIDATES.mkdir(parents=True, exist_ok=True)
    stem = actual_through + "." + digest[:12]
    json_name = "published/candidates/" + stem + ".json"
    md_name = "published/candidates/" + stem + ".md"
    path = Path(json_name)
    path.write_bytes(canonical)
    lines = [
        "# NBA Model C input candidate — " + actual_through,
        "",
        "**NOT PRODUCTION — Experimental data-delivery candidate only.**",
        "",
        "**Independent final-game coverage:** PASS (%d games across %d NBA dates)" % (len(independent), checked_days),
        "**Model C formula and team aggregate parity:** PASS (30/30)",
        "**Independent ESPN shooting / rebounding / turnover field parity:** NOT CHECKED",
        "**Original Task 08 regression suite:** NOT EXECUTED",
        "**Data through NBA league date:** " + actual_through,
        "**Generated UTC:** " + generated,
        "**Source:** BoxScore Lab, CC BY 4.0. Independent final-score check: ESPN.",
        "**Source SHA-256 team games:** " + snapshot["sha256_source_team_games"],
        "**Source SHA-256 standings:** " + snapshot["sha256_source_standings"],
        "**JSON SHA-256:** " + digest,
        "",
        "The statistics below use the Model C estimated possession formula, including overtime.",
        "",
        "| Team | GP | W | L | ORtg | DRtg | Pace |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for team in sorted(rates):
        r = rates[team]
        lines.append("| %s | %d | %d | %d | %.4f | %.4f | %.4f |" % (
            team,r["gp"],r["wins"],r["losses"],r["ortg"],r["drtg"],r["pace"]))
    lines += ["", "Do not treat this file as a production source. Missing final model gate: independent per-game core-stat comparison and the existing 9-test Task 08 validator.", ""]
    Path(md_name).write_text("\n".join(lines),encoding="utf-8")
    index = {
        "schema_version": "nba-candidate-index-v1",
        "status": "EXPERIMENTAL_CANDIDATE_NOT_PRODUCTION",
        "data_through_nba_date": actual_through,
        "json_path": json_name,
        "markdown_path": md_name,
        "json_sha256": digest,
        "source_team_games_sha256": snapshot["sha256_source_team_games"],
        "generated_at_utc": generated,
        "production_pointer_must_not_advance": True,
    }
    (OUT/"candidate_index.json").write_text(json.dumps(index,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(index,indent=2))
    return index


if __name__=="__main__":
    build()
