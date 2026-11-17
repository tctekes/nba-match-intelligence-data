#!/usr/bin/env python3
"""EXPERIMENTAL READ-ONLY probe: BSL lag -> official NBA + independent ESPN parity.

DO NOT publish candidates, modify existing inputs, or call frozen Model C.
For each ESPN-completed NBA-local game absent from the BoxScore Lab team-game CSV,
compare the official NBA live box with ESPN's independent 8 core box statistics.
Both providers must match score, identities, date, and all core fields.
No backup game is accepted or published by this probe. Fail closed.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import nba_baseline_v01 as model
import independent_core_fields as espn_fields

ESPN_SCOREBOARD = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
ESPN_SUMMARY = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary"
BSL_GAMES = "https://boxscorelab.com/downloads/2026-27-team-game-results.csv"
NBA_SCHEDULE = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json"
NBA_BOX = "https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{game_id}.json"
ET = ZoneInfo("America/New_York")
NBA_TO_CORE = {
    "fieldGoalsMade": "field_goals_made",
    "fieldGoalsAttempted": "field_goal_attempts",
    "threePointersMade": "three_point_makes",
    "threePointersAttempted": "three_point_attempts",
    "freeThrowsMade": "free_throws_made",
    "freeThrowsAttempted": "free_throw_attempts",
    "reboundsOffensive": "offensive_rebounds",
    "turnovers": "turnovers",
}

def api_bytes(url):
    return espn_fields.shared.get_bytes(url)

def api_json(url):
    raw = api_bytes(url)
    return json.loads(raw.decode("utf-8")), hashlib.sha256(raw).hexdigest()

def nba_day(utc_string):
    return dt.datetime.fromisoformat(utc_string.replace("Z","+00:00")).astimezone(ET).date().isoformat()

def pair_key(day, teams):
    names = tuple(sorted(model.norm(str(t)) for t in teams))
    if len(names)!=2 or names[0]==names[1] or any(t not in model.TEAMS for t in names):
        raise ValueError("Noncanonical or duplicated NBA teams " + str(teams))
    return (day,names)

def scheduled_nba_games(payload, day):
    schedule = payload.get("leagueSchedule") or {}
    dates = schedule.get("gameDates")
    if not isinstance(dates,list):
        raise ValueError("Official NBA schedule gameDates missing")
    result = {}
    for date in dates:
        for g in date.get("games",[]):
            if str(g.get("gameId","")).startswith("002") is False: continue
            utc = g.get("gameDateTimeUTC")
            if not utc or nba_day(utc)!=day: continue
            home,away=g.get("homeTeam") or {},g.get("awayTeam") or {}
            key=pair_key(day,[home.get("teamTricode"),away.get("teamTricode")])
            if key in result: raise ValueError("Duplicate official scheduled matchup " + str(key))
            game_id=str(g["gameId"])
            if len(game_id)!=10 or not game_id.isdigit(): raise ValueError("Invalid NBA ID")
            result[key]=game_id
    if not result:raise ValueError("No official NBA schedule games for "+day)
    return result

def espn_finals(board,day):
    out={}
    for e in board.get("events",[]):
        if (e.get("season") or {}).get("type")!=2:continue
        if nba_day(e["date"])!=day:continue
        comp=(e.get("competitions") or [None])[0]
        if not comp:raise ValueError("ESPN missing competition")
        if any("championship" in str(n.get("headline","")).lower() for n in comp.get("notes",[])):continue
        c=comp["competitors"]
        key=pair_key(day,[x["team"]["abbreviation"] for x in c])
        if not (e.get("status") or {}).get("type",{}).get("completed"):
            raise ValueError("Unfinished ESPN game "+str(key))
        if key in out:raise ValueError("Duplicate ESPN game "+str(key))
        score={model.norm(x["team"]["abbreviation"]):int(x["score"]) for x in c}
        out[key]={"espn_id":str(e["id"]),"scores":score}
    if not out:raise ValueError("No completed ESPN regular season games for "+day)
    return out

def nba_box_fields(team):
    stats=team.get("statistics")
    if not isinstance(stats,dict):raise ValueError("Official NBA team statistics missing")
    parsed={}
    for source,target in NBA_TO_CORE.items():
        raw=stats.get(source)
        if type(raw) is not int or not 0<=raw<=250:
            raise ValueError("Official NBA invalid "+source+" "+str(raw))
        parsed[target]=raw
    return parsed

def validated_pair(nba_box,espn_summary,expected,game_id,day):
    live=nba_box.get("game") or {}
    if str(live.get("gameId"))!=game_id or live.get("gameStatus")!=3:
        raise ValueError("NBA game not final or ID mismatch: "+game_id)
    if nba_day(live["gameTimeUTC"])!=day:
        raise ValueError("NBA box date mismatch "+game_id)
    official={}
    for loc in ("homeTeam","awayTeam"):
        team=live.get(loc) or {}
        t=model.norm(team.get("teamTricode",""))
        if t in official:raise ValueError("NBA duplicate team")
        official[t]={"core":nba_box_fields(team),"points":team.get("score")}
    if set(official)!=set(expected["scores"]):
        raise ValueError("Official NBA team identity mismatch: "+game_id)
    independent={}
    for entry in (espn_summary.get("boxscore") or {}).get("teams") or []:
        t=model.norm(((entry.get("team") or {}).get("abbreviation")) or "")
        if t in independent:raise ValueError("ESPN duplicate team")
        independent[t]=espn_fields.espn_team_fields(entry)
    if set(independent)!=set(official):
        raise ValueError("ESPN summary identity mismatch: "+game_id)
    result=[]
    for team in sorted(official):
        score=official[team]["points"]
        if type(score) is not int or score!=expected["scores"][team]:
            raise ValueError("Official NBA score mismatch "+team+" "+game_id)
        a,b=official[team]["core"],independent[team]
        if a!=b:
            raise ValueError("Independent 8-field mismatch "+team+" "+game_id+" "+str({k:(a[k],b[k]) for k in a if a[k]!=b[k]}))
        other=next(t for t in official if t!=team)
        vals={x:str(v) for x,v in a.items()}
        vals.update(season="2026-27",game_date=day,team=team,opponent=other,
                    points=str(score),opponent_points=str(official[other]["points"]))
        result.append(vals)
    model.validate_pair(result)
    return result

def probe(day):
    today=dt.datetime.now(dt.timezone.utc).astimezone(ET).date()
    requested=dt.date.fromisoformat(day)
    if not dt.date(2026,10,20)<=requested<today:
        raise ValueError("Only fully closed 2026-27 NBA dates eligible")
    raw=api_bytes(BSL_GAMES)
    games=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    if not games:raise ValueError("Empty BSL CSV")
    bsl=set()
    for r in games:
        k=pair_key(r["game_date"],[r["team"],r["opponent"]])
        bsl.add(k)
    board,board_sha=api_json(ESPN_SCOREBOARD+"?dates="+requested.strftime("%Y%m%d")+"&seasontype=2&limit=100")
    finals=espn_finals(board,day)
    schedule,schedule_sha=api_json(NBA_SCHEDULE)
    nba=scheduled_nba_games(schedule,day)
    if set(finals)!=set(nba):
        raise ValueError("Official schedule vs ESPN finished slate discrepancy "+
                         str({"only_espn":sorted(set(finals)-set(nba)),
                              "only_nba":sorted(set(nba)-set(finals))}))
    missing=sorted(set(finals)-bsl)
    audited=[]
    for k in missing:
        official_id=nba[k];espn_id=finals[k]["espn_id"]
        box,box_sha=api_json(NBA_BOX.format(game_id=official_id))
        summary,espn_sha=api_json(ESPN_SUMMARY+"?event="+espn_id)
        rows=validated_pair(box,summary,finals[k],official_id,day)
        audited.append({"date":day,"teams":list(k[1]),"nba_id":official_id,
                        "espn_id":espn_id,"independent_fields_verified":16,
                        "official_nba_box_sha256":box_sha,
                        "espn_summary_sha256":espn_sha,
                        "scores":finals[k]["scores"],
                        "estimated_possessions":(sum(
                            int(r["field_goal_attempts"])+0.44*int(r["free_throw_attempts"])
                            -int(r["offensive_rebounds"])+int(r["turnovers"])
                            for r in rows)/2)})
    return {"status":"DUAL_SOURCE_PROBE_PASS_NO_PUBLICATION",
            "day":day,"source_bsl_sha256":hashlib.sha256(raw).hexdigest(),
            "espn_board_sha256":board_sha,"nba_schedule_sha256":schedule_sha,
            "completed_games":len(finals),"already_in_bsl":len(set(finals)&bsl),
            "missing_bsl":len(missing),"dual_source_verified":len(audited),
            "candidate_backfill_receipts":audited,
            "scope":"DIAGNOSTIC_ONLY. No files published. No Model C inference."}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--day",default="2026-11-16")
    args=parser.parse_args()
    try:
        result=probe(args.day)
        print(json.dumps(result,indent=2,sort_keys=True))
    except Exception as ex:
        print(json.dumps({"status":"FAIL_CLOSED","type":type(ex).__name__,"error":str(ex),
                          "scope":"DIAGNOSTIC_ONLY_NO_PUBLICATION"},indent=2))
        return 1
    return 0

if __name__=="__main__":
    raise SystemExit(main())
