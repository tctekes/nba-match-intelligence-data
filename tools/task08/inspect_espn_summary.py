#!/usr/bin/env python3
"""Inspect a single ESPN summary's team-stat schema; no publication."""
import json, urllib.parse, urllib.request

def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":"NBA-Match-Intelligence-Validation/1.0"})
    with urllib.request.urlopen(req,timeout=30) as r:
        return json.loads(r.read().decode())

day=get("https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates=20261111&seasontype=2&limit=100")
events=[e for e in day["events"] if e["status"]["type"]["completed"] and e["season"]["type"]==2]
if not events: raise RuntimeError("No completed sample games")
id=str(events[0]["id"])
s=get("https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event="+urllib.parse.quote(id))
box=s.get("boxscore",{})
teams=box.get("teams",[])
print("event_id",id,"team_count",len(teams),"boxscore_keys",list(box))
for team in teams:
    print(json.dumps({"team":team.get("team",{}).get("abbreviation"),
     "statistics":[{"name":x.get("name"),"displayValue":x.get("displayValue"),
                    "value":x.get("value")} for x in team.get("statistics",[])]},ensure_ascii=False))
