# NBA Match Intelligence — 18 November 2026 SHADOW Postgame Retro

**Audit UTC:** 2026-11-19T19:07:43.683Z. **12 previously locked games**, regular season, no NBA Cup classification. All source FINAL scores included. No market O/U eligible.

## Original append-only pretip records

- [First independent analyst view](../forecast_locks/2026-11-18-pre-model-independent-analyst-first-view.json): 2026-11-18T17:29:42.928Z, before model outputs.
- [Frozen C model](../forecast_locks/2026-11-18-frozen-model-c-baseline-shadow.json): 2026-11-18T17:34:52.381Z; SHA code `b6efd52df74f540c3bda711cd37a372e1ae7cbdbda134579c4c43bc7ff1eafef`, params `259b0dcc561c2f0400b04d9b19aba59eef53973ba06075f5db97a73497d1c640`; data `5e7d896690dade079cea3178d1867a40ebffa889fee9a248c37b8d12bbd84ac8`.
- [Final analyst review](../forecast_locks/2026-11-18-independent-analyst-reviewed-final-shadow.json): 2026-11-18T17:39:51.981Z.
- [Market audit](../forecast_locks/2026-11-18-nba-ou-fail-closed-market-audit-v1.json): 2026-11-18T17:42:00.951Z. No verified pretip bookmaker total, odds, and selected analyst direction; official O/U grading **N/A**.

## Results and scoring

**Model C: 5/12 (41.67%)**. Home-win Brier **0.310233**. Home−away margin MAE **13.04**. Full-game OT-included total MAE **14.80**. Actual minus forecast mean total **-2.81**.

**Independent final analyst:** 6/10 (60%), 2 abstentions. Confidence bins {"MEDIUM":{"n":4,"win":3,"loss":1},"LOW":{"n":6,"win":3,"loss":3}}. Genuine contrarian Denver and Dallas both correct **2/2**, but this small sample does not prove incremental skill. On model's 12 games, 2 abstentions maintained (MEM@CLE, DET@NOP).

| Away@Home | Final away–home | Frozen C winner | Final analyst | Expected home margin → actual | Frozen OT total → actual |
|---|---:|---|---|---|---|
| MIL@MIA | 130–137 | MIA 81.99% ✓ | MIA ✓ | 11.78 → 7 | 234.30 → 267 |
| HOU@IND | 119–104 | HOU 72.97% ✓ | HOU ✓ | -7.72 → -15 | 227.84 → 223 |
| MEM@CLE | 124–121 | CLE 56.22% ✗ | ABSTAIN — | 1.94 → -3 | 237.19 → 245 |
| PHI@ORL | 121–116 | PHI 52.04% ✓ | PHI ✓ | -0.64 → -5 | 223.97 → 237 |
| CHI@BKN | 137–107 | BKN 57.24% ✗ | BKN ✗ | 2.27 → -30 | 234.51 → 244 |
| WAS@TOR | 103–99 | TOR 80.91% ✗ | TOR ✗ | 11.22 → -4 | 231.81 → 202 |
| ATL@OKC | 117–112 | OKC 69.49% ✗ | OKC ✗ | 6.40 → -5 | 225.53 → 229 |
| DET@NOP | 122–109 | DET 77.71% ✓ | ABSTAIN — | -9.71 → -13 | 232.32 → 231 |
| GSW@DAL | 94–116 | GSW 59.17% ✗ | DAL ✓ | -2.88 → 22 | 228.24 → 210 |
| BOS@DEN | 101–105 | BOS 63.05% ✗ | DEN ✓ | -4.15 → 4 | 226.91 → 206 |
| UTA@LAL | 109–97 | LAL 84.56% ✗ | LAL ✗ | 13.21 → -12 | 236.55 → 206 |
| PHX@SAC | 128–107 | PHX 69.41% ✓ | PHX ✓ | -6.37 → -21 | 229.56 → 235 |

Final score independent comparisons: [NBA](https://www.nba.com/games?date=2026-11-18), [Probetrics](https://www.probetrics.com/nba/2026-11-18), [DeepMetrics](https://deepmetricanalytics.com/nba/schedule?date=2026-11-18), [NBA Flare](https://nbaflare.com/schedule). No game score sourced from model or prior-lock notes.

## Targeted basketball research — what was known before, observed after, and competing mechanisms

### GSW@DAL: correct independent contrarian, with plausible role logic
Pregame first-view Dallas, final Dallas LOW, versus frozen GSW **59.17%**. GSW Curry/Butler OUT and uncertain replacement burden was a real pretip mechanism. Dallas prevailed **116–94**, Flagg scored 33. [NBA final](https://www.nba.com/game/gsw-vs-dal-0022600267), [Mavs recap](https://www.nba.com/mavs/news/flagg-popped-in-33-points-as-mavs-snap-three-game-losing-streak-with-116-94-victory-over-warriors). The outcome supports the direction, but a game cannot isolate Curry/Butler causal points. Note original final analyst reduced confidence from MEDIUM to LOW, recorded before tip.

### BOS@DEN: correct Denver, but investigate explanation
Pregame first-view Denver LOW, model favored BOS **63.05%**. Pregame Jokic-versus-centers hypothesis predicted stress on Boston rim/help coverages. Denver won **105–101** after recovering a 17-point deficit, notably via Jamal Murray and DeMar DeRozan late scoring. Queta was 17/10, a real **counterexample** to a simplistic "weak Celtics center" storyline. [Boston official analysis](https://www.nba.com/celtics/news/game-recap-keys-20261118); [Denver team recap](https://www.nba.com/nuggets/news/nuggets-17-point-deficit-celtics). Correct pick does not prove the proposed center matchup was the main reason.

### UTA@LAL: biggest high-confidence upset
Frozen Lakers **84.56%**, analyst Lakers MEDIUM. Utah won **109–97**, Lakers held to 97. Pregame Lakers' extra-time match and Jazz recent Sensabaugh shooting were explicitly known. Postgame Utah's Mo Bamba hauled **16 rebounds**. This could relate to interior activity and back-to-back issues, but no robust isolated rest-effect proof. [Utah game coverage](https://www.slcdunk.com/utah-jazz-game-coverage/70821/utah-jazz-vs-los-angeles-lakers-recap-and-final-score).

### CHI@BKN: largest margin miss
Pregame BKN +2.27 home, final Chicago **137–107** (Brooklyn home −30). **Margin absolute error 32.27.** Our LOW Brooklyn matchup view on spacing/offensive boards failed. Do not invent a repeatable Brooklyn flaw or momentum diagnosis from one game.

### MIL@MIA: win correct, total badly underestimated
Miami won **137–130**; model expected full-game total **234.30**, actual **267**, absolute error **32.70**. Explainable postgame with scoring efficiency and trading runs only after validated box evidence, not a fake pretip prediction.

## Research / governance
- Frozen model SHA and forecasts never changed.
- First independent lean, post-model final lean and market selections strictly separated.
- No eligible pretip Over/Under market quotes and no official scored O/U results.
- Single night is not a Model C coefficient-recalibration trigger; review larger prospective samples, role availability and contrast hypotheses without fitting to results.
