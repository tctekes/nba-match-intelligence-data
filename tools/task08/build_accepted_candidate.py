#!/usr/bin/env python3
"""Build a Model C input candidate excluding entire games with source conflicts.

Model C frozen historical backtest excludes entire games if ESPN and BoxScore
Lab disagree on any of eight core team box statistics. This module follows
that rule prospectively: verify all completed ESPN games, compare 8 fields
for BOTH teams, then omit disputed WHOLE games from current averages.
Never patch BoxScore Lab numbers, never include a partial game's statistics.

Deliberately non-production until the ChatGPT Project reads the candidate.
"""
from __future__ import annotations
import csv
import datetime as dt
import hashlib
import io
import json
import math
import re
import sys
import time
import urllib.parse
from collections import defaultdict
from pathlib import Path
from zoneinfo import ZoneInfo

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
import cloud_capture_candidate as capture
import independent_core_fields as independent
import static_snapshot as validation
import nba_baseline_v01 as model

ROOT_OUT=ROOT/"published"
LIMIT_EXCLUSIONS=12
LIMIT_RATIO=0.02
STATE="ACCEPTED_GAMES_EXPERIMENTAL_NOT_PRODUCTION"


def groups_of_pairs(raw_rows):
    groups=defaultdict(list)
    for r in raw_rows:
        k=(r["game_date"],tuple(sorted((r["team"],r["opponent"]))))
        groups[k].append(r)
    for k,pair in groups.items():
        model.validate_pair(pair)
    return groups


def accepted_aggregates(groups, exclusions):
    """Exact Model C update and rates; disputed games are omitted as a whole."""
    state={}
    included=0
    for k,pair in sorted(groups.items()):
        if k in exclusions:continue
        a,b=pair
        def poss(r):
            return float(r["field_goal_attempts"])+.44*float(r["free_throw_attempts"])-float(r["offensive_rebounds"])+float(r["turnovers"])
        p=(poss(a)+poss(b))/2
        if not 50<p<200:raise ValueError("Invalid pair possessions")
        game={"home":a["team"],"away":b["team"],"hp":float(a["points"]),
              "ap":float(b["points"]),"possessions":p,"minutes":48}
        model.update(state,game)
        included+=1
    if not state or set(state)!=set(model.TEAMS):
        raise ValueError("Accepted dataset lacks one or more NBA teams")
    return {t:model.rates(state[t]) for t in model.TEAMS}, included


def independent_ids(documents):
    """Map completed ESPN finals, already date/score validated by Task08."""
    lookup={}
    for day,doc in sorted(documents.items()):
        for e in doc.get("events",[]):
            if int(e.get("season",{}).get("type",-1))!=2:continue
            comp=e["competitions"][0]
            if any("championship" in n.get("headline","").lower() for n in comp.get("notes",[])):continue
            teams=tuple(sorted(model.norm(c["team"]["abbreviation"]) for c in comp["competitors"]))
            if len(teams)!=2 or any(t not in model.TEAMS for t in teams):continue
            tip=dt.datetime.fromisoformat(e["date"].replace("Z","+00:00"))
            if tip.astimezone(ZoneInfo("America/New_York")).date().isoformat()!=day:continue
            if not e["status"]["type"]["completed"]:continue
            k=(day,teams)
            if k in lookup:raise ValueError("Duplicate ESPN event key")
            lookup[k]=str(e["id"])
    return lookup


def compare_full_box_stats(groups, ids):
    if set(groups)!=set(ids):
        raise ValueError("Box stats audit missing or extra completed games")
    excluded={}
    verified_teams=0
    for k,event_id in sorted(ids.items()):
        url=independent.ESPN_SUMMARY+"?event="+urllib.parse.quote(event_id)
        summary=json.loads(independent.shared.get_bytes(url).decode("utf-8"))
        teams=(summary.get("boxscore") or {}).get("teams") or []
        if len(teams)!=2:raise ValueError("Missing independent two-team box for "+event_id)
        by_team={r["team"]:r for r in groups[k]}
        checked=set()
        discrepancies={}
        for entry in teams:
            team=model.norm((entry.get("team") or {}).get("abbreviation"))
            if team not in by_team or team in checked:
                raise ValueError("ESPN ambiguous identity for "+event_id)
            checked.add(team)
            fields=independent.espn_team_fields(entry)
            diff=independent.compare_team(by_team[team],fields)
            if diff: discrepancies[team]=diff
            verified_teams+=1
        if checked!=set(by_team):
            raise ValueError("ESPN team IDs differ on "+event_id)
        if discrepancies:
            excluded[k]={"espn_game_id":event_id,"date":k[0],
                         "teams":list(k[1]),"mismatches":discrepancies}
        time.sleep(0.06)
    if len(excluded)>LIMIT_EXCLUSIONS or len(excluded)>max(1,int(len(groups)*LIMIT_RATIO)):
        raise ValueError("Quarantine volume exceeds conservative safety cap")
    return excluded,verified_teams


def validate_receipts(folder, cutoff):
    files={p.name:p.read_bytes() for p in folder.iterdir() if p.suffix in (".txt",".json")}
    raw_receipts=json.loads(files["fetch_receipts.json"])
    for name,body in files.items():
        if name=="fetch_receipts.json":continue
        rec=raw_receipts[name]
        observed=dt.datetime.fromisoformat(rec["observed_at"])
        if rec["http_status"]!=200 or rec["sha256"]!=hashlib.sha256(body).hexdigest():
            raise ValueError("Acquisition integrity mismatch "+name)
        if not 0 <= (cutoff-observed).total_seconds() <= 900:
            raise ValueError("Stale acquisition "+name)
    return files


def execute():
    folder=capture.capture()
    cutoff=dt.datetime.now(dt.timezone.utc)
    files=validate_receipts(folder,cutoff)
    parsed=validation.reconstruct(files["games.txt"].decode("utf-8-sig"),
                                  files["standings.txt"].decode("utf-8-sig"))
    if parsed["standings_max_abs_difference"]>0.015:
        raise ValueError("All-game published-standings parity fails")
    documents={dt.datetime.strptime(n[:8],"%Y%m%d").date().isoformat():json.loads(v)
               for n,v in files.items() if re.fullmatch(r"\d{8}\.json",n)}
    count=validation.coverage(parsed,documents,cutoff)
    groups=groups_of_pairs(validation.rows(files["games.txt"].decode("utf-8-sig")))
    if count!=len(groups) or count!=parsed["games"]:
        raise ValueError("Full-game universe discrepancy")
    ids=independent_ids(documents)
    excluded,rows_checked=compare_full_box_stats(groups,ids)
    if rows_checked!=2*count:raise ValueError("Incomplete independent box audit")
    accepted,total=accepted_aggregates(groups,excluded)
    if total+len(excluded)!=count:
        raise ValueError("Accepted plus excluded games mismatch")
    through=parsed["latest"]
    current_nba_day=cutoff.astimezone(ZoneInfo("America/New_York")).date()
    if not 0<(current_nba_day-dt.date.fromisoformat(through)).days<=2:
        raise ValueError("Stale NBA input")
    serial_exclusions=[excluded[k] for k in sorted(excluded)]
    entry={
       "schema_version":"nba-model-c-accepted-candidate-v1",
       "publication_status":STATE,
       "model":"Frozen Model C v0.1 (no parameter changes)",
       "season":"2026-27",
       "data_through_nba_date":through,
       "generated_at_utc":cutoff.isoformat(),
       "raw_completed_games":count,
       "accepted_games":total,
       "excluded_games":len(excluded),
       "independent_box_team_rows_checked":rows_checked,
       "core_fields_verified_per_team":8,
       "data_provenance":{"boxscorelab_games_sha256":hashlib.sha256(files["games.txt"]).hexdigest(),
                          "boxscorelab_standings_sha256":hashlib.sha256(files["standings.txt"]).hexdigest(),
                          "source":"BoxScore Lab (CC BY 4.0)",
                          "independent_checks":"ESPN completed game dates, scores and eight team box fields"},
       "metric_definitions":{"gp":"accepted games per team",
                             "ortg":"arithmetic mean of per-game 100*points/P",
                             "drtg":"arithmetic mean of per-game 100*opp_points/P",
                             "pace":"arithmetic mean full-game P including OT",
                             "possessions":"P=0.5*sum_for_2_teams(FGA+0.44*FTA-OREB+TOV)"},
       "excluded_game_receipts":serial_exclusions,
       "teams":{t:accepted[t] for t in sorted(accepted)},
    }
    output=json.dumps(entry,sort_keys=True,indent=2,ensure_ascii=False,allow_nan=False)+"\n"
    digest=hashlib.sha256(output.encode()).hexdigest()
    name=through+"-accepted-"+digest[:12]
    path=ROOT_OUT/"accepted_candidates"
    path.mkdir(parents=True,exist_ok=True)
    fjson=path/(name+".json"); fmd=path/(name+".md")
    if fjson.exists() or fmd.exists():raise ValueError("Immutable candidate exists")
    fjson.write_text(output,encoding="utf-8")
    lines=[
       "# NBA Model C Accepted-Game Inputs — "+through,
       "", "**STATUS: EXPERIMENTAL — NOT PRODUCTION.**",
       "", "2026–27 season | BoxScore Lab (CC BY 4.0) | independent ESPN check",
       "", "**Raw completed games:** "+str(count),
       "**Accepted for Model C:** "+str(total),
       "**Fully quarantined games:** "+str(len(excluded)),
       "**Independent ESPN box team rows:** "+str(rows_checked),
       "**Data through (NBA ET date):** "+through,
       "**Generated UTC:** "+cutoff.isoformat(),
       "**JSON SHA-256:** "+digest,
       "**Source team-game SHA-256:** "+entry["data_provenance"]["boxscorelab_games_sha256"],
       "", "Inputs use estimated full-game possessions (OT included). GP counts ONLY non-conflicting accepted games.",
       "", "| Team | GP | ORtg | DRtg | Pace |",
       "|---|---:|---:|---:|---:|",
    ]
    for t in sorted(accepted):
        v=accepted[t]
        lines.append(f"| {t} | {v['n']} | {v['ortg']:.8f} | {v['drtg']:.8f} | {v['pace']:.8f} |")
    lines+=["","## Exclusions (whole games; no substitutions)",""]
    for x in serial_exclusions:
        lines.append("- "+x["date"]+" "+"/".join(x["teams"])+"; ESPN "+x["espn_game_id"]+"; "+json.dumps(x["mismatches"],sort_keys=True))
    if not serial_exclusions:lines.append("- None")
    lines+=["","This candidate is not a production publication. No frozen parameters were published or changed.",""]
    fmd.write_text("\n".join(lines),encoding="utf-8")
    index={
      "schema_version":"nba-model-c-accepted-candidate-index-v1",
      "status":STATE,
      "data_through_nba_date":through,
      "raw_completed_games":count,
      "accepted_games":total,
      "excluded_games":len(excluded),
      "independent_eight_box_fields":"PASS_WITH_WHOLE_GAME_EXCLUSIONS",
      "json_path":str(fjson.relative_to(ROOT)),
      "md_path":str(fmd.relative_to(ROOT)),
      "json_sha256":digest,
      "source_sha256":entry["data_provenance"]["boxscorelab_games_sha256"],
      "generated_at_utc":cutoff.isoformat(),
      "production_pointer_advanced":False,
    }
    ROOT_OUT.mkdir(exist_ok=True)
    (ROOT_OUT/"accepted_candidate_index.json").write_text(
       json.dumps(index,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(index,indent=2))
    return index

if __name__=="__main__":
    execute()
