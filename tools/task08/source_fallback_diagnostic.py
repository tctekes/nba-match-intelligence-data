#!/usr/bin/env python3
"""Read-only diagnostic of NBA data source freshness, schema and missing games.
Never publishes or changes frozen model inputs.
"""
import csv,datetime as dt,hashlib,io,json,urllib.request
from collections import Counter
from zoneinfo import ZoneInfo

URLS={
 "bsl":"https://boxscorelab.com/downloads/2026-27-team-game-results.csv",
 "nba_stats":"https://github.com/sportsdataverse/sportsdataverse-data/releases/download/nba_stats_team_boxscores/team_boxscores_2027.csv",
 "espn_release":"https://github.com/sportsdataverse/sportsdataverse-data/releases/download/espn_nba_team_boxscores/team_box_2027.csv",
}
def fetch(url):
 req=urllib.request.Request(url,headers={"User-Agent":"NBA-MI-data-sanity/1.0"})
 with urllib.request.urlopen(req,timeout=35) as r:
  if r.status!=200:raise RuntimeError("HTTP "+str(r.status))
  return r.read(3_000_000)
def main():
 for key,url in URLS.items():
  try:
   raw=fetch(url)
   rows=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
   print(json.dumps({"source":key,"rows":len(rows),"sha256":hashlib.sha256(raw).hexdigest(),"columns":list(rows[0]) if rows else []}))
   if rows:
    columns=list(rows[0])
    dates=[k for k in columns if "date" in k.lower()]
    print(json.dumps({"source":key,"date_columns":dates,"last_five": [{k:r.get(k) for k in dates[:3]} for r in rows[-5:]]}))
    filters=[r for r in rows if any("0022600245" in str(v) or "401909994" in str(v) or (("2026-11-16" in str(v) or "2026-11-17" in str(v)) and ("BOS" in str(r) or "ORL" in str(r))) for v in r.values())]
    print(json.dumps({"source":key,"matching_orl_bos_or_nov16":filters[:3]},default=str)[:7500])
  except Exception as e:print(json.dumps({"source":key,"fetch_error":str(e)}))
if __name__=="__main__":main()
