#!/usr/bin/env python3
"""NBA 2026-27 independent schedule/score coverage diagnostic.

This diagnostic NEVER publishes Model C input. The local Task 08
static_snapshot.py validator must also pass before a production publication.
Source universe: 2026-27 NBA regular-season games, starting Oct 20 2026.
"""
from __future__ import annotations
import collections
import csv
import datetime as dt
import hashlib
import io
import json
import math
import os
from pathlib import Path
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

BOX = "https://boxscorelab.com/downloads/2026-27-team-game-results.csv"
ESPN = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
FIRST_DATE = dt.date(2026, 10, 20)
TEAM_SET = set("ATL BKN BOS CHA CHI CLE DAL DEN DET GSW HOU IND LAC LAL MEM MIA MIL MIN NOP NYK OKC ORL PHI PHX POR SAC SAS TOR UTA WAS".split())
ALIASES = {"NY":"NYK","GS":"GSW","NO":"NOP","SA":"SAS","WSH":"WAS","PHO":"PHX","BRK":"BKN","UTAH":"UTA"}
OUT = Path("independent_coverage_report.json")


def canonical(value):
    v = str(value).strip().upper()
    return ALIASES.get(v, v)


def get_bytes(url):
    req = urllib.request.Request(url, headers={"User-Agent": "NBA-Match-Intelligence-ReadOnly-Audit/1.0", "Accept": "text/csv,application/json"})
    with urllib.request.urlopen(req, timeout=40) as res:
        if res.status != 200:
            raise ValueError("HTTP %s from %s" % (res.status, url))
        return res.read()


def integer(v):
    x = float(v)
    if not math.isfinite(x) or x != int(x):
        raise ValueError("Invalid integer value: %r" % v)
    return int(x)


def bsl_games(raw, through):
    text = raw.decode("utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise ValueError("Empty BoxScore Lab team-game CSV")
    grouped = collections.defaultdict(list)
    for r in rows:
        date = dt.date.fromisoformat(r["game_date"])
        team, opp = canonical(r["team"]), canonical(r["opponent"])
        if date < FIRST_DATE or date > through:
            raise ValueError("Unexpected BoxScore Lab date %s outside complete cutoff" % date)
        if team not in TEAM_SET or opp not in TEAM_SET or team == opp:
            raise ValueError("Unrecognized team matchup: %s vs %s" % (team, opp))
        grouped[(date.isoformat(), tuple(sorted((team, opp))))].append(r)
    checked = {}
    for key, pair in grouped.items():
        if len(pair) != 2:
            raise ValueError("Missing/duplicate team-game half: %s, count %d" % (key, len(pair)))
        a, b = pair
        if canonical(a["opponent"]) != canonical(b["team"]) or canonical(b["opponent"]) != canonical(a["team"]):
            raise ValueError("Opponent rows are not reciprocal: %s" % (key,))
        ap, bp = integer(a["points"]), integer(b["points"])
        if ap == bp or ap != integer(b["opponent_points"]) or bp != integer(a["opponent_points"]):
            raise ValueError("Non-final/conflicting scores: %s" % (key,))
        for r in pair:
            pts = integer(r["points"])
            if pts != 2 * integer(r["field_goals_made"]) + integer(r["three_point_makes"]) + integer(r["free_throws_made"]):
                raise ValueError("Shooting arithmetic differs from final score: %s" % (key,))
            for make, attempt in [
                ("field_goals_made","field_goal_attempts"),
                ("three_point_makes","three_point_attempts"),
                ("free_throws_made","free_throw_attempts"),
            ]:
                if integer(r[make]) > integer(r[attempt]):
                    raise ValueError("Makes exceed attempts: %s" % (key,))
            if integer(r["field_goal_attempts"]) < 1 or integer(r["turnovers"]) < 0 or integer(r["offensive_rebounds"]) < 0:
                raise ValueError("Implausible box count: %s" % (key,))
        checked[key] = {canonical(a["team"]): ap, canonical(b["team"]): bp}
    return checked, rows


def parse_espn_events(payload, requested_date):
    events = {}
    for event in payload.get("events", []):
        season = event.get("season") or {}
        if int(season.get("type", -1)) != 2:
            continue
        competition = (event.get("competitions") or [None])[0]
        if not competition:
            raise ValueError("ESPN event without competition on %s" % requested_date)
        notes = " ".join(str(n.get("headline", "")) for n in competition.get("notes", []) if isinstance(n, dict))
        if "championship" in notes.lower() and "cup" in notes.lower():
            continue
        comps = competition.get("competitors", [])
        if len(comps) != 2:
            raise ValueError("ESPN event not a two-team game on %s" % requested_date)
        teams = [canonical(x["team"]["abbreviation"]) for x in comps]
        if any(t not in TEAM_SET for t in teams):
            continue
        match_date = dt.datetime.fromisoformat(event["date"].replace("Z", "+00:00")).astimezone(
            ZoneInfo("America/New_York")).date()
        if match_date != requested_date:
            # ESPN sometimes places the event under an adjacent-date feed.
            # Verify it in the authoritative ET date feed rather than counting twice.
            continue
        st = (event.get("status") or {}).get("type") or {}
        if st.get("completed") is not True:
            label = (st.get("description") or st.get("name") or "").lower()
            if "postponed" in label or "cancelled" in label or "canceled" in label:
                continue
            raise ValueError("Scheduled NBA event not completed: %s %s %s" % (requested_date, teams, label))
        score = {canonical(x["team"]["abbreviation"]): integer(x["score"]) for x in comps}
        if len(score) != 2 or len(set(score.values())) != 2:
            raise ValueError("ESPN invalid scores for %s" % teams)
        key = (requested_date.isoformat(), tuple(sorted(teams)))
        if key in events:
            raise ValueError("Duplicated ESPN event for %s" % (key,))
        events[key] = score
    return events


def esn_games(through):
    events = {}
    day = FIRST_DATE
    dates_checked = 0
    while day <= through:
        params = urllib.parse.urlencode({"dates": day.strftime("%Y%m%d"), "seasontype": "2", "limit": "100"})
        data = json.loads(get_bytes(ESPN + "?" + params).decode("utf-8"))
        result = parse_espn_events(data, day)
        for k, v in result.items():
            if k in events:
                raise ValueError("Duplicate ESPN event key %s" % (k,))
            events[k] = v
        dates_checked += 1
        day += dt.timedelta(days=1)
    return events, dates_checked


def compare(bsl, espn):
    a, b = set(bsl), set(espn)
    mismatches = [
        {"date": k[0], "teams": list(k[1]), "bsl": bsl[k], "espn": espn[k]}
        for k in sorted(a & b) if bsl[k] != espn[k]
    ]
    return {
        "bsl_games": len(bsl), "espn_completed_games": len(espn),
        "missing_from_bsl": [{"date": k[0], "teams": list(k[1])} for k in sorted(b - a)],
        "extra_in_bsl": [{"date": k[0], "teams": list(k[1])} for k in sorted(a - b)],
        "score_conflicts": mismatches,
        "pass": bool(bsl and espn and a == b and not mismatches),
    }


def main():
    now = dt.datetime.now(dt.timezone.utc)
    through_env = os.environ.get("NBA_THROUGH_DATE", "").strip()
    through = dt.date.fromisoformat(through_env) if through_env else (
        now.astimezone(ZoneInfo("America/New_York")).date() - dt.timedelta(days=1))
    report = {
        "status": "FAIL", "scope": "INDEPENDENT SCORE AND GAME COVERAGE ONLY — NOT PRODUCTION MODEL INPUT",
        "checked_at_utc": now.isoformat(), "through_date_et": through.isoformat(),
        "boxscorelab_source": BOX, "independent_source": ESPN,
        "model_input_definition_parity": "NOT_CHECKED",
        "task08_validator": "NOT_EXECUTED",
    }
    try:
        if through < FIRST_DATE or through >= dt.date(2027, 4, 12):
            raise ValueError("Selected NBA date outside supported 2026-27 regular season")
        raw = get_bytes(BOX)
        bsl, rows = bsl_games(raw, through)
        espn, checked_days = esn_games(through)
        comparison = compare(bsl, espn)
        report.update(
            status="SCORE_COVERAGE_PASS" if comparison["pass"] else "FAIL",
            boxscorelab_sha256=hashlib.sha256(raw).hexdigest(),
            bsl_team_game_rows=len(rows), espn_days_checked=checked_days,
            comparison=comparison,
        )
    except Exception as exc:
        report.update(status="FAIL", error="%s: %s" % (type(exc).__name__, exc))
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["status"] == "SCORE_COVERAGE_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
