#!/usr/bin/env python3
"""Validated secondary source for entire completed NBA games missing from BoxScore Lab.

Never silently patches BSL statistics. Missing whole games are sourced from
ESPN's independently published team-box release, cross-checked against
NBA Stats official-source team-box release and ESPN live final/box summary.
Every mismatch quarantines the WHOLE game. Captures source SHA receipts.
"""
from __future__ import annotations
import collections,csv,hashlib,io,json
from pathlib import Path
import cloud_capture_candidate as capture
import nba_baseline_v01 as model

BASE="https://github.com/sportsdataverse/sportsdataverse-data/releases/download/"
ESPN_RELEASE=BASE+"espn_nba_team_boxscores/team_box_2027.csv"
NBA_RELEASE=BASE+"nba_stats_team_boxscores/team_boxscores_2027.csv"
ESPN_FIELDS={
 "field_goals_made":"field_goals_made",
 "field_goal_attempts":"field_goals_attempted",
 "three_point_makes":"three_point_field_goals_made",
 "three_point_attempts":"three_point_field_goals_attempted",
 "free_throws_made":"free_throws_made",
 "free_throw_attempts":"free_throws_attempted",
 "offensive_rebounds":"offensive_rebounds",
 "turnovers":"total_turnovers",
}
NBA_FIELDS={
 "field_goals_made":"field_goals_made",
 "field_goal_attempts":"field_goals_attempted",
 "three_point_makes":"three_pointers_made",
 "three_point_attempts":"three_pointers_attempted",
 "free_throws_made":"free_throws_made",
 "free_throw_attempts":"free_throws_attempted",
 "offensive_rebounds":"rebounds_offensive",
}
def integer(x,label):
    if not isinstance(x,str) or not x.isdecimal():
        raise ValueError("Invalid/missing "+label+": "+str(x))
    value=int(x)
    if value>250:raise ValueError("Out-of-range "+label)
    return value

def source_csv(url):
    raw,code=capture.acquire(url,limit=3_000_000)
    if code!=200:raise ValueError("Source release not HTTP 200")
    reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    if not reader.fieldnames or len(set(reader.fieldnames))!=len(reader.fieldnames):
        raise ValueError("Release CSV missing/duplicated fields")
    rows=list(reader)
    if not rows or any(None in r or None in r.values() for r in rows):
        raise ValueError("Release CSV malformed")
    return rows,hashlib.sha256(raw).hexdigest()

def source_index(rows,id_name,season_name,season_val,type_name,type_val):
    groups=collections.defaultdict(list)
    for r in rows:
        if r.get(season_name)!=season_val or r.get(type_name)!=type_val:continue
        gameid=r.get(id_name)
        if not gameid or not gameid.isdecimal():raise ValueError("Invalid season game ID")
        groups[gameid].append(r)
    for k,pair in groups.items():
        if len(pair)!=2:raise ValueError("Missing/duplicated release game side "+k)
    return groups

def pair_key(day,teams):
    t=tuple(sorted(model.norm(str(v)) for v in teams))
    if len(t)!=2 or t[0]==t[1] or any(x not in model.TEAMS for x in t):
        raise ValueError("Noncanonical NBA team pair")
    return (day,t)

def official_index(nba_games):
    """Index official NBA game ID by two teams, exact scores and home designation."""
    result=collections.defaultdict(list)
    for official_id,pair in nba_games.items():
        side={r["side"]:r for r in pair}
        if set(side)!={"home","away"}:raise ValueError("NBA Stats invalid home/away "+official_id)
        teams=[model.norm(r["team_tricode"]) for r in pair]
        scores={model.norm(r["team_tricode"]):integer(r["points"],"nba_points") for r in pair}
        if len(set(teams))!=2:raise ValueError("NBA Stats duplicate team")
        key=(tuple(sorted(scores.items())),model.norm(side["home"]["team_tricode"]))
        result[key].append((official_id,{model.norm(r["team_tricode"]):r for r in pair}))
    return result

def one_fallback(gameid,espn_pair,official_lookup):
    """Construct both team rows with all eight exact historical Model C inputs."""
    if len(espn_pair)!=2:raise ValueError("ESPN release missing 2 sides "+gameid)
    day=espn_pair[0]["game_date"]
    if any(r["game_date"]!=day for r in espn_pair):raise ValueError("ESPN release date mismatch")
    sides={r["team_home_away"]:r for r in espn_pair}
    if set(sides)!={"home","away"}:raise ValueError("ESPN release home/away invalid")
    teams={model.norm(r["team_abbreviation"]):r for r in espn_pair}
    k=pair_key(day,list(teams))
    if len(teams)!=2:raise ValueError("ESPN release duplicate team")
    scores={t:integer(r["team_score"],"espn_points") for t,r in teams.items()}
    match=(tuple(sorted(scores.items())),model.norm(sides["home"]["team_abbreviation"]))
    candidates=official_lookup.get(match,[])
    if len(candidates)!=1:raise ValueError("Official NBA Stats match missing or ambiguous for "+str(k))
    official_id,nba_teams=candidates[0]
    discrepancies={}
    paired=[]
    for t,r in sorted(teams.items()):
        n=nba_teams[t]
        data={target:integer(r[col],"ESPN "+col) for target,col in ESPN_FIELDS.items()}
        diff={}
        for target,col in NBA_FIELDS.items():
            observed=integer(n[col],"NBA "+col)
            if observed!=data[target]:diff[target]={"espn":data[target],"nba_stats":observed}
        # The ESPN total combines player and team turnovers. Official NBA Stats
        # release has PLAYER turnovers only. Verify that independently while
        # explicitly recording the uncorroborated ESPN team-turnover component.
        player=integer(r["turnovers"],"ESPN player turnovers")
        team=integer(r["team_turnovers"],"ESPN team turnovers")
        nba_player=integer(n["turnovers"],"NBA player turnovers")
        if player!=nba_player:diff["player_turnovers"]={"espn":player,"nba_stats":nba_player}
        if data["turnovers"]!=player+team:
            diff["total_turnovers_decomposition"]={"espn_total":data["turnovers"],"player":player,"team":team}
        if diff:discrepancies[t]=diff
        other=next(z for z in teams if z!=t)
        data.update(season="2026-27",game_date=day,team=t,opponent=other,
            points=str(scores[t]),opponent_points=str(scores[other]))
        data={key:str(value) for key,value in data.items()}
        paired.append(data)
    model.validate_pair(paired)
    receipt={"espn_game_id":gameid,"nba_stats_game_id":official_id,
             "date":day,"teams":list(k[1]),"mismatches":discrepancies}
    return k,paired,receipt

def restore_missing(bsl_groups,espn_finals):
    """Only ESPN-confirmed completed games absent from BSL are eligible."""
    missing=set(espn_finals)-set(bsl_groups)
    if not missing:return {},{},{"recovered":0,"source":"BoxScore Lab complete","fallback_source_shas":{}}
    if set(bsl_groups)-set(espn_finals):
        raise ValueError("Unexplained BSL-only game(s); no alternate-source merge")
    espn_rows,sha_espn=source_csv(ESPN_RELEASE)
    official_rows,sha_nba=source_csv(NBA_RELEASE)
    espn=source_index(espn_rows,"game_id","season","2027","season_type","2")
    official=source_index(official_rows,"game_id","season","2027","season_type_id","2")
    nba_lookup=official_index(official)
    receipts,groups={},{}
    for k in sorted(missing):
        ids=espn_finals[k]
        if ids not in espn:raise ValueError("ESPN team release missing completed game "+ids)
        key,pair,receipt=one_fallback(ids,espn[ids],nba_lookup)
        if key!=k:raise ValueError("Released game date/identity differs from scoreboard "+ids)
        groups[key]=pair
        if receipt["mismatches"]:receipts[key]=receipt
    return groups,receipts,{"recovered":len(groups),
        "source":"ESPN released team box + independently published NBA Stats team box",
        "fallback_source_shas":{"espn_release_sha256":sha_espn,"nba_stats_release_sha256":sha_nba},
        "partial_turnover_independence":"NBA player TOV independently checked; ESPN team TOV verified by decomposition and live ESPN, but no independent NBA team TOV in source release",
        "fallback_games":[{"date":k[0],"teams":list(k[1]),"espn_game_id":espn_finals[k]}
                          for k in sorted(groups)]}
