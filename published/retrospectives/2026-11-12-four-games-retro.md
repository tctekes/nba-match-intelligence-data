# NBA Match Intelligence 1.0 — 2026-11-12 SHADOW Retrospective

**NBA game date:** 2026-11-12  
**Original locked forecasts (never changed):** [2026-11-12 Keel vs clean source](../forecast_locks/2026-11-12-shadow-keel-vs-clean.md)  
**Status:** POSTGAME RETROSPECTIVE, not a new forecast or a change to Model C v0.1.

## Verified finals

Independent [Basketball Reference 2026-11-12 scores](https://www.basketball-reference.com/boxscores/?day=12&month=11&year=2026) and [CBS fixture/results](https://www.cbssports.com/nba/schedule/20261112/) agree on all four final scores.

| Away @ home | Final (away–home) | Home minus away margin | Full-game total | OT |
|---|---:|---:|---:|---|
| TOR @ PHI | TOR 112 – PHI 123 | +11 | 235 | None |
| DET @ WAS | DET 144 – WAS 140 | -4 | 284 | **2OT** |
| DAL @ MIN | DAL 94 – MIN 133 | +39 | 227 | None |
| CHA @ PHX | CHA 96 – PHX 101 | +5 | 197 | None |

### Locked predictors: two separate SHADOW sets

| Metric | Keel Stats pilot | Clean Model C |
|---|---:|---:|
| Winners correctly predicted | 4 / 4 | 4 / 4 |
| Home-win Brier score (lower better) | **0.12289025** | 0.12344717 |
| Full-game total MAE, points | 25.0750 | **24.5475** |
| Home-minus-away margin MAE, points | **12.5000** | 12.8150 |

Home-win Brier = average over four games of (P(home wins) − actual_home_win)^2. For an away favourite, home probability is 1−P(away wins). **No new probabilities were fitted**.

### Per-match errors

| Away @ home | Keel projected total | Clean projected total | Actual total | Keel total error | Clean total error | Keel margin absolute error | Clean margin absolute error |
|---|---:|---:|---:|---:|---:|---:|---:|
| TOR @ PHI | 223.20 | 224.02 | 235 | 11.80 | 10.98 | 10.50 | 10.26 |
| DET @ WAS | 221.10 | 223.49 | 284 | 62.90 | 60.51 | 7.00 | 7.85 |
| DAL @ MIN | 224.80 | 226.21 | 227 | 2.20 | 0.79 | 31.20 | 31.13 |
| CHA @ PHX | 220.40 | 222.91 | 197 | 23.40 | 25.91 | 1.30 | 2.02 |

Signed home-margin targets: +11, −4, +39, +5. Full-game totals include OT because that is the original model's target definition.

## Basketball interpretation — hypotheses, not fitted adjustments

1. **DET @ WAS, 2OT:** The tied 121–121 score after regulation produced 42 overtime points, taking the final total to 284. This materially inflates full-game total error. OT is legitimately part of the frozen full-game target, so this record still scores **284**; consider reporting both OT-tagged and regulation-only *diagnostics* across a larger retrospective sample, without silently changing the target.
2. **DAL @ MIN, blowout:** Minnesota won by **39** while both models projected home winning margins close to **+8**. Winner identification alone obscures this large margin miss. [Reuters NBA roundup, Nov 13 2026](https://www.reuters.com/sports/nba-roundup-cade-cunningham-puts-up-52-points-pistons-2ot-win--flm-2026-11-13/) reports Minnesota's Anthony Edwards was absent and Bones Hyland scored 24; do not invent a causal story from these facts. Investigate injury/rotation exposure, shooting variance and pace independently, prior to any model update.
3. **PHI and PHX wins:** Both forecasts had moderate-to-low winner confidence for Philadelphia and Phoenix; do not reclassify them as high-confidence picks after they won.
4. **Keel vs clean input:** The clean model's total MAE is only **0.5275** points lower in this four-game comparison; Keel's Brier and margin MAE are marginally lower. The sample is far too small to infer which is better.

## Rules for follow-up experiments

- Preserve frozen Model C v0.1 and all past locks. Do not post-hoc change probabilities or parameters.
- Record injuries and role/rotation context as **sourced pregame** information for future games; avoid learning from unavailable or postgame-only facts.
- Accumulate nightly Brier, full-game total MAE, margin MAE; track OT flag, rest/back-to-back, material lineup absences, and margin bins. For total predictions consider pre-specified stratification by OT, but do not exclude OT results from scored totals.
- Propose challenger variants only after accumulating enough samples and defining predeclared data rules, backtest design, and a comparable holdout.
- Distinguish **Model C baseline output** from any qualitative NBA expert interpretation; never make an uncalibrated probability adjustment.

**Result:** Baseline operationally credible, no model promotion or retuning authorized by this four-game sample. Retrospective committed separately from the immutable SHADOW forecast lock.
