#!/usr/bin/env python3
"""Research-only replay source. No Model C parameters or model inference.
Parses the *same public source families* and exact eight-stat whole-game
exclusions as the original archived four-season evaluation.
Output is an isolated, compact accepted-game table for offline comparison.
"""
import collections,csv,datetime as dt,hashlib,io,json,urllib.request
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"/"task08"))
import nba_baseline_v01 as check

OUT=Path(__file__).resolve().parent/"datasets"
BASE="https://github.com/sportsdataverse/sportsdataverse-data/releases/download/"
EXPECTED={2023:(1230,1226),2024:(1230,1223),2025:(1230,1224),2026:(1230,1222)}
def get_csv(url,manifest):
    req=urllib.request.Request(url,headers={"User-Agent":"NBA-MI-research-replay/1.0","Accept":"*/*"})
    with urllib.request.urlopen(req,timeout=90) as r:
        if r.status!=200:raise ValueError("Non-200 historical source "+url)
        body=r.read(16000000)
    if not body or len(body)>=16000000:raise ValueError("Missing/oversized historical source")
    manifest[url]={"sha256":hashlib.sha256(body).hexdigest(),"bytes":len(body)}
    reader=csv.DictReader(io.StringIO(body.decode("utf-8-sig")))
    if not reader.fieldnames or len(reader.fieldnames)!=len(set(reader.fieldnames)):
        raise ValueError("Unexpected CSV columns "+url)
    rows=list(reader)
    if not rows or any(None in row or None in row.values() for row in rows):
        raise ValueError("Malformed CSV "+url)
    return rows

def load(year,manifest):
    short=f"{year-1}-{str(year)[2:]}"
    games=get_csv(f"https://www.boxscorelab.com/downloads/{short}-team-game-results.csv",manifest)
    schedule=get_csv(BASE+f"espn_nba_schedules/nba_schedule_{year}.csv",manifest)
    box=get_csv(BASE+f"espn_nba_team_boxscores/team_box_{year}.csv",manifest)
    scheduled=collections.defaultdict(list)
    for r in schedule:
        k=(r["game_date"],tuple(sorted((check.norm(r["home_abbreviation"]),check.norm(r["away_abbreviation"])))))
        scheduled[k].append(r)
    boxed=collections.defaultdict(list)
    for r in box:
        boxed[(r["game_id"],check.norm(r["team_abbreviation"]))].append(r)
    grouped=collections.defaultdict(list)
    for r in games:
        k=(r["game_date"],tuple(sorted((r["team"],r["opponent"]))))
        grouped[k].append(r)
    result=[];excluded=[];neutral_ambiguities=0
    for k,pair in sorted(grouped.items()):
        gid=None
        try:
            check.validate_pair(pair)
            matches=scheduled[k]
            if len(matches)!=1:raise ValueError("Missing or ambiguous schedule join")
            s=matches[0];gid=s["game_id"]
            if s["season_type"]!="2" or not all(t in check.TEAMS for t in k[1]):
                raise ValueError("Not regular season")
            if "championship" in s.get("notes_headline","").lower():
                raise ValueError("Cup championship excluded")
            if s["status_type_completed"].lower()!="true":raise ValueError("Not final")
            period=float(s["status_period"])
            if period!=int(period) or period<4:raise ValueError("Bad period")
            home,away=check.norm(s["home_abbreviation"]),check.norm(s["away_abbreviation"])
            by_team={r["team"]:r for r in pair}
            h,a=by_team[home],by_team[away]
            if float(h["points"])!=float(s["home_score"]) or float(a["points"])!=float(s["away_score"]):
                raise ValueError("Independent final-score mismatch")
            if h["home"]==a["home"]:neutral_ambiguities+=1
            mismatch=[]
            for r in pair:
                bs=boxed[(gid,r["team"])]
                if len(bs)!=1:
                    mismatch.append(r["team"]+" missing independent row");continue
                for field,ext in check.FIELDS.items():
                    if not bs[0][ext].strip() or float(r[field])!=float(bs[0][ext]):
                        mismatch.append(r["team"]+" "+field+" disagreement")
            if mismatch:raise ValueError("; ".join(mismatch))
            pos=lambda r:float(r["field_goal_attempts"])+.44*float(r["free_throw_attempts"])-float(r["offensive_rebounds"])+float(r["turnovers"])
            p=(pos(h)+pos(a))/2
            if not 50<p<200:raise ValueError("Invalid possessions")
            hp,ap=float(h["points"]),float(a["points"])
            if hp==ap:raise ValueError("Tied final")
            # Stable compact columns: [ID, league_date, tip_utc, home, away, neutral, hp, ap, possessions, minutes]
            result.append([gid,k[0],s["date"],home,away,s["neutral_site"].lower()=="true",hp,ap,p,48+5*(int(period)-4)])
        except (ValueError,KeyError,IndexError,TypeError) as exc:
            excluded.append({"id":gid,"date":k[0],"teams":k[1],"reason":str(exc)})
    result.sort(key=lambda row:(row[1],row[2],row[0]))
    if (len(grouped),len(result))!=EXPECTED[year]:
        raise ValueError(f"Historical coverage regression {year}: raw={len(grouped)} accepted={len(result)} expected={EXPECTED[year]}")
    return result,{"raw":len(grouped),"accepted":len(result),"excluded":excluded,"neutral_ambiguities":neutral_ambiguities}

def run():
    manifest={}; seasons={};audits={}
    for year in EXPECTED:
        seasons[str(year)],audits[str(year)]=load(year,manifest)
        print(year,"PASS",audits[str(year)]["raw"],audits[str(year)]["accepted"])
    output={"schema":"NBA_MI_HISTORICAL_REPLAY_SOURCE_V1_RESEARCH_ONLY",
            "columns":["game_id","nba_date","tipoff_utc","home","away","neutral","home_points","away_points","paired_possessions","minutes"],
            "source_policy":"Exactly eight BSL vs ESPN core field checks; whole-game exclusion on conflict",
            "attribution":"BoxScore Lab team-game results (CC BY 4.0); sportsdataverse-data ESPN-derived schedule and box scores",
            "seasons":seasons,"audit":audits,"sources":manifest}
    OUT.mkdir(parents=True,exist_ok=True)
    raw=(json.dumps(output,ensure_ascii=False,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")
    if len(raw)>980_000:raise ValueError("Dataset exceeds GitHub Contents readable limit")
    path=OUT/"historical_accepted_games_2023_2026.json"
    path.write_bytes(raw)
    print(json.dumps({"result":"PASS","games":sum(len(x) for x in seasons.values()),
       "bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"path":str(path)}))
if __name__=="__main__":run()
