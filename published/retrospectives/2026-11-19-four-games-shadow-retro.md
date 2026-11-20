# NBA Match Intelligence — 19 November 2026 SHADOW Retrospective

**Audited at (UTC): 2026-11-20T15:56:57.580Z.** Four NBA-local 2026-11-19 regular-season games; all FINAL in regulation; NBA Cup 0. Finished Türkiye morning 20 November.

## Original immutable pretip references
- [Before-model analyst independent view](../forecast_locks/2026-11-19-pre-model-independent-analyst-first-view.json) at 2026-11-19T19:09:59.233Z.
- [Frozen Model C numbers](../forecast_locks/2026-11-19-four-games-model-c-frozen-shadow.json) at 2026-11-19T19:14:57.080Z.
- [Final independent analyst review](../forecast_locks/2026-11-19-post-model-independent-analyst-reviewed-shadow.json) at 2026-11-19T19:16:19.553Z.
- [Pregame market source audit](../forecast_locks/2026-11-19-pretip-ou-source-audit-unverified.json) at 2026-11-19T19:17:49.825Z (**no verified quotes or analyst O/U directions**, 0/4 coverage).
- Frozen code SHA-256 `b6efd52df74f540c3bda711cd37a372e1ae7cbdbda134579c4c43bc7ff1eafef`; param SHA-256 `259b0dcc561c2f0400b04d9b19aba59eef53973ba06075f5db97a73497d1c640`; accepted data path `published/accepted_candidates/2026-11-18-accepted-fef5b8784747.json` and SHA-256 `fef5b8784747841a24bd15cb80ccd61716753850bad3473dbeb411f2938f6b30`. No model changes.

## Performance
- Frozen C winner: **3/4 (75%)**; summed favorite predicted wins 2.827 of four. Home-win Brier **0.140815**.
- Home-minus-away margin **MAE 7.60 points**. Full-game incl OT total **MAE 10.99 points**; mean signed actual minus model total **-2.10 points**.
- Final analyst winner **3/4 (75%)**; zero abstentions, zero contrarian leans. Final MEDIUM 1/1 and LOW 2/3. Initial MEDIUM 2/2, initial LOW 1/2; Memphis explicitly reduced from MEDIUM to LOW pretip.
- Independent contribution to winner choices **not identified**, since all four agreed with C. A retrospective 3/4 doesn't prove any model calibration.
- Official graded total O/U **N/A (0/4)**: no independently verified main OT included market price/odds and separate analyst pretip selection. Indexed candidates not graded.

Scores away–home, margin home minus away. Four quarters, zero OT.

| Match | FINAL | Model winner | Final analyst | Home margin predicted → actual | Full-game total predicted → actual |
|---|---:|---|---|---|---|
| GSW@MEM | 98–126 | MEM 63.08% ✓ | MEM ✓ (LOW) | 4.16 → 28 | 232.16 → 224 |
| POR@MIL | 124–114 | POR 77.56% ✓ | POR ✓ (LOW) | -9.64 → -10 | 228.59 → 238 |
| NYK@MIN | 102–99 | MIN 58.99% ✗ | MIN ✗ (LOW) | 2.83 → -3 | 219.01 → 201 |
| LAC@SAS | 112–124 | SAS 83.11% ✓ | SAS ✓ (MEDIUM) | 12.38 → 12 | 227.63 → 236 |

Official NBA game score URLs: [GSW@MEM](https://www.nba.com/game/gsw-vs-mem-0022600270) · [POR@MIL](https://www.nba.com/game/por-vs-mil-0022600271) · [NYK@MIN](https://www.nba.com/game/nyk-vs-min-0022600272) · [LAC@SAS](https://www.nba.com/game/lac-vs-sas-0022600273). Independent [Land of Basketball](https://www.landofbasketball.com/results/2026_2027_nov_scores.htm), [American Bball](https://americanbball.com/games/season/81/2026-27?page=1).

## Basketball hypotheses: as-of pretip, not invented after the scores

### Memphis 126–98 Warriors
**Before**: Memphis winner chosen; GSW Curry/Butler reported absent in prior preview, but team's actual game-day injury report at the morning capture was NOT YET SUBMITTED. Warriors' half-court initiation weakness was an opponent-specific signal. Independent first view MEM MEDIUM → final pretip MEM LOW due unresolved availability and back-to-back.
**After**: Warriors 5/29 3P (17.2%), Memphis 15/35 3P (42.9%); 30-point difference from threes, 20 vs 34 assists. Expected MEM +4.16 versus actual +28 creates night's largest margin error **23.84**; winner still correct. Multiple hypotheses (availability, shooting variance, fatigue) remain causally indistinguishable. [Warriors team recap](https://www.nba.com/warriors/news/gameday-recap-20261119).

### Knicks 102–99 Minnesota
**Before**: Model MIN 58.99%, analyst MIN LOW. The specific pretip counterargument anticipated Karl-Anthony Towns' floor spacing pulling Gobert away and Brunson's closing-ball-handler role.
**After**: Towns 22/12 (17 first-half points), Brunson 21/7. New York nearly squandered a 19-point third-quarter lead and scored nothing final 3:26, while Minnesota missed late opportunities. Outcome supports possibility of the pretip *counterargument*, not proof that spacing alone caused it. Final total **201** vs forecast **219.01** (absolute miss **18.01**, largest total miss). [NBA recap](https://www.nba.com/game/nyk-vs-min-0022600272).

### Portland 124–114 Milwaukee
**Before**: POR chosen LOW with Lillard + Jrue Holiday guard-creation routes, despite Avdija and Camara QUESTIONABLE.
**After**: Lillard 33 points, Holiday 22, Scoot Henderson 27. Camara played (18) but Avdija sat (injured). An unanticipated secondary creator scoring surge helped bridge availability uncertainty. Expected POR margin +9.64 vs actual +10, absolute miss **0.36**. Twenty lead changes/eight ties caution against equating exact final spread with stable game domination. [NBA game](https://www.nba.com/game/por-vs-mil-0022600271).

### Spurs 124–112 Clippers
**Before**: SAS chosen MEDIUM; Wembanyama defense and Spurs ball creation against LAC lineup; counterargument Brook Lopez threes pulling Wemby from the paint.
**After**: Wembanyama 32 points/11 rebounds, Castle 21 points/12 assists; Lopez 23 with 5/7 three-pointers, Garland 23. Clippers 17/42 from 3. The predicted Spurs advantage materialized but the opposing stretch-big mechanism **also occurred**. Model expected SAS +12.38 vs final +12, absolute error **0.38**. [NBA game](https://www.nba.com/game/lac-vs-sas-0022600273).

## Governance
- Original SHA-verified Model C outputs reused exactly; nothing recalculated from postgame stats to impersonate pregame predictions.
- First analyst lean and final lean recorded before tip, source provenance checked; current-day unavailable statuses not retroactively reclassified.
- No new model calibration or production approval from four games, and no official O/U grade without true pretip markets.
- Append-only report: original lock files untouched.
