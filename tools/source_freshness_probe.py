#!/usr/bin/env python3
"""Diagnostic only: inspect public 2026-27 BoxScore Lab CSV freshness.

This script never publishes model inputs or predictions. A row-count pass
is NOT the full NBA Match Intelligence production validation gate.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://boxscorelab.com/downloads/"
FILES = {
    "standings": "2026-27-team-standings.csv",
    "team_games": "2026-27-team-game-results.csv",
}
EXPECTED_COMPLETED_GAMES_THROUGH_NOV_11 = 170
EXPECTED_TEAM_GAME_ROWS = 2 * EXPECTED_COMPLETED_GAMES_THROUGH_NOV_11
OUTPUT = Path("source_preflight_report.json")


def download(name: str) -> bytes:
    request = urllib.request.Request(
        BASE + name,
        headers={"User-Agent": "NBA-Match-Intelligence-Source-Preflight/1.0"},
    )
    with urllib.request.urlopen(request, timeout=35) as response:
        data = response.read()
        if response.status != 200:
            raise RuntimeError(f"{name} returned HTTP {response.status}")
        return data


def load_csv(raw: bytes):
    text = raw.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise ValueError("CSV has no header")
    return list(reader), reader.fieldnames


def main():
    report = {
        "probe_type": "DIAGNOSTIC_ONLY_NOT_MODEL_VALIDATION",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": BASE,
        "expected_games_completed_through_nov_11": EXPECTED_COMPLETED_GAMES_THROUGH_NOV_11,
        "rows_needed_for_170_games": EXPECTED_TEAM_GAME_ROWS,
        "files": {},
        "candidate_coverage": "UNVERIFIED",
        "limitations": [
            "Row counts alone do not establish complete NBA results.",
            "Team-game pairing, game dates, exact scores, and Model C metric parity still require the existing local snapshot validator.",
            "A fresh download-page build number does not establish an up-to-date team-game CSV.",
            "This workflow does not publish production data.",
        ],
    }
    try:
        parsed = {}
        for key, filename in FILES.items():
            raw = download(filename)
            rows, headers = load_csv(raw)
            parsed[key] = rows
            report["files"][key] = {
                "filename": filename,
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "rows": len(rows),
                "columns": headers,
                "first_row_sample": dict(list(rows[0].items())[:7]) if rows else {},
            }

        standings = parsed["standings"]
        games = parsed["team_games"]
        if len(standings) != 30:
            report["candidate_coverage"] = "FAIL"
            report["reason"] = f"Expected 30 standings rows, got {len(standings)}."
        elif len(games) != EXPECTED_TEAM_GAME_ROWS:
            report["candidate_coverage"] = "FAIL"
            report["reason"] = (
                f"Expected {EXPECTED_TEAM_GAME_ROWS} team-game rows for "
                f"170 completed NBA games through Nov 11; got {len(games)}."
            )
        else:
            report["candidate_coverage"] = "ROW_COUNT_CANDIDATE_ONLY"
            report["reason"] = (
                "170 games have the expected aggregate row count, but "
                "the independent game-level validation gate has NOT run."
            )
        # Metadata only, never substitute these heuristics for a full gate.
        report["observed_game_rows_divided_by_two"] = len(games) / 2
        bos = [
            row for row in standings
            if any("boston" in str(v).lower() or str(v).strip().upper() == "BOS"
                   for v in row.values())
        ]
        report["boston_row_for_manual_cross_check"] = bos[:1]
    except Exception as exc:
        report["candidate_coverage"] = "FAIL"
        report["reason"] = f"{type(exc).__name__}: {exc}"
    finally:
        OUTPUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, ensure_ascii=False))

    return 0 if report["candidate_coverage"] == "ROW_COUNT_CANDIDATE_ONLY" else 1


if __name__ == "__main__":
    sys.exit(main())
