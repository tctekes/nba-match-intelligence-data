# NBA Match Intelligence 1.0 — November 13, 2026 SHADOW Retrospective

**Postgame research date:** 2026-11-14 Europe/Istanbul  
**Status:** RETROSPECTIVE, retrospective-only; frozen parameters and locked forecasts are not modified  
**Original exact pregame forecast:** [2026-11-13 Model C v0.1 immutable SHADOW lock](../forecast_locks/2026-11-13-model-c-shadow.json)  
**Pregame context file (sourced, *preliminary*, not converted into model numbers):** [2026-11-13 scouting notes](../context_notes/2026-11-13-nba-pregame-basketball-context.md)

## Evidence and reproducibility

- Fixed 9 forecasts were taken from the linked locked JSON recorded 2026-11-13T18:59:10.756603+00:00 (**21:59:10 TSİ**), before tip-off.
- Frozen model: Model C v0.1, code SHA-256 `b6efd52df74f540c3bda711cd37a372e1ae7cbdbda134579c4c43bc7ff1eafef`; params SHA-256 `259b0dcc561c2f0400b04d9b19aba59eef53973ba06075f5db97a73497d1c640`.
- Locked snapshot: `published/accepted_candidates/2026-11-12-accepted-5aabf4a8efe0.json`, SHA-256 `5aabf4a8efe0c11fe4ec998b9167b1d33eff255a15a5ebbf453889e9a9100db4`; accepted games = 172, excluded games = 2, source through 2026-11-12.
- The 9 finals were cross-checked against [November 13 complete scores (NBA Games Hub)](https://nbagameshub.com/nba-schedule/?month=2026-11) and [Land of Basketball November results](https://www.landofbasketball.com/results/2026_2027_nov_scores.htm) for the eight displayed there. The ninth LAC–OKC final 113–112 also confirmed by the [CBS Sports game recap](https://www.cbssports.com/nba/gametracker/recap/NBA_20261113_OKC%40LAC/) and the [Associated Press report](https://www.chron.com/sports/article/clippers-overcome-40-points-from-sga-and-use-late-22530453.php).
- Only ATL@CHI reached **one overtime**. Every total and margin score uses official **full-game including OT**. This is the original model target. No result has been filtered from the scoring.
- Box-score / rotation explanations are scoped to individually cited game reports; **no full independent 8-field box-stat re-audit was performed as part of this postgame retrospective**.

## All nine outcomes and absolute point errors

Home margin = home minus away. Winner probability = locked pregame winner's probability. Full game total including overtime.

| Away @ home | Frozen winner (%) | Final away–home | Winner? | Home margin predicted → actual | Margin absolute error | Total predicted → actual | Total absolute error |
|---|---|---|:---:|---|---:|---|---:|
| NYK@IND | NYK 71.78% | 104–106 | ✗ | -7.26 → +2 | 9.26 | 222.07 → 210 | 12.07 |
| MIL@ORL | ORL 74.15% | 99–107 | ✓ | 8.19 → +8 | 0.19 | 227.37 → 206 | 21.37 |
| CLE@MIA | CLE 53.98% | 121–133 | ✗ | -1.24 → +12 | 13.24 | 236.83 → 254 | 17.17 |
| ATL@CHI | ATL 73.33% | 117–125 (OT) | ✗ | -7.86 → +8 | 15.86 | 239.50 → 242 | 2.50 |
| MEM@NOP | MEM 60.73% | 142–111 | ✓ | -3.39 → -31 | 27.61 | 238.18 → 253 | 14.82 |
| UTA@HOU | HOU 88.34% | 118–125 | ✓ | 15.74 → +7 | 8.74 | 227.49 → 243 | 15.51 |
| GSW@SAS | SAS 69.98% | 85–123 | ✓ | 6.58 → +38 | 31.42 | 230.54 → 208 | 22.54 |
| POR@SAC | POR 78.11% | 120–107 | ✓ | -9.89 → -13 | 3.11 | 231.74 → 227 | 4.74 |
| OKC@LAC | OKC 66.49% | 112–113 | ✗ | -5.32 → +1 | 6.32 | 224.47 → 225 | 0.53 |

## Primary metrics

| Measure | 2026-11-13 (9 games) | Explanation |
|---|---:|---|
| Winner accuracy | **5/9 (55.56%)** | 4 upsets against locked favourites |
| Home-win Brier (lower is better) | **0.239898** | 9-sample mean (predicted home-win probability − actual home result)^2 |
| Winner log loss (lower is better) | 0.664656 | Natural log, home/away direction aligned |
| Total MAE | **12.3605** | 111.2446 total absolute error / 9 |
| Home-minus-away margin MAE | **12.8612** | 115.7505 margin absolute error / 9 |
| Mean signed total error (actual − forecast) | -1.1323 | Averages can cancel offsetting errors |
| Overtime games | **1/9** | ATL@CHI, includes OT in all scored metrics |
| Locks with favourite >=70% | **3/5 correct** | NYK and ATL failed; MIL, UTA, POR won |

No accuracy or calibration conclusion should be made from any single game night. The historical holdout (2025–26) included 1222 games; these 9 are not a new holdout. The 13-game combined SHADOW descriptive aggregate including November 12 (4 for 4) is: 9/13 winners, 69.23%; home-win Brier 0.204067; total MAE 16.1104; margin MAE 12.8470. This tiny descriptive aggregate is not statistical validation.

## NBA analyst review — useful mechanics, not retrospective fitting

1. **NYK@IND: Knicks 71.78% lost by 2.** Indiana had a real late defensive stand, and New York missed a final possible tying jumper. Pacers official recap notes Indiana had a 13-point lead in Q4 before NYK's rally, and injured/limited Aaron Nesmith was made available before the match. Source: [official Indiana Pacers Nov 13 rewind](https://www.nba.com/pacers/news/instant-rewind-pacers-106-knicks-104-nba-cup). Team-strength mismatch alone misses the outcome, but a single possession ending should not motivate an instant -20pt probability revision.
2. **ATL@CHI: Hawks 73.33% lost in OT.** Chicago's Norman Powell scored **33**, including **9 in overtime**, while Josh Giddey logged **14 assists, 10 rebounds**. The pregame scouting file explicitly flagged Powell as questionable, not OUT. Hypothesis: availability and immediate top-scorer contributions could challenge a season-average-only prior. Need a historically available lineup-status dataset and shadow-vs-context outcomes before any adjustment. Source: [AP/CBS Bulls-Hawks recap](https://www.cbssports.com/nba/news/norman-powell-leads-bulls-past-hawks-in-ot-to-snap-8-game-skid/).
3. **CLE@MIA: Model near toss-up (CLE 53.98%), Miami won by 12.** Miami's Bam Adebayo and Giannis Antetokounmpo each scored **37**; Cleveland's Evan Mobley was inactive. This is an explicitly documented example of matchup/personnel context that Model C does not directly quantify. The pregame context file had already called Mobley OUT, not a retrospective insight. Source: [AP/CBS Cavaliers-Heat recap](https://www.cbssports.com/nba/gametracker/NBA_20261113_CLE%40MIA/).
4. **OKC@LAC: Thunder 66.49% lost by 1.** Clippers won on a **7–0 closing run**; SGA scored 40 but missed the potential winner. OKC had material player absences already flagged *before tipoff*, making this a useful prospective contextual caution case. No verified numeric adjustment exists; do not claim the analyst 'corrected' the model. Source: [AP Clippers-Thunder recap](https://www.chron.com/sports/article/clippers-overcome-40-points-from-sga-and-use-late-22530453.php).
5. **GSW@SAS: Spurs winner correct, margin dramatically low.** Frozen home margin +6.58 vs actual +38; model total 230.54 vs 208. Warriors missed Stephen Curry; Spurs opened **38–14** in Q1; Stephon Castle scored **32**. Source: [CBS / AP Warriors-Spurs recap](https://www.cbssports.com/nba/gametracker/recap/NBA_20261113_GS%40SA/). Investigate player-absence effects, extreme shooting outcomes, and garbage-time changes separately; neither injury nor result is proof of direct causation.
6. **MEM@NOP: Grizzlies winner correct, margin dramatically low.** Frozen home margin -3.39 vs actual -31. Memphis made **18 threes**, New Orleans made **7**, with 10 Memphis players in double figures. Source: [official New Orleans Pelicans postgame report](https://www.nba.com/pelicans/news/grizzlies-142-pelicans-111-nba-cup-group-stage-postgame-wrap). One strong opponent-specific shooting night does not make team-average pace/efficiency parameters generally incorrect.
7. **MIL@ORL: winner and margin closely predicted; total overestimated.** Model home +8.19 vs actual +8 (error **0.19**), total 227.37 vs 206 (error **21.37**). Separately analyze offensive/defensive efficiency vs number of possessions; margin accuracy is not totals accuracy.
8. **UTA@HOU: most confident Houston winner correct but expected blowout absent.** Model Houston +15.74; actual +7. Correct winner is not the same as correct margin. Do not read an 88% probability as an 88% chance to cover +16 points.
9. **POR@SAC: risk flagged pregame but Portland won anyway.** Model Portland 78.11%, actual 13-point win; projected Portland by 9.89. The pregame personnel-warning memo was meant to prioritize investigation, not to overturn the result. Do not relabel the qualitative warning as a 'failed corrected pick'.

## Prioritized, testable hypotheses for future analysis

- **H1 — injury/rotation overlay:** Log official pretipout player statuses and realized team availability, role/usage/defensive value, and opponent scheme matchups. Run blind prospective context labels and compare error by category. Do not translate into probabilities until a challenger is calibrated and backtested.
- **H2 — confidence calibration:** Reliability diagrams, Brier, log loss and confidence-bin accuracy on a meaningful sample; inspect loss rates for 60–70%, 70–80%, 80%+ bins rather than re-tuning k_eff or rho after 9 games.
- **H3 — total vs margin separation:** Track both errors; examine low-scoring blowouts, 3P distribution, OT and garbage-time separately. Do not equate a correct predicted winner with an accurate game simulation.
- **H4 — game context:** NBA Cup flags, rest, travel, near-term opponent rematches as source-verifiable pregame variables. Previous Detroit-Washington quick-rematch hypothesis remains prospective, not established from 1–2 examples.
- **H5 — benchmark comparisons:** Freeze a pre-declared secondary challenger before future games. Keep Model C v0.1 as the untouched baseline with the same test slate.

### GO/NO-GO

**Retrospective accepted as postgame assessment; Model C v0.1 stays FROZEN.** Neither full production promotion nor coefficient changes are justified by 13 completed shadow games. This document is a *new* append-only retrospective, not a modification of the pregame lock.
