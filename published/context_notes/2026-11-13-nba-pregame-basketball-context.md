# 2026-11-13 NBA pregame basketball context — separate from immutable Model C lock

**Status:** Preliminary contextual scouting; NO numerical adjustment to frozen forecasts.  
**Context research as of:** 2026-11-13 approximately 19:00 UTC (22:00 Europe/Istanbul).  
**Base predictions / exact probabilities:** [Nine-game immutable Model C lock](../forecast_locks/2026-11-13-model-c-shadow.md).  
**Published NBA schedule:** [NBA.com November 13 games](https://www.nba.com/games?date=2026-11-13).

## Why this exists

The NBA analyst must not be just a readout of the 30-team table. Especially with only **10–12 accepted games per team** and prior-season shrinkage `n/(n+20)` on efficiency, v0.1 only weights current-season efficiency near one third. Personnel and rotation changes, especially star absence, must be investigated; but **no point-to-probability conversion** has been validated. The baseline output is already locked and will remain numerically unchanged.

The injuries below were reported by [TalkBasket's Nov 13 morning injury report](https://www.talkbasket.net/227893-nba-injury-report-giannis-thompson-listed-on-friday-november-13), [Action Network NBA injuries](https://www.actionnetwork.com/nba/injury-report) and [Read the Game's NBA-report-sourced Nov 13 game notes](https://www.readthegame.com/today?date=2026-11-13&season=2026-27). Some statuses are uncertain or may change before tipoff. Report times must not be confused with final first-five announcements.

## Matchup context — *not used to compute locked percentages*

| Fixture | Frozen-model winner / probability | Basketball and injury-context interpretation |
|---|---|---|
| NYK @ IND | NYK 71.78% | Tyrese Haliburton **OUT**; removal of Indy’s lead initiator materially affects creation/late-game structure. Aaron Nesmith questionable. Knicks advantage plausible, but this is a *sourced context*, not a second probability |
| MIL @ ORL | ORL 74.15% | Paolo Banchero **OUT**, Jalen Suggs **questionable**, Tristan da Silva **questionable**: loss of first-option creation could make the raw 74% *contextually fragile*. Milwaukee also has poor recorded efficiency, so do not invent a reversal |
| CLE @ MIA | CLE 53.98% | Evan Mobley **OUT**, Miami Giannis Antetokounmpo **probable**, Klay Thompson **questionable**. Cleveland's +1.24 projected win margin is a statistical near toss-up; lineup status is critical to interpretation |
| ATL @ CHI | ATL 73.33% | Chicago's early-season efficiency is weak. Atlanta has multiple listed rotation absences; Chicago Norman Powell is questionable. Avoid simplistic 'Hawks by 8 is guaranteed' language |
| MEM @ NOP | MEM 60.73% | Memphis Zach Edey **OUT**; New Orleans Trey Murphy III **doubtful**, Bennedict Mathurin **doubtful**. Both size/rim-pressure and perimeter creation may change |
| UTA @ HOU | HOU 88.34% | Utah Lauri Markkanen and Jaren Jackson Jr **OUT**; Houston favoured both by data and the pregame availability gap. Still, 88% is not certainty or a betting recommendation |
| GSW @ SAS | SAS 69.98% | Golden State Stephen Curry and Jimmy Butler **OUT**; San Antonio De'Aaron Fox and Devin Vassell **questionable**. The absence of a primary shot creator changes half-court offensive structure, but Spurs ball-handling availability should be rechecked |
| POR @ SAC | POR 78.11% | **Highest contextual warning among strong favourites.** Portland Ja Morant and Shaedon Sharpe **OUT**; offensive-creation load and closing lineup may change. Sacramento has its own absences. Do not present the locked 78% as injury-adjusted |
| OKC @ LAC | OKC 66.49% | Oklahoma City Jalen Williams, Chet Holmgren, Cason Wallace and Jaylin Williams **OUT**; Ajay Mitchell questionable. Clippers Brandon Ingram and Bradley Beal also out. Early-season strength alone may not capture rotations. [Reuters preview Nov 13](https://www.reuters.com/sports/basketball/thunders-visit-clippers-inspires-injury-flashbacks--flm-2026-11-13/) |

## Process rules for last-minute lineup updates

1. First verify the changed status (prefer current NBA league report and team first-five announcement); distinguish **OUT** from **Questionable**, and source time from actual tip.
2. Explain expected tactical mechanism (ball-handling, shot creation, rim protection, defensive switching, rebounding, pace), **plus counterargument** (backup fit, minutes redistribution, opponent weakness).
3. Keep original Model C probability, expected total and margin *immutable*. Do not invent an adjusted winner percentage without a separately validated quantitative approach.
4. If materially challenged, label `MODEL_C_BASELINE` vs `CONTEXT_CAUTION`, or offer an explicit *new time-stamped conditional analysis*, not an overwrite.
5. Capture contextual flags before the result to support prospective matchup-aware retrospectives. Do not assert these personnel facts caused any result without adequate evidence.

## Forecast risk labels

These are **qualitative scouting-priority flags, not calibrated statistical confidence scores**:
- **Major material availability / potential model stale-prior risk:** POR@SAC, MIL@ORL, OKC@LAC, CLE@MIA, GSW@SAS.
- **Read team schemes and recent results as needed:** NYK@IND, ATL@CHI, MEM@NOP, UTA@HOU.
- **Totals:** frozen Model C is a full-game expectation; a single number carries meaningful dispersion (historical total MAE ≈15.3 points). Do not give arbitrary over/under probabilities without an explicit line and validated residual distribution.

**No refitting; no revisions to pregame forecast lock.**
