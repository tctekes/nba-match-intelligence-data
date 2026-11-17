# NBA Match Intelligence 1.0 — Winner Confidence & Analyst Agreement Audit

**Audit date:** 2026-11-17 (Europe/Istanbul)
**Scope:** 30 NBA games with frozen Model C v0.1 pregame forecast locks and completed retrospectives, NBA game dates 2026-11-13 through 2026-11-16.
**Status:** Descriptive exploratory audit ONLY. No recalibration, model modification, integrity allegation, or betting-performance claim.

## Sources and reproducibility

Pregame locks (use for ALL probabilities, predicted teams and analyst decisions):
- [Nov 13 — model only](../forecast_locks/2026-11-13-model-c-shadow.json)
- [Nov 14 — model + analyst](../forecast_locks/2026-11-14-model-c-analyst-shadow.json)
- [Nov 15 — model + analyst](../forecast_locks/2026-11-15-eight-games-model-c-analyst-shadow.json)
- [Nov 16 — model + analyst](../forecast_locks/2026-11-16-eight-games-model-c-analyst-shadow.json)

Finals / postgame grades only:
- [Nov 13](../retrospectives/2026-11-13-nine-games-retro.md)
- [Nov 14](../retrospectives/2026-11-14-five-games-shadow-retro.json)
- [Nov 15](../retrospectives/2026-11-15-eight-games-shadow-retro.json)
- [Nov 16 corrected v2](../retrospectives/2026-11-16-eight-games-shadow-retro-v2.json)

**Counting rules:** Predicted-winner probability (p), winner correctness based on original lock vs final. Bands are half-open: 50% <= p < 60%; 60% <= p < 70%; 70% <= p < 80%; 80% <= p <= 100%. *Analyst agrees* only where pregame analyst_lean.team explicitly equals model predicted_winner. Null/unknown means **ABSTAIN**, not disagreement; Nov 13 has **NO FORMAL ANALYST LOCK**, which is distinct from abstention. Only the original pregame lock can establish analyst choice. Corrected Nov 16 retro v2 supersedes earlier retro.

## Calibration bins — descriptive

| Predicted-winner confidence | Games | Winners correct | Actual hit rate | Mean model probability | Expected wins |
|---|---:|---:|---:|---:|---:|
| 50–<60% | 2 | 1 | 50.0% | 55.12% | 1.10 |
| 60–<70% | 13 | 8 | 61.5% | 65.63% | 8.53 |
| 70–<80% | 7 | 5 | 71.4% | 74.72% | 5.23 |
| 80–100% | 8 | 6 | 75.0% | 84.33% | 6.75 |
| **All** | **30** | **20** | **66.7%** | — | — |

The 60–<70% bin realized 8 wins vs 8.53 expected, a difference of only -0.53 wins across 13 games. All subgroup findings remain highly uncertain.

## Requested 60–<70% subset (n=13)

| NBA date | Fixture | Model pick | Model p | Analyst at pregame lock | Model result |
|---|---|---|---:|---|---|
| Nov 13 | MEM@NOP | MEM | 60.73% | No formal analyst lock | WIN |
| Nov 13 | GSW@SAS | SAS | 69.98% | No formal analyst lock | WIN |
| Nov 13 | OKC@LAC | OKC | 66.49% | No formal analyst lock | LOSS |
| Nov 14 | DEN@NOP | DEN | 69.24% | Agrees: DEN | WIN |
| Nov 14 | DAL@CLE | CLE | 66.38% | ABSTAIN (see audit inconsistency) | WIN |
| Nov 14 | DET@MIA | DET | 64.62% | Opposes: MIA | LOSS |
| Nov 15 | LAL@PHX | LAL | 61.14% | Agrees: LAL | WIN |
| Nov 15 | CHA@LAC | LAC | 61.57% | Agrees: LAC | WIN |
| Nov 16 | PHI@BKN | PHI | 66.59% | ABSTAIN | WIN |
| Nov 16 | HOU@MIA | HOU | 64.03% | ABSTAIN | LOSS |
| Nov 16 | GSW@NOP | GSW | 68.20% | ABSTAIN | LOSS |
| Nov 16 | POR@MIN | MIN | 65.42% | Agrees: MIN | WIN |
| Nov 16 | PHX@DEN | DEN | 68.83% | Agrees: DEN | LOSS |

### Analyst condition in the 60–<70% bin

| Pregame analyst label | Games | Model winners correct | Hit rate |
|---|---:|---:|---:|
| **Agrees with Model C** | **5** | **4** | **80%** |
| ABSTAIN (formal lock exists) | 4 | 2 | 50% |
| Explicitly opposes model | 1 | 0 | 0% |
| No formal analyst lock (Nov 13) | 3 | 2 | 66.7% |
| **All** | **13** | **8** | **61.5%** |

The 5 analyst-agreed matches averaged about **65.24%** model probability (expected 3.26 wins), with 4 actual wins. This difference is far too small to establish that analyst agreement improves calibration.

**Agreement strength nuance:** Of those 5 matching analyst leans, 3 were tagged **LOW** confidence (3/3 winners) and 2 were tagged **MEDIUM** (1/2 winners). There were **0 HIGH** confidence agreements in this probability bin. Matching directions are not the same thing as strong analyst endorsement. A stricter *MEDIUM-or-HIGH agreement* screen is therefore **1/2**, with no valid statistical inference. Analyst and model share some information; their agreement is not independent evidence.

**Audit exception (do not backfill or overwrite original):** For Nov 14 DAL@CLE, pregame lock `analyst_lean.team` is null (no directional lean), but the Nov 14 retrospective JSON labels the analyst lean as DAL. This audit uses the *pregame* lock: **ABSTAIN**. The discrepancy needs separate provenance correction before any analyst performance metric based on retro-only labels.

## Team view, only for predicted favorites in 60–<70% bin

| Team predicted | Correct / total | Games |
|---|---:|---|
| DEN | 1/2 | Nov 14 DEN@NOP W; Nov 16 PHX@DEN L |
| MEM | 1/1 | Nov 13 MEM@NOP W |
| SAS | 1/1 | Nov 13 GSW@SAS W |
| CLE | 1/1 | Nov 14 DAL@CLE W |
| LAL | 1/1 | Nov 15 LAL@PHX W |
| LAC | 1/1 | Nov 15 CHA@LAC W |
| PHI | 1/1 | Nov 16 PHI@BKN W |
| MIN | 1/1 | Nov 16 POR@MIN W |
| OKC | 0/1 | Nov 13 OKC@LAC L |
| DET | 0/1 | Nov 14 DET@MIA L |
| HOU | 0/1 | Nov 16 HOU@MIA L |
| GSW | 0/1 | Nov 16 GSW@NOP L |

There is **no demonstrated reliable team** here: most team rows are just one fixture. Any streak-based team shortlist is extremely overfit.

## High-confidence upset sanity check

- Nov 14 CHI@MIN: MIN **89.38%** pregame, analyst also MIN; Chicago won 117–106.
- Nov 16 ORL@BOS: BOS **83.26%** pregame, analyst also BOS; Orlando won 115–105.

These are ordinary forecast errors unless independent integrity evidence exists. An outcome contrary to an 80–90% forecast does not itself suggest match fixing.

## Important scope exclusions

Nov 12's four pilot SHADOW games were *not* blended into the 30-game main series: they were a separate Keel-vs-clean-source comparison, the clean-source calculation time was not recorded precisely, and there was no formal analyst pick lock. See [original pilot](../forecast_locks/2026-11-12-shadow-keel-vs-clean.md) and [four-game retro](../retrospectives/2026-11-12-four-games-retro.md). They can be shown separately but must not masquerade as comparable jointly-screened predictions.

## Prospective governance

1. Append new rows only when exact pretip probabilities, analyst choice (agree / oppose / abstain / no review), lock timestamps, and verified finals exist.
2. Recompute bins and separate: unfiltered baseline; analyst-reviewed; analyst-agrees; explicit disagreement; abstention; missing analyst review.
3. Report model-probability sum (expected wins), observed wins, Brier and uncertainty intervals; NEVER use mere hit rate in isolation.
4. For teams record selected favorite, opponent, home/away, sample count, pregame injury/lineup coverage, probability, outcome, calendar date; report small samples honestly. Do not label a team “safe” based on 1–2 games.
5. Test the predeclared analyst-agreement rule **prospectively** on many more games, and compare with equivalent-probability model-only cases. Do not select bands, teams, or time windows post hoc to maximize success.
6. Match-integrity work, if undertaken, must use independent sourced alerts or credible case evidence and have separate fields. **Do not classify lost favorite predictions as manipulated events.**
7. Preserve frozen Model C, original forecasts, and all previous retro artifacts. This is an audit note, not a promoted model or an automated tracker implementation.
