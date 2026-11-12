"""Local, fail-closed static snapshot generator. No network or publication.
Use --input directory containing games.txt, standings.txt, downloads.txt and
YYYYMMDD.json ESPN daily scoreboards covering Oct 1 through cutoff date.
Capture sources immediately before running; cutoff is the validation observation
time, NOT a backdated forecast time. Requires the existing frozen baseline module.
"""
import argparse, collections, csv, datetime as dt, hashlib, io, json, math, re
from pathlib import Path
from zoneinfo import ZoneInfo
import nba_baseline_v01 as model

SEASON='2026-27'
SOURCE='https://www.boxscorelab.com/downloads/'
NY=ZoneInfo('America/New_York')
def sha(data): return hashlib.sha256(data).hexdigest()
def rows(text):
    reader=csv.DictReader(io.StringIO(text)); result=list(reader)
    assert reader.fieldnames and len(set(reader.fieldnames))==len(reader.fieldnames),'Duplicate columns'
    assert result and all(None not in r and None not in r.values() for r in result),'Malformed CSV'
    return result
def key(day,a,b): return (day,*sorted((a,b)))
def reconstruct(game_text,standing_text):
    groups=collections.defaultdict(list)
    for r in rows(game_text):
        assert r['season']==SEASON and r['team'] in model.TEAMS and r['opponent'] in model.TEAMS and r['team']!=r['opponent'],'Team/season'
        dt.date.fromisoformat(r['game_date'])
        groups[key(r['game_date'],r['team'],r['opponent'])].append(r)
    state={}; wl={t:[0,0] for t in model.TEAMS}; scores={}
    for k,pair in sorted(groups.items()):
        model.validate_pair(pair)
        a,b=pair
        for r in pair:
            for field in list(model.FIELDS)+['points','opponent_points']:
                v=float(r[field]); assert v.is_integer() and 0<=v<=250,'Invalid integer count'
            assert r['result']==('W' if float(r['points'])>float(r['opponent_points']) else 'L'),'Result'
            assert float(r['points'])!=float(r['opponent_points']),'Tied final'
            assert float(r['point_diff'])==float(r['points'])-float(r['opponent_points']),'Score margin'
        poss=lambda r:float(r['field_goal_attempts'])+.44*float(r['free_throw_attempts'])-float(r['offensive_rebounds'])+float(r['turnovers'])
        p=(poss(a)+poss(b))/2; assert 50<p<200,'Possessions'
        g=dict(home=a['team'],away=b['team'],hp=float(a['points']),ap=float(b['points']),possessions=p,minutes=48)
        model.update(state,g) # minutes only affect unused per-48 accumulator
        scores[k]={r['team']:float(r['points']) for r in pair}
        for r in pair: wl[r['team']][int(float(r['points'])<float(r['opponent_points']))]+=1
    assert set(state)==set(model.TEAMS),'Missing team'
    table={t:dict(model.rates(state[t]),wins=wl[t][0],losses=wl[t][1]) for t in model.TEAMS}
    standings=rows(standing_text)
    assert len(standings)==30 and {r['team'] for r in standings}==set(model.TEAMS),'Standings teams'
    diffs=[]
    for r in standings:
        t=table[r['team']]; assert r['season']==SEASON,'Standings season'
        assert [int(r[x]) for x in ('games','wins','losses')]==[t['n'],t['wins'],t['losses']],'Standings GP/W/L mismatch'
        assert 1<=t['n']<=82 and t['n']==t['wins']+t['losses'],'GP'
        for field,out in [('off_rating_est','ortg'),('def_rating_est','drtg'),('pace','pace')]:
            assert math.isfinite(t[out]) and 50<t[out]<160,'Numeric range'
            diffs.append(abs(float(r[field])-t[out]))
    return dict(teams=table,scores=scores,latest=max(k[0] for k in scores),games=len(scores),standings_max_abs_difference=max(diffs))

def coverage(data,documents,cutoff):
    expected={}; today=cutoff.astimezone(NY).date(); seen=set(); incomplete=[]
    for day,doc in sorted(documents.items()):
        assert isinstance(doc.get('events'),list) and doc.get('leagues'),'Invalid reference'
        calendar=doc['leagues'][0].get('calendar')
        assert isinstance(calendar,list),'Missing reference calendar'
        assert doc['events'] or not any(str(x)[:10]==day for x in calendar),'Empty reference on scheduled day'
        for e in doc['events']:
            if e['season']['type']!=2: continue
            c=e['competitions'][0]
            if any('championship' in n.get('headline','').lower() for n in c.get('notes',[])): continue
            competitors=c['competitors']; teams=[model.norm(x['team']['abbreviation']) for x in competitors]
            if not all(t in model.TEAMS for t in teams): continue
            assert len(teams)==2 and teams[0]!=teams[1] and e['id'] not in seen,'Duplicate reference'
            seen.add(e['id']); tip=dt.datetime.fromisoformat(e['date'].replace('Z','+00:00'))
            assert tip.astimezone(NY).date().isoformat()==day,'Reference day'
            k=key(day,*teams); status=e['status']['type']
            if status['completed']:
                assert tip<cutoff,'Future final'
                assert k in data['scores'],f'Missing completed game {e["id"]} ({day})'
                score={model.norm(x['team']['abbreviation']):float(x['score']) for x in competitors}
                assert data['scores'][k]==score,'Independent score disagreement'
                expected[k]=score
            elif day<=data['latest'] and status['name'] not in ('STATUS_POSTPONED','STATUS_CANCELED'):
                incomplete.append(e['id'])
    assert not incomplete,'Partial NBA day'
    start=dt.date(2026,10,1)
    needed={(start+dt.timedelta(days=i)).isoformat() for i in range((today-start).days+1)}
    assert set(documents)==needed,'Full-season daily reference coverage missing'
    assert set(expected)==set(data['scores']),'Completed-game universe mismatch'
    assert (today-dt.date.fromisoformat(data['latest'])).days<=2,'Stale source'
    # Same-day finals lack reliable completion timestamps; conservatively reject.
    assert data['latest']<today.isoformat(),'Current NBA date cannot be certified closed'
    return len(expected)

def render(payload):
    checksum=sha(json.dumps(payload,sort_keys=True,separators=(',',':'),allow_nan=False).encode())
    lines=['# NBA Model C v0.1 static inputs',f'Season: {SEASON}',f'Validation: **{payload["validation"]}**',f'Data-through NBA date: {payload["data_through"]}',f'Generation/cutoff UTC: {payload["cutoff"]}',f'Completed source games: {payload["game_count"]}',f'Publisher build claim: {payload["build"]} (CSV/build binding UNVERIFIED)',f'Canonical JSON payload SHA-256: `{checksum}`','',f'Source: [BoxScore Lab]({SOURCE}); [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Changes: validation, paired-possession reconstruction, aggregation and formatting. ESPN used for validation only.','', 'GP = accepted completed games. P = mean of both teams’ (FGA + 0.44 FTA − OREB + TOV). ORtg/DRtg = arithmetic mean of 100 × scored/allowed points per P. Pace = arithmetic mean full-game P, including OT; NOT per 48 minutes. Rates printed to 10 decimals. No predictions.','']
    if payload['validation']=='PASS':
        lines+=['| Team | GP | W | L | ORtg | DRtg | Pace |','|---|---:|---:|---:|---:|---:|---:|']
        for team,t in payload['teams'].items(): lines.append(f'| {team} | {t["n"]} | {t["wins"]} | {t["losses"]} | {t["ortg"]:.10f} | {t["drtg"]:.10f} | {t["pace"]:.10f} |')
    else: lines+=['No usable team table. Reason: '+payload['reason']]
    lines+=['','Receipts:',*['- '+name+': SHA-256 `'+value+'`' for name,value in payload['receipts'].items()]]
    return '\n\n'.join(lines[:9])+'\n'+'\n'.join(lines[9:])+'\n'

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input',type=Path,required=True); ap.add_argument('--output',type=Path,default=Path('snapshots')); args=ap.parse_args()
    files={p.name:p.read_bytes() for p in args.input.iterdir() if p.suffix in ('.txt','.json')}
    cutoff=dt.datetime.now(dt.timezone.utc)
    build=re.findall(r'build\s+(\d{8}T\d{4})',re.sub(r'<[^>]*>','',files['downloads.txt'].decode()))
    payload=dict(schema_version=1,validation='FAIL',cutoff=cutoff.isoformat(),build=sorted(set(build)) or 'UNVERIFIED',receipts={n:sha(v) for n,v in files.items()},data_through='UNKNOWN',game_count=0)
    try:
        data=reconstruct(files['games.txt'].decode('utf-8-sig'),files['standings.txt'].decode('utf-8-sig'))
        payload.update(data_through=data['latest'],game_count=data['games'],standings_max_abs_difference=data['standings_max_abs_difference'])
        docs={dt.datetime.strptime(n[:8],'%Y%m%d').date().isoformat():json.loads(v) for n,v in files.items() if re.fullmatch(r'\d{8}\.json',n)}
        coverage(data,docs,cutoff)
        receipt=json.loads(files['fetch_receipts.json'])
        for name,body in files.items():
            if name=='fetch_receipts.json': continue
            r=receipt[name]; observed=dt.datetime.fromisoformat(r['observed_at'])
            assert r['sha256']==sha(body) and r['http_status']==200,'Fetch receipt mismatch'
            assert 0<=(cutoff-observed).total_seconds()<=900,'Stale acquisition receipt'
        payload.update(validation='PASS',teams=data['teams'])
    except (AssertionError,ValueError,KeyError) as e: payload['reason']=str(e)
    args.output.mkdir(parents=True,exist_ok=True)
    name=payload['data_through']; target=args.output/(name+'.md')
    assert not target.exists(),'Date artifact exists; immutable output refuses overwrite'
    target.write_text(render(payload),encoding='utf-8'); target.with_suffix('.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(payload,indent=2))

if __name__=='__main__': main()