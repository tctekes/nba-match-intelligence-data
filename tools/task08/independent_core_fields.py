#!/usr/bin/env python3
"""Audit every NBA 2026-27 BoxScore Lab game against ESPN's independent team box.

This does NOT alter or publish model inputs. For exact Model C historical
exclusion-policy consistency, all eight core stat fields must agree per game.
Reports failure on missing ESPN fields, incomplete boxscore, conflicting stats,
missing games or source download errors. No silent data substitution.
"""
from __future__ import annotations

import collections
import csv
import datetime as dt
import hashlib
import io
import json
import os
import re
import sys
import time
import urllib.parse
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import independent_coverage_probe as shared

SOURCE = "https://boxscorelab.com/downloads/2026-27-team-game-results.csv"
ESPN_SCOREBOARD = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
ESPN_SUMMARY = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary"
OUTPUT = Path("independent_box_fields_report.json")
PAIRS = [
    ("fieldGoalsMade-fieldGoalsAttempted", "field_goals_made", "field_goal_attempts"),
    ("threePointFieldGoalsMade-threePointFieldGoalsAttempted", "three_point_makes", "three_point_attempts"),
    ("freeThrowsMade-freeThrowsAttempted", "free_throws_made", "free_throw_attempts"),
]
SINGLES = [
    ("offensiveRebounds", "offensive_rebounds"),
    ("totalTurnovers", "turnovers"),
]
EXPECTED_CORE = ["field_goals_made","field_goal_attempts","three_point_makes","three_point_attempts",
                 "free_throws_made","free_throw_attempts","offensive_rebounds","turnovers"]


def espn_team_fields(record):
    stat_list = record.get("statistics")
    if not isinstance(stat_list, list):
        raise ValueError("ESPN team statistics missing")
    stats = {}
    for item in stat_list:
        name = item.get("name")
        if name in stats:
            raise ValueError("ESPN duplicated stat key " + str(name))
        stats[name] = item.get("displayValue")
    result = {}
    for espn_name, made, attempted in PAIRS:
        x = str(stats.get(espn_name, ""))
        if not re.fullmatch(r"\d+-\d+",x):
            raise ValueError("ESPN missing/invalid " + espn_name + ": " + x)
        ma, at = map(int,x.split("-"))
        if ma > at:
            raise ValueError("ESPN makes exceed attempts: "+espn_name)
        result[made], result[attempted] = ma, at
    for espn_name, target in SINGLES:
        raw = stats.get(espn_name)
        if raw is None or not re.fullmatch(r"\d+",str(raw)):
            raise ValueError("ESPN missing/invalid "+espn_name+": "+str(raw))
        result[target] = int(raw)
    if sorted(result) != sorted(EXPECTED_CORE):
        raise ValueError("Unexpected ESPN core stat schema")
    return result


def compare_team(source_row, independent):
    mismatches = {}
    for field in EXPECTED_CORE:
        observed = shared.integer(source_row[field])
        if observed != independent[field]:
            mismatches[field] = {"bsl":observed,"espn":independent[field]}
    return mismatches


def event_index(through):
    result = {}
    day = dt.date(2026,10,20)
    while day <= through:
        params=urllib.parse.urlencode({"dates":day.strftime("%Y%m%d"),"seasontype":"2","limit":"100"})
        payload=json.loads(shared.get_bytes(ESPN_SCOREBOARD+"?"+params).decode("utf-8"))
        for e in payload.get("events",[]):
            if int(e.get("season",{}).get("type",-1)) != 2: continue
            comp=(e.get("competitions") or [None])[0]
            if comp is None: raise ValueError("ESPN event missing competition")
            if any("championship" in str(n.get("headline","")).lower() for n in comp.get("notes",[])):continue
            teams=[shared.canonical(c["team"]["abbreviation"]) for c in comp.get("competitors",[])]
            if len(teams)!=2 or not all(t in shared.TEAM_SET for t in teams): continue
            event_day=dt.datetime.fromisoformat(e["date"].replace("Z","+00:00")).astimezone(
                ZoneInfo("America/New_York")).date()
            if event_day != day: continue
            status=e.get("status",{}).get("type",{})
            if not status.get("completed",False):continue
            key=(day.isoformat(),tuple(sorted(teams)))
            if key in result:raise ValueError("ESPN duplicated event "+str(key))
            result[key]=str(e["id"])
        day+=dt.timedelta(days=1)
    return result


def main():
    utc=dt.datetime.now(dt.timezone.utc)
    through=utc.astimezone(ZoneInfo("America/New_York")).date()-dt.timedelta(days=1)
    report={
      "checked_at_utc":utc.isoformat(), "through_et":through.isoformat(),
      "scope":"INDEPENDENT EIGHT CORE BOX-SCORE STAT FIELDS; NO MODEL DATA PUBLICATION",
      "status":"FAIL", "source":SOURCE, "espn_summary_endpoint":ESPN_SUMMARY,
      "game_count":0, "team_rows_checked":0, "field_values_compared":0,
      "game_conflicts":0,"field_conflicts":0,"missing_box_scores":0,
      "disagreement_examples":[],"errors":[],
    }
    try:
        raw=shared.get_bytes(SOURCE)
        source,rows=shared.bsl_games(raw,through)
        esn=event_index(through)
        if set(source)!=set(esn):
            raise ValueError("ESPN completed-game universe mismatch; BSL-only=%d ESPN-only=%d" % (
               len(set(source)-set(esn)),len(set(esn)-set(source))))
        by_game=collections.defaultdict(dict)
        for r in rows:
            key=(r["game_date"],tuple(sorted((shared.canonical(r["team"]),shared.canonical(r["opponent"])))))
            by_game[key][shared.canonical(r["team"])] = r
        issues = []
        counts = collections.Counter()
        for k,event_id in sorted(esn.items()):
            url=ESPN_SUMMARY+"?event="+urllib.parse.quote(event_id)
            summary=json.loads(shared.get_bytes(url).decode("utf-8"))
            records=(summary.get("boxscore") or {}).get("teams") or []
            if len(records)!=2:
                issues.append({"date":k[0],"teams":k[1],"event_id":event_id,
                              "error":"ESPN missing 2 team boxscore rows"})
                counts["missing_box"]+=1
                continue
            checked=set()
            for record in records:
                t=shared.canonical((record.get("team") or {}).get("abbreviation"))
                if t not in by_game[k] or t in checked:
                    issues.append({"date":k[0],"teams":k[1],"error":"Incorrect/missing ESPN team identity"})
                    counts["missing_box"]+=1
                    continue
                checked.add(t)
                try:
                    expected=espn_team_fields(record)
                    mismatches=compare_team(by_game[k][t],expected)
                    counts["team_rows"]+=1
                    counts["field_values"]+=len(EXPECTED_CORE)
                    if mismatches:
                        issues.append({"date":k[0],"team":t,"event_id":event_id,"stat_conflicts":mismatches})
                        counts["field_conflicts"]+=len(mismatches)
                except (ValueError,KeyError) as exc:
                    issues.append({"date":k[0],"team":t,"event_id":event_id,"error":str(exc)})
                    counts["missing_box"]+=1
            # Small delay limits strain on ESPN's public endpoints.
            time.sleep(0.08)
        conflict_games=set()
        for issue in issues:
            if issue.get("stat_conflicts"): conflict_games.add((issue["date"],issue["event_id"]))
        report.update(
           game_count=len(source),team_rows_checked=counts["team_rows"],
           field_values_compared=counts["field_values"],game_conflicts=len(conflict_games),
           field_conflicts=counts["field_conflicts"],missing_box_scores=counts["missing_box"],
           bsl_sha256=hashlib.sha256(raw).hexdigest(),
           disagreement_examples=issues[:30],
           status="CORE_STAT_PARITY_PASS" if not issues and counts["team_rows"]==2*len(source) else "FAIL",
        )
    except Exception as exc:
        report["errors"].append("%s: %s" % (type(exc).__name__,exc))
    finally:
        OUTPUT.write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8")
        print(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False))
    return 0 if report["status"]=="CORE_STAT_PARITY_PASS" else 1

if __name__=="__main__":
    raise SystemExit(main())
