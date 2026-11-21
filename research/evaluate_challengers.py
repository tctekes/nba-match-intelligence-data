#!/usr/bin/env python3
"""Predeclared, isolated NBA challenger model comparison.
No frozen model file, private parameters, or production state is read or changed.
Selection: 2024-25 validation; holdout: 2025-26, once, after selection.
Replay C-v0.1 architecture to test historical published metric parity.
"""
from __future__ import annotations
import collections,datetime as dt,hashlib,json,math,statistics
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
SRC=HERE/"datasets"/"historical_accepted_games_2023_2026.json"
REPORT=HERE/"reports"/"form_challenger_v1.json"
MD=HERE/"reports"/"form_challenger_v1.md"

# Candidate specification frozen BEFORE reading holdout outcome data.
# rho=0 removes prior-season TEAM-specific deviation, while the league-
# neutral stabilizer remains; k_eff controls early-season regularization.
CONFIGS=[
 {"id":"C_reference_reconstruction","k_eff":20,"k_pace":5,"rho":.5,"window":0},
 {"id":"A_no_team_prior_k20","k_eff":20,"k_pace":5,"rho":0.,"window":0},
 {"id":"B_no_team_prior_k10","k_eff":10,"k_pace":5,"rho":0.,"window":0},
 {"id":"C_no_team_prior_k5","k_eff":5,"k_pace":5,"rho":0.,"window":0},
 {"id":"D_no_team_prior_recent5_k5","k_eff":5,"k_pace":5,"rho":0.,"window":5},
]
def groups(raw):
    return {int(year):[
      dict(id=row[0],date=row[1],tip=row[2],home=row[3],away=row[4],neutral=row[5],
           hp=float(row[6]),ap=float(row[7]),possessions=float(row[8]),minutes=float(row[9]),
           margin=float(row[6])-float(row[7]),total=float(row[6])+float(row[7]),winner=int(row[6]>row[7]))
      for row in rows] for year,rows in raw.items()}

def league(rates):
    denom=sum(r["n"] for r in rates.values())
    if not denom:raise AssertionError("No prior league games")
    return {k:sum(r[k]*r["n"] for r in rates.values())/denom for k in ("ortg","drtg","pace")}

def compute_rates(history,window=0):
    out={}
    for t,games in history.items():
        used=games[-window:] if window else games
        n=len(used)
        out[t]={"n":n,"ortg":sum(x[0] for x in used)/n,
                "drtg":sum(x[1] for x in used)/n,
                "pace":sum(x[2] for x in used)/n}
    return out

def add_game(hist,g):
    hp,ap,p=g["hp"],g["ap"],g["possessions"]
    hist[g["home"]].append((100*hp/p,100*ap/p,p))
    hist[g["away"]].append((100*ap/p,100*hp/p,p))

def shrink(row,prior,center,config):
    n=row["n"];out={}
    for k in ("ortg","drtg","pace"):
        kk=config["k_pace"] if k=="pace" else config["k_eff"]
        w=n/(n+kk) if n+kk else 0
        val=center[k]+config["rho"]*(prior[k]-center[k])
        out[k]=w*row[k]+(1-w)*val
    return out

def features(games,prior_games,config):
    prev=collections.defaultdict(list)
    for g in prior_games:add_game(prev,g)
    previous=compute_rates(prev)
    previous_league=league(previous)
    history=collections.defaultdict(list)
    output=[]
    for day,batch_it in __import__("itertools").groupby(games,key=lambda g:g["date"]):
        batch=list(batch_it)
        full=compute_rates(history)
        # Stable league mean as in frozen C; recency changes team-specific
        # offensive/defensive form, not the league-wide center definition.
        n=sum(x["n"] for x in full.values())
        center=dict(previous_league)
        weight=(n/2)/(n/2+30)
        for k in ("ortg","drtg"):
            live=sum(r[k]*r["n"] for r in full.values())/n if n else previous_league[k]
            center[k]=weight*live+(1-weight)*previous_league[k]
        current=compute_rates(history,config["window"]) if config["window"] else full
        for g in batch:
            h=current.get(g["home"],dict(n=0,**center))
            a=current.get(g["away"],dict(n=0,**center))
            ph=previous.get(g["home"],previous_league)
            pa=previous.get(g["away"],previous_league)
            hr=shrink(h,ph,center,config)
            ar=shrink(a,pa,center,config)
            pace=(hr["pace"]+ar["pace"])/2
            baseline=(center["ortg"]+center["drtg"])/2
            home_rate=hr["ortg"]+ar["drtg"]-baseline
            away_rate=ar["ortg"]+hr["drtg"]-baseline
            x=(pace*(home_rate-away_rate)/100,
               float(not g["neutral"]),
               pace*(home_rate+away_rate)/100)
            output.append({"g":g,"x":x,"nh":len(history[g["home"]]),"na":len(history[g["away"]])})
        for g in batch:add_game(history,g)
    return output

def fit(rows):
    x=np.asarray([r["x"] for r in rows],dtype=float)
    ym=np.asarray([r["g"]["margin"] for r in rows],dtype=float)
    yt=np.asarray([r["g"]["total"] for r in rows],dtype=float)
    w=np.asarray([r["g"]["winner"] for r in rows],dtype=float)
    margin=np.linalg.lstsq(x[:,:2],ym,rcond=None)[0]
    total=np.linalg.lstsq(np.column_stack([np.ones(len(x)),x[:,2]]),yt,rcond=None)[0]
    pm=x[:,:2]@margin
    slope=.1
    for _ in range(50):
        prob=1/(1+np.exp(-np.clip(slope*pm,-35,35)))
        delta=np.sum(pm*(w-prob))/max(1e-8,np.sum(pm*pm*prob*(1-prob)))
        slope=max(.00001,min(1,slope+delta))
        if abs(delta)<1e-10:break
    return [float(margin[0]),float(margin[1]),float(total[0]),float(total[1]),float(slope)]

def predict(rows,coeffs):
    m,h,i,s,beta=coeffs
    out=[]
    for row in rows:
        x=row["x"];margin=m*x[0]+h*x[1]
        total=i+s*x[2]
        p=1/(1+math.exp(-max(-35,min(35,beta*margin))))
        out.append({"g":row["g"],"nh":row["nh"],"na":row["na"],"p":p,"m":margin,"total":total})
    return out

def scores(rows):
    n=len(rows)
    if not n:raise ValueError("Empty evaluation")
    return {"n":n,
     "accuracy":sum((x["p"]>=.5)==bool(x["g"]["winner"]) for x in rows)/n,
     "brier":sum((x["p"]-x["g"]["winner"])**2 for x in rows)/n,
     "log_loss":sum(-x["g"]["winner"]*math.log(max(1e-12,x["p"]))-(1-x["g"]["winner"])*math.log(max(1e-12,1-x["p"])) for x in rows)/n,
     "margin_mae":sum(abs(x["m"]-x["g"]["margin"]) for x in rows)/n,
     "total_mae":sum(abs(x["total"]-x["g"]["total"]) for x in rows)/n,
     "mean_p":sum(x["p"] for x in rows)/n}

def validation_score(rows):
    return statistics.mean(((r["m"]-r["g"]["margin"])/15)**2+((r["total"]-r["g"]["total"])/22)**2 for r in rows)

def date_cluster_ci(a,b,seed=11012026,resamples=4000):
    day=collections.defaultdict(list)
    assert [r["g"]["id"] for r in a]==[r["g"]["id"] for r in b]
    for x,y in zip(a,b):
        day[x["g"]["date"]].append((
          (x["p"]-x["g"]["winner"])**2-(y["p"]-y["g"]["winner"])**2,
          abs(x["m"]-x["g"]["margin"])-abs(y["m"]-y["g"]["margin"]),
          abs(x["total"]-x["g"]["total"])-abs(y["total"]-y["g"]["total"])))
    vals=np.array([[sum(t[i] for t in ds) for i in range(3)]+[len(ds)] for ds in day.values()])
    rng=np.random.default_rng(seed)
    ids=rng.integers(0,len(vals),size=(resamples,len(vals)))
    picks=vals[ids].sum(axis=1)
    v=picks[:,:3]/picks[:,3,None]
    est=vals[:,:3].sum(axis=0)/vals[:,3].sum()
    return {"metrics":["brier_difference","margin_mae_difference","total_mae_difference"],
      "selected_minus_reference":est.tolist(),
      "date_cluster_95ci":np.quantile(v,[.025,.975],axis=0).T.tolist(),
      "dates":len(vals),"bootstrap_resamples":resamples}

def phase(rows):
    specs=(("early_0_9",0,10),("middle_10_19",10,20),("late_20_plus",20,100))
    return {name:scores([r for r in rows if lo<=min(r["nh"],r["na"])<hi])
            if any(lo<=min(r["nh"],r["na"])<hi for r in rows) else None
            for name,lo,hi in specs}

def pregame_form_shift_ids(games,minimum_net_shift=10):
    """Exploratory diagnostic only; for each team use ONLY its prior games.
    Compare most recent 5 vs previous 5 in net efficiency, pts per 100.
    Selection and coefficients remain fixed before seeing holdout results.
    """
    team=collections.defaultdict(list)
    flagged=set()
    direction=collections.Counter()
    for day,batch_it in __import__("itertools").groupby(games,key=lambda g:g["date"]):
        batch=list(batch_it)
        for g in batch:
            for t in (g["home"],g["away"]):
                rows=team[t]
                if len(rows)<10:continue
                recent=sum(p[0]-p[1] for p in rows[-5:])/5
                older=sum(p[0]-p[1] for p in rows[-10:-5])/5
                delta=recent-older
                if abs(delta)>=minimum_net_shift:
                    flagged.add(g["id"])
                    direction["rising" if delta>0 else "falling"]+=1
        for g in batch:add_game(team,g)
    return flagged,dict(direction)


def evaluate():
    raw=SRC.read_bytes()
    data=json.loads(raw)
    if data["schema"]!="NBA_MI_HISTORICAL_REPLAY_SOURCE_V1_RESEARCH_ONLY":
        raise ValueError("Unknown source format")
    seasons=groups(data["seasons"])
    expected={2023:1226,2024:1223,2025:1224,2026:1222}
    if {k:len(v) for k,v in seasons.items()}!=expected:
        raise ValueError("Historical acceptance gate failed")
    comparisons={}
    # Only development outcomes participate in model selection.
    for conf in CONFIGS:
        train=features(seasons[2024],seasons[2023],conf)
        val=features(seasons[2025],seasons[2024],conf)
        coeffs=fit(train)
        val_preds=predict(val,coeffs)
        comparisons[conf["id"]]={"validation":scores(val_preds),
           "validation_selection_score":validation_score(val_preds),
           "config":conf}
    challengers=[x for x in CONFIGS if x["id"]!="C_reference_reconstruction"]
    chosen=min(challengers,key=lambda c:(comparisons[c["id"]]["validation_selection_score"],c["id"]))
    selected_id=chosen["id"]
    # Freeze the choice and refit on development-only BEFORE holdout.
    out={}
    for conf in (CONFIGS[0],chosen):
        dev=features(seasons[2024],seasons[2023],conf)+features(seasons[2025],seasons[2024],conf)
        coef=fit(dev)
        hold=features(seasons[2026],seasons[2025],conf)
        out[conf["id"]]=predict(hold,coef)
    old=out["C_reference_reconstruction"];new=out[selected_id]
    oldsc=scores(old);newsc=scores(new)
    # Form-shift sample is a diagnostic, not model selection. Its membership
    # is based strictly on past completed same-season games as-of each date.
    shifts,shift_directions=pregame_form_shift_ids(seasons[2026])
    recent_conf=next(x for x in CONFIGS if x["id"]=="D_no_team_prior_recent5_k5")
    recent_dev=features(seasons[2024],seasons[2023],recent_conf)+features(seasons[2025],seasons[2024],recent_conf)
    recent_hold=predict(features(seasons[2026],seasons[2025],recent_conf),fit(recent_dev))
    shift_stats={
      "definition":"At least one team had pregame absolute delta >=10 net rating pts/100 between most recent 5 and previous 5 league games; minimum 10 pregame games",
      "exploratory_not_used_for_promotion":True,
      "n":len(shifts),"direction_counts":shift_directions,
      "model_c":scores([r for r in old if r["g"]["id"] in shifts]),
      "selected_challenger":scores([r for r in new if r["g"]["id"] in shifts]),
      "recent5_challenger":scores([r for r in recent_hold if r["g"]["id"] in shifts]),
      "recent5_all_games":scores(recent_hold)
    }
    # This is a strict public-data replay/parity gate against the known
    # frozen Model C holdout values, not an implementation of the private model.
    parity=(abs(oldsc["accuracy"]-.6858)<.00015
            and abs(oldsc["brier"]-.204926)<.000008
            and abs(oldsc["margin_mae"]-11.420)<.008
            and abs(oldsc["total_mae"]-15.294)<.008)
    if not parity:raise ValueError("C-v0.1 reference replay parity FAIL; cannot judge challenger: "+str(oldsc))
    ci=date_cluster_ci(new,old)
    # Precommitted promotion rule: both Brier and MAE not worse, and at least
    # one primary metric 95% paired CI excludes zero in beneficial direction.
    b,margin,total=ci["selected_minus_reference"]
    interval=ci["date_cluster_95ci"]
    superior=(b<=0 and total<=0 and (interval[0][1]<0 or interval[2][1]<0))
    verdict="PROMOTION_RESEARCH_ELIGIBLE_NOT_AUTOMATIC" if superior else "NO_PROMOTION_KEEP_FROZEN_C"
    result={"status":"PASS_INDEPENDENT_HISTORICAL_REPLAY",
       "data_sha256":hashlib.sha256(raw).hexdigest(),
       "sources":data["source_policy"],
       "design":"2022-23 prior only; 2023-24 train; 2024-25 validation/challenger select; 2023-24+2024-25 refit; 2025-26 once-only holdout",
       "candidate_selection":"Best challenger by normalized margin MSE/225 + total MSE/484 in 2024-25 (regardless of baseline)",
       "candidate_configs_predeclared":CONFIGS,"development_scores":comparisons,
       "selected_challenger":selected_id,"reference_reproduction_parity":"PASS",
       "holdout":{"C_reproduction":oldsc,"selected_challenger":newsc,
                  "selected_subgroups":phase(new),"reference_subgroups":phase(old),
                  "difference_selected_minus_reference":ci},
       "form_shift_diagnostic":shift_stats,
       "promotion_gate":"Must not be worse on winner Brier and total MAE; at least one improvement with date-cluster 95% CI entirely below zero",
       "verdict":verdict,
       "limitations":["Source historical source corrections do not reproduce pretip availability",
                      "No roster-change labels, player injury data or last-5 change-point labels: subgroup phase is not a true form-shift test",
                      "Winner comparison reuses same development fitted coefficient family but does not directly run the private frozen model file",
                      "Season-level league stabilizer is previous-season league baseline even when rho=0; TEAM-specific prior is zero",
                      "This is research, not live or production candidate; no Model C parameters or public forecasts changed"]}
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    def percent(x):return f"{x*100:.2f}%"
    v=comparisons
    lines=["# NBA Match Intelligence — No Prior / Form Challenger Study",
      "", "**Isolated, no production change.**","",
      "Source: 4,895 accepted games across 2022–23 to 2025–26. Eight independent core fields, full-game exclusion.",
      "No 2025–26 result was used to select a candidate.","",
      "## 2024–25 validation (selection only)","",
      "| Architecture | Accuracy | Winner Brier | Margin MAE | Total MAE | Selection score |",
      "|---|---:|---:|---:|---:|---:|"]
    for cf in CONFIGS:
        d=v[cf["id"]]; s=d["validation"]
        lines.append(f"| {cf['id']} | {percent(s['accuracy'])} | {s['brier']:.4f} | {s['margin_mae']:.2f} | {s['total_mae']:.2f} | {d['validation_selection_score']:.4f} |")
    lines.extend(["",f"**Selected before holdout:** {selected_id}","","## 2025–26 holdout (never used for selection)","","| Metric | Frozen-C architecture replay | Selected challenger |",
         "|---|---:|---:|",f"| Accuracy | {percent(oldsc['accuracy'])} | {percent(newsc['accuracy'])} |",
         f"| Brier | {oldsc['brier']:.5f} | {newsc['brier']:.5f} |",
         f"| Margin MAE | {oldsc['margin_mae']:.3f} | {newsc['margin_mae']:.3f} |",
         f"| Total MAE | {oldsc['total_mae']:.3f} | {newsc['total_mae']:.3f} |",
         "",f"**Parity:** {result['reference_reproduction_parity']}. **Decision:** {verdict}.",
         "", "## Paired uncertainty (selected minus baseline; lower is better)","",
         "| Metric | Mean diff | Date cluster 95% CI |","|---|---:|---:|"])
    for idx,name in enumerate(ci["metrics"]):
        a,b=ci["date_cluster_95ci"][idx]
        lines.append(f"| {name} | {ci['selected_minus_reference'][idx]:+.4f} | [{a:+.4f}, {b:+.4f}] |")
    lines.extend(["","## Exploratory pregame form-shift stress test (NOT model selection)","",
         shift_stats["definition"],"",
         "| Method | n | Accuracy | Brier | Total MAE |","|---|---:|---:|---:|---:|"])
    for key,label in (("model_c","C reference"),("selected_challenger",selected_id),("recent5_challenger","Recent 5 only")):
        sc=shift_stats[key]
        lines.append(f"| {label} | {sc['n']} | {percent(sc['accuracy'])} | {sc['brier']:.4f} | {sc['total_mae']:.2f} |")
    lines.extend(["","This last subgroup is exploratory and does NOT authorize promotion. It is not an injury/roster change dataset.",""])
    lines.extend(["","Promotion threshold was set before reading holdout results. We only consider changing production if uncertainty and performance support it.",
      "No roster/injury labels were used; the result does not yet prove specific form-change responsiveness.",
      "Previous-year team prior is removed only if rho=0; a league-level prior remains for stabilization.",
      "Source attribution: BoxScore Lab (CC BY 4.0) + sportsdataverse-data ESPN-origin schedule and team box scores."])
    MD.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({"verdict":verdict,"selected":selected_id,
          "baseline":oldsc,"challenger":newsc,"difference":ci,
          "report_path":str(REPORT),"parity":parity},indent=2))
if __name__=="__main__":evaluate()
