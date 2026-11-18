#!/usr/bin/env python3
"""Read-only proof-of-feasibility: NBA Stats vs ESPN vs BoxScoreLab, full season."""
import csv,io,urllib.request,collections,json
def get(url):
 req=urllib.request.Request(url,headers={"User-Agent":"NBA-MI-source-parity-check/1.0"})
 with urllib.request.urlopen(req,timeout=35) as r: return list(csv.DictReader(io.StringIO(r.read().decode("utf-8-sig"))))
base="https://github.com/sportsdataverse/sportsdataverse-data/releases/download/"
nba=get(base+"nba_stats_team_boxscores/team_boxscores_2027.csv")
esp=get(base+"espn_nba_team_boxscores/team_box_2027.csv")
bsl=get("https://boxscorelab.com/downloads/2026-27-team-game-results.csv")
def norm(x):return {"GS":"GSW","NY":"NYK","NO":"NOP","SA":"SAS","WSH":"WAS","UTAH":"UTA"}.get(x,x)
fields={
 "FGM":("field_goals_made","field_goals_made","field_goals_made"),
 "FGA":("field_goals_attempted","field_goals_attempted","field_goal_attempts"),
 "3PM":("three_pointers_made","three_point_field_goals_made","three_point_makes"),
 "3PA":("three_pointers_attempted","three_point_field_goals_attempted","three_point_attempts"),
 "FTM":("free_throws_made","free_throws_made","free_throws_made"),
 "FTA":("free_throws_attempted","free_throws_attempted","free_throw_attempts"),
 "OREB":("rebounds_offensive","offensive_rebounds","offensive_rebounds"),
 "TOV_PLAYER":("turnovers","turnovers","turnovers")
}
nbag=collections.defaultdict(list)
for r in nba:
 if r["season_type_id"]=="2":nbag[r["game_id"]].append(r)
espng=collections.defaultdict(list)
for r in esp:
 if r["season_type"]=="2":espng[r["game_id"]].append(r)
bslg=collections.defaultdict(list)
for r in bsl:bslg[(r["game_date"],tuple(sorted((r["team"],r["opponent"]))))].append(r)
matcher=collections.defaultdict(list)
for game_id,pair in nbag.items():
 if len(pair)!=2:continue
 key=tuple(sorted((norm(r["team_tricode"]),int(r["points"])) for r in pair))
 matcher[key].append((game_id,pair))
stats=collections.Counter();differences=collections.Counter(); examples=[]
for gid,rows in espng.items():
 if len(rows)!=2:continue
 ky=tuple(sorted((norm(r["team_abbreviation"]),int(r["team_score"])) for r in rows))
 choices=matcher[ky]
 if len(choices)!=1:stats["unmatched_or_ambiguous"]+=1;continue
 stats["joined"]+=1
 nid,nrows=choices[0]
 N={norm(r["team_tricode"]):r for r in nrows}
 E={norm(r["team_abbreviation"]):r for r in rows}
 day=rows[0]["game_date"];bk=(day,tuple(sorted(E)))
 B={r["team"]:r for r in bslg.get(bk,[])}
 if B:stats["also_bsl"]+=1
 if not B:stats["missing_bsl"]+=1
 for team in E:
  for label,(nf,ef,bf) in fields.items():
   x=int(N[team][nf]);y=int(E[team][ef])
   if x!=y:
    differences["NBA_vs_ESPN_"+label]+=1
    if len(examples)<22:examples.append([day,team,label,x,y,"NBA_ESPN"])
   if team in B:
    z=int(B[team][bf])
    if z!=y:differences["BSL_vs_ESPN_"+label]+=1
    if z!=x:differences["BSL_vs_NBA_"+label]+=1
 for team in E:
  nturn=int(N[team]["turnovers"]);player=int(E[team]["turnovers"]);tturn=int(E[team]["team_turnovers"]);total=int(E[team]["total_turnovers"])
  if total!=player+tturn:differences["ESPN_total_turnovers_not_decomposable"]+=1
  if nturn+tturn!=total:differences["NBA_player_plus_ESPN_team_TOV_not_total"]+=1
 stats["day_"+day]+=1
print(json.dumps({"nba_games":len(nbag),"espn_games":len(espng),"bsl_games":len(bslg),
 "stats":stats,"differences":differences,"examples":examples},indent=2))
