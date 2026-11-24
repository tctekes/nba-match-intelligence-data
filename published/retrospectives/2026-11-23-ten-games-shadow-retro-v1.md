# NBA Match Intelligence — 2026-11-23 SHADOW retrospective

**Created:** 2026-11-24 13:05:18 UTC · **Scope:** NBA-local 2026-11-23, 10 pretip games · append-only SHADOW; NOT production.

## Immutable inputs read before scores

- [Frozen Model C + separate analyst](../forecast_locks/2026-11-23-ten-games-frozen-model-c-analyst-shadow-v1.json), Model C 20:35:28 UTC, analyst 20:36:52 UTC.
- [Pretip injury availability addendum](../forecast_locks/2026-11-23-2340tsi-availability-source-addendum-v1.json), 20:40:49 UTC.
- [Pretip O/U evidence audit — 0 verified](../context_notes/2026-11-23-pretip-ou-source-candidates-not-verified-v1.json), 20:40:49 UTC.
- Snapshot `f842ee5309639171a1e89af1d754115ea39e8bc10131b003873abe2572542732`, frozen code `b6efd52df74f540c3bda711cd37a372e1ae7cbdbda134579c4c43bc7ff1eafef`, frozen parameters `259b0dcc561c2f0400b04d9b19aba59eef53973ba06075f5db97a73497d1c640`.
- All pretip record timestamps **precede the relevant tipoffs**. No Cup games; 1 OT (PHX@NOP). 10/10 slate scope.
- Independent full-night scores: [AmericanBball](https://americanbball.com/games/season/81/2026-27), [Latescratch](https://latescratch.com/), [Reuters postgame roundup](https://www.reuters.com/sports/nba-roundup-tyler-herro-nets-32-bucks-top-raptors-end-13-game-skid--flm-2026-11-24/). [Official Pelicans OT confirmation](https://www.nba.com/pelicans/news/suns-123-pelicans-119-ot-jordan-poole-28-points-postgame-wrap).

## Locked projections vs 10 actual finals

Final scores are **away–home**; margins are **home minus away**; full-game totals **include OT**. Analyst selected picks only graded; null means pretip abstention.

| Game | Final | Model winner | Projected margin → Actual margin | Projected total → Actual | Analyst lean |
|---|---|---|---|---|---|
| MEM@CHA | 117–111 | MEM 63.41% ✓ | -4.27 → -6 | 224.48 → 228 | MEM (MEDIUM) ✓ |
| POR@PHI | 128–111 | PHI 51.85% ✗ | 0.58 → -17 | 227.80 → 239 | ABSTAIN (LOW) — |
| OKC@IND | 120–125 | OKC 73.07% ✗ | -7.76 → 5 | 223.58 → 245 | ABSTAIN (LOW) — |
| MIL@TOR | 116–111 | TOR 80.81% ✗ | 11.17 → -5 | 227.75 → 227 | TOR (MEDIUM) ✗ |
| BKN@MIN | 116–142 | MIN 87.89% ✓ | 15.40 → 26 | 223.12 → 258 | MIN (MEDIUM) ✓ |
| CLE@CHI | 108–122 | CLE 68.96% ✗ | -6.20 → 14 | 241.95 → 230 | CLE (LOW) ✗ |
| PHX@NOP | 123–119 (OT) | PHX 62.63% ✓ | -4.01 → -4 | 233.74 → 242 | ABSTAIN (LOW) — |
| LAC@HOU | 104–116 | HOU 79.35% ✓ | 10.46 → 12 | 230.33 → 220 | HOU (MEDIUM) ✓ |
| UTA@LAL | 94–109 | LAL 82.67% ✓ | 12.14 → 15 | 233.45 → 203 | LAL (MEDIUM) ✓ |
| SAS@SAC | 123–107 | SAS 89.12% ✓ | -16.34 → -16 | 225.56 → 230 | SAS (LOW) ✓ |

## Exact performance metrics

- **Frozen Model C:** **6/10 (60%)** winners; home-win Brier **0.230415**, home-margin MAE **8.3789**, full-game total MAE **13.7210**, signed actual minus model total bias **+3.0235**.
- **Independent analyst:** **5/7**, 3 explicit abstentions; MEDIUM **4/5**, LOW **1/2**. **0 counterleans** among selected picks; all chosen leans agreed with baseline, so incremental analyst benefit not demonstrated. On three abstained fixtures, Model C was right 1/3. Not crediting abstentions as wins.
- **Official O/U:** **N/A — 0/10 independently verified pretip bookmaker full-game main-line plus two decimal prices**; postgame closing prices and search snippets are not substitutes.
- Previous 2026-11-21 night had model 4/5 winner, total MAE 27.06 and signed total −27.06; today's 10 games total MAE 13.72, signed +3.02. This is *descriptive*, not evidence of fixed model bias. Historical holdout C total MAE 15.29, margin MAE 11.42 on 1,222 games.

## Key basketball findings (pretip facts separated from postgame)

### MIL @ TOR — expensive home-favorite error
**Pretip:** Toronto 80.81% frozen favorite, analyst TOR MEDIUM; Raptors RJ Barrett and Kawhi Leonard OUT, Bucks previously weak ORtg/DRtg. **Observed:** Bucks 116 Raptors 111; Tyler Herro scored 32 on 10/16 FG and 4/5 threes; Myles Turner scored 27. Milwaukee ended a 13-game losing streak. **Possible mechanisms:** hot opposing shot creation, lineup contribution and Raptors wing shortage. **Counterargument/limits:** 111 Raptors points is not automatically a proof that wing shortages caused the loss; these mechanisms are not causally isolated. One upset does not establish Model C overconfidence. [NBA/AP](https://www.nba.com/game/0022600290).

### OKC @ IND — independent abstention was valid risk management, not a win
**Pretip:** OKC 73.07% model favorite. Analyst ABSTAIN due unsubmitted official injury statuses and back-to-back; Shai expected return pretip addendum, not registered as confirmed OUT. **Observed:** IND 125 OKC 120, Shai scored 38, Indiana Siakam and Oubre 20 each, Indiana 15/37 from three. **Alternatives:** short OKC rotation vs opponent perimeter conversion; Shai 38 is counterevidence against erroneous "missing Shai" explanation. No proof of a repeatable model failure. [NBA blueprint](https://www.nba.com/game/okc-vs-ind-0022600289/blueprint) / [AP/CBS](https://www.cbssports.com/nba/news/pascal-siakam-pacers-hold-off-thunder-to-snap-four-game-skid/).

### BKN @ MIN and UTA @ LAL — largest total point deviations in opposite directions
**Pretip:** MIN full total 223.12; LAL full total 233.45. **Observed:** MIN won 142-116 (258, +34.88 forecast residual); McDaniels 34 on 12/16 incl 4/4 3PT. Lakers won 109-94 (203, −30.45 residual); Jazz back-to-back had poor perimeter conversion (6/32 3PT). **Hypotheses:** realized shotmaking and possession variation. **Counterargument:** these realized events need not have been individually predictable and cannot justify a new model total coefficient on this sample. [NBA MIN blueprint](https://www.nba.com/game/bkn-vs-min-0022600291/blueprint); [Utah Jazz postgame note](https://www.nba.com/jazz/news/cold-shooting-sinks-utah-jazz-in-loss-to-lakers-key-takeaways).

### SAS @ SAC — Wembanyama & Fox both out, but model correctly forecasts margin
**Pretip:** SAS 89.12% favorite, independent analyst SAS LOW because both stars were QUESTIONABLE, not confirmed OUT. **Observed:** Both were out; SAS 123-107 SAC, Castle 28/11 ast/8 reb; margin projection −16.34, actual −16. **Hypothesis:** good substitution and two-way overall strength, but no verified causal or minute-specific explanation; close numerical match does NOT prove star outs immaterial. [AP/CBS](https://www.cbssports.com/nba/news/stephon-castle-short-handed-spurs-top-kings-to-stay-8-0-on-road/).

### PHX @ NOP overtime
Phoenix 123 New Orleans 119 after one OT; full-game actual 242 vs frozen 233.74. Official Pelicans postgame confirms 109–109 regulation followed by 14–10 OT. Do NOT claim the model predicted an OT. [Official Pelicans](https://www.nba.com/pelicans/news/suns-123-pelicans-119-ot-jordan-poole-28-points-postgame-wrap).

## Verdict

**6/10 model winners, 5/7 analyst winners with 3 abstentions, Brier 0.2304, margin MAE 8.38, total MAE 13.72.** Distinguish injury-known pretip from late active/inactive outcome, avoid forced narratives. The last night did not demonstrate independent analyst uplift, a frozen C defect, or a justified recalibration.

No model parameter, old lock, or production pointer changes; no postgame backfill of market odds or supposedly prospective choices.
