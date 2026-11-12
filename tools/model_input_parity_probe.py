#!/usr/bin/env python3
"""Reconstruct 2026-27 Model C team inputs from complete BoxScore Lab games.

Algebra mirrors frozen nba_baseline_v01.py:
P = mean(FGA + .44 FTA - OREB + TOV for the two game teams).
ORtg/DRtg = arithmetic mean of per-game 100*points/P, 100*opp/P.
Pace = arithmetic mean of P, incl OT, NOT normalized per-48.

Diagnostic only. Independent scoreboard score coverage is a separate gate.
Never publish from this module.
"""
from __future__ import annotations
from collections import defaultdict
import csv
import datetime as dt
import hashlib
import io
import json
import math
from pathlib import Path
import independent_coverage_probe as base

STANDINGS_URL = "https://boxscorelab.com/downloads/2026-27-team-standings.csv"
OUTPUT = Path("model_input_parity_report.json")
FIELDS = ("field_goal_attempts","free_throw_attempts","offensive_rebounds","turnovers")


def num(row, col):
    v = float(row[col])
    if not math.isfinite(v) or v < 0:
        raise ValueError("Non-finite/negative %s for %s" % (col, row.get("team")))
    return v


def reconstruct(games):
    groups = defaultdict(list)
    for row in games:
        teams = tuple(sorted((base.canonical(row["team"]), base.canonical(row["opponent"]))))
        groups[(row["game_date"], teams)].append(row)
    grouped = defaultdict(list)
    for key, pairs in groups.items():
        if len(pairs) != 2:
            raise ValueError("Expected reciprocal rows for %s" % (key,))
        def poss(r):
            return num(r,"field_goal_attempts") + 0.44*num(r,"free_throw_attempts") - num(r,"offensive_rebounds") + num(r,"turnovers")
        p = (poss(pairs[0]) + poss(pairs[1])) / 2.0
        if not 50.0 < p < 200.0:
            raise ValueError("Invalid possession estimate %f %s" % (p,key))
        for r in pairs:
            team = base.canonical(r["team"])
            points = num(r,"points"); allowed = num(r,"opponent_points")
            grouped[team].append((100*points/p, 100*allowed/p, p, int(points > allowed)))
    ret = {}
    for team, vals in grouped.items():
        n = len(vals)
        ret[team] = {
            "gp":n,
            "wins":sum(v[3] for v in vals),
            "losses":n-sum(v[3] for v in vals),
            "ortg":sum(v[0] for v in vals)/n,
            "drtg":sum(v[1] for v in vals)/n,
            "pace":sum(v[2] for v in vals)/n,
        }
    return ret


def audit(st, actual):
    if len(st) != 30 or set(st) != base.TEAM_SET:
        raise ValueError("Not exactly 30 unique canonical standings teams")
    if set(actual) != set(st):
        raise ValueError("Game-derived teams and standings teams differ")
    mismatches = []
    for team in sorted(base.TEAM_SET):
        row = st[team]
        x = actual[team]
        for field, source_field in (("gp","games"),("wins","wins"),("losses","losses")):
            if x[field] != base.integer(row[source_field]):
                mismatches.append("%s %s derived=%s source=%s" % (team,field,x[field],row[source_field]))
        for field, source_field, tolerance in (
            ("ortg","off_rating_est",0.001),
            ("drtg","def_rating_est",0.001),
            ("pace","pace",0.015),
        ):
            if abs(x[field] - float(row[source_field])) > tolerance:
                mismatches.append("%s %s derived=%.6f source=%s" % (team,field,x[field],row[source_field]))
    return mismatches


def main():
    report={"status":"FAIL","scope":"MODEL C ALGEBRA / STANDINGS PARITY ONLY; NOT INDEPENDENT BOX STAT VERIFICATION",
            "asof_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
            "model_rules":"per-game arithmetic mean efficiency, OT-inclusive possessions per game",
            "independent_box_field_comparison":"NOT_CHECKED",
            "first_party_model_sha":"NOT_CHECKED",
            "publication":"NONE"}
    try:
        raw_games=base.get_bytes(base.BOX)
        raw_st=base.get_bytes(STANDINGS_URL)
        rows=list(csv.DictReader(io.StringIO(raw_games.decode("utf-8-sig"))))
        st_rows=list(csv.DictReader(io.StringIO(raw_st.decode("utf-8-sig"))))
        if len(st_rows)!=30:
            raise ValueError("Expected 30 standings, got %d" % len(st_rows))
        st={base.canonical(x["team"]):x for x in st_rows}
        if len(st)!=30:
            raise ValueError("Standings contains duplicates")
        # Revalidate reciprocal score and shooting invariants before arithmetic.
        cutoff=dt.datetime.now(dt.timezone.utc).astimezone(
            __import__("zoneinfo").ZoneInfo("America/New_York")).date()-dt.timedelta(days=1)
        _, valid_rows=base.bsl_games(raw_games,cutoff)
        rates=reconstruct(valid_rows)
        mismatches=audit(st,rates)
        report.update(
            status="METRIC_FORMULA_PASS" if not mismatches else "FAIL",
            source_standings_sha256=hashlib.sha256(raw_st).hexdigest(),
            source_games_sha256=hashlib.sha256(raw_games).hexdigest(),
            teams=len(rates),gp_sum=sum(x["gp"] for x in rates.values()),
            games=len(valid_rows)//2,
            through_date=max(x["game_date"] for x in valid_rows),
            mismatch_count=len(mismatches),mismatches=mismatches[:25],
            sample_boston=rates.get("BOS"),
        )
    except Exception as exc:
        report.update(status="FAIL", error="%s: %s" % (type(exc).__name__,exc))
    OUTPUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))
    return 0 if report["status"]=="METRIC_FORMULA_PASS" else 1


if __name__=="__main__":
    raise SystemExit(main())
