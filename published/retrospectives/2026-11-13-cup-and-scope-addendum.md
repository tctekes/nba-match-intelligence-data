# 2026-11-13 NBA SHADOW retrospective — NBA Cup and user-selected discussion-scope addendum

**Date filed:** 2026-11-14 Europe/Istanbul. **POSTGAME commentary**, not a pregame forecast.  
**Original 9-game lock:** [unchanged JSON](../forecast_locks/2026-11-13-model-c-shadow.json)  
**Official 9-game retrospective:** [unchanged report](./2026-11-13-nine-games-retro.md)  
**Protocol adopted prospectively:** [NBA Cup + main-line totals](../../docs/NBA_CUP_AND_TOTALS_MARKET_PROTOCOL_V01.md)

## Correction: ALL NINE games were NBA Cup group-play games

The official [NBA November 13 schedule](https://www.nba.com/schedule?cal=November&pd=all&region=1) and [November 13 Cup stakes report](https://www.nba.com/news/emirates-nba-cup-stakes-friday-nov-13) show all nine fixtures were NBA Cup Group Play:

- NYK @ IND — East Group B
- MIL @ ORL — East Group A
- CLE @ MIA — East Group B
- ATL @ CHI — East Group C
- MEM @ NOP — West Group B
- UTA @ HOU — West Group A
- GSW @ SAS — West Group C
- POR @ SAC — West Group C
- OKC @ LAC — West Group B

**This classification was not separately surfaced in the pregame model lock or scouting context.** Preserve that omission as an audit lesson. It does NOT establish that Cup status caused the model misses.

Per [NBA Cup group rules](https://www.nba.com/news/nba-cup-101), winning matters for advancement and regulation point differential/points scored can break ties. Players on knockout-round teams may earn prize-pool allocations ([NBA Cup FAQs](https://www.nba.com/news/nba-cup-frequently-asked-questions)). These give plausible **bidirectional** motivations but no scientifically established upset adjustment. In overtime group games, points scored in overtime **do not count toward Cup tiebreakers**, while the official game score and Model C's full-game totals **DO count overtime**.

## User-focused discussion subset (exclude two games FROM THE DEEP DIVE, not from audit)

Per user request, **MEM@NOP and GSW@SAS are omitted from this conversation's highlighted retrospective**. Both nevertheless occurred on the **same official NBA-local date November 13** and were Cup matches. They remain in the locked predictions and official full-nine retrospective. No model-score rows are deleted or relabelled.

| Predefined slice | Winner correct | Home-win Brier | Full-game total MAE | Home-margin MAE |
|---|---:|---:|---:|---:|
| All 9 original Cup fixtures (official retrospective) | **5 / 9** | 0.239898 | 12.3605 | 12.8612 |
| 7-game **user discussion scope** (excluding MEM@NOP and GSW@SAS **after results**) | **3 / 7** | 0.273532 | 10.5545 | 8.1020 |

**Selection made after results, for discussion convenience only. The 7-game slice must not be used as a replacement headline accuracy or prospective model-scoring cohort.**

## User observations vs grounded evidence and alternative explanations

1. **NYK@IND (forecast NYK 71.78%; actual IND 106–104):** The Knicks had a potential game-tying last possession. [AP game recap](https://www.cbssports.com/nba/gametracker/recap/NBA_20261113_NY%40IND/) describes Towns' unsuccessful potential tying shot. Making it would have forced OT, **not guaranteed a Knicks win**. NBA Cup group stakes plausibly mattered to both teams, but a two-point result remains a probabilistic miss, not evidence for a categorical Cup adjustment.
2. **CLE@MIA (forecast CLE 53.98%; actual MIA 133–121):** User describes both as difficult to trust/“fraudulent”; this is **user scouting language**, not a verified statistical category. An operational hypothesis is higher player-availability sensitivity / late-game or game-to-game volatility. Need measurable definitions and prospective data, not a narrative verdict.
3. **ATL@CHI (forecast ATL 73.33%; actual CHI 125–117 in OT):** User suggested Bulls might be motivated to end a poor start and change the narrative. Independent [AP recap](https://www.cbssports.com/nba/news/norman-powells-33-points-lift-bulls-over-hawks-in-ot-to-end-skid/) documents an 8-game losing streak, Norman Powell's 33 (9 in OT), and Chicago's win at home. [Chicago Sun-Times](https://chicago.suntimes.com/bulls/2026/11/13/chicago-bulls-caleb-wilson-atlanta-hawks-norman-powell-josh-giddey-isaac-okoro-nic-claxton-jalen-smith) reports their recovery after giving up an 18-point lead. A “statement win” is plausible interpretation, **not verified causal evidence**. Pregame Powell availability was flagged uncertain in the timestamped context file.
4. **OKC@LAC (forecast OKC 66.49%; actual LAC 113–112):** OKC absences were noted in the pregame scouting file. [AP game account](https://www.chron.com/sports/article/clippers-overcome-40-points-from-sga-and-use-late-22530453.php) documents Clippers' 7–0 closing burst and SGA's missed potential winner. Look for changes in crunch-time creation with absent personnel; do not claim permanent “OKC is poor in clutch”.
5. **MIL@ORL, UTA@HOU, POR@SAC:** They remain part of this seven-game discussion. Correct winners were ORL, HOU, POR; their different margin/total errors deserve separate evaluation instead of simply tallying winners.

## O/U retrospective eligibility

For 2026-11-13, the original model **predicted an exact expected total**, but did **NOT** lock a pregame sportsbook main total line, O/U decimal prices, or an actual over/under selection. Therefore the official O/U performance for this slate remains **N/A**, not 0/9, 5/9, or any hindsight-based score. Historical market quotations (if sourced later) are retrospective context only, not prospective hits. The **new O/U protocol begins with future pretip locked forecasts**.

## Future validation questions

- Do NBA Cup nights empirically produce different **winner calibration**, underdog rates, full-game total/margin error after controlling for teams, opponent, personnel, home, rest, point-differential incentive and date? Use large samples, declare analysis ahead of time.
- Are **post-loss bounceback or losing-streak breaks** associated with model residuals or simply hindsight narratives?
- Is **starter/finisher availability** an independent predictive variable after season-average strength is included?
- Does **OT vs regulation in Cup** change apparent scoring error? Always preserve official full-game target separately from Cup group tie-break accounting.
- Does a **prospectively selected** over/under direction on a verifiable, named European bookmaker's main pretip total line improve upon chance and the market after enough samples? Do not optimize thresholds from the same evaluation sample.

**Frozen Model C unchanged. Original full-nine locked predictions unchanged. No production pointer promoted.**
