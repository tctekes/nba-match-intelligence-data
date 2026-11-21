# NBA Match Intelligence — No Prior / Form Challenger Study

**Isolated, no production change.**

Source: 4,895 accepted games across 2022–23 to 2025–26. Eight independent core fields, full-game exclusion.
No 2025–26 result was used to select a candidate.

## 2024–25 validation (selection only)

| Architecture | Accuracy | Winner Brier | Margin MAE | Total MAE | Selection score |
|---|---:|---:|---:|---:|---:|
| C_reference_reconstruction | 66.50% | 0.2104 | 11.02 | 14.93 | 1.6032 |
| A_no_team_prior_k20 | 66.18% | 0.2121 | 11.12 | 15.09 | 1.6212 |
| B_no_team_prior_k10 | 66.34% | 0.2116 | 11.12 | 15.08 | 1.6191 |
| C_no_team_prior_k5 | 65.69% | 0.2116 | 11.13 | 15.10 | 1.6217 |
| D_no_team_prior_recent5_k5 | 64.22% | 0.2247 | 11.63 | 15.47 | 1.7398 |

**Selected before holdout:** B_no_team_prior_k10

## 2025–26 holdout (never used for selection)

| Metric | Frozen-C architecture replay | Selected challenger |
|---|---:|---:|
| Accuracy | 68.58% | 68.41% |
| Brier | 0.20493 | 0.20480 |
| Margin MAE | 11.420 | 11.445 |
| Total MAE | 15.294 | 15.529 |

**Parity:** PASS. **Decision:** NO_PROMOTION_KEEP_FROZEN_C.

## Paired uncertainty (selected minus baseline; lower is better)

| Metric | Mean diff | Date cluster 95% CI |
|---|---:|---:|
| brier_difference | -0.0001 | [-0.0026, +0.0024] |
| margin_mae_difference | +0.0253 | [-0.0768, +0.1306] |
| total_mae_difference | +0.2347 | [+0.1096, +0.3596] |

## Exploratory pregame form-shift stress test (NOT model selection)

At least one team had pregame absolute delta >=10 net rating pts/100 between most recent 5 and previous 5 league games; minimum 10 pregame games

| Method | n | Accuracy | Brier | Total MAE |
|---|---:|---:|---:|---:|
| C reference | 504 | 68.85% | 0.2063 | 15.02 |
| B_no_team_prior_k10 | 504 | 69.05% | 0.2066 | 15.41 |
| Recent 5 only | 504 | 59.52% | 0.2325 | 15.68 |

This last subgroup is exploratory and does NOT authorize promotion. It is not an injury/roster change dataset.


Promotion threshold was set before reading holdout results. We only consider changing production if uncertainty and performance support it.
No roster/injury labels were used; the result does not yet prove specific form-change responsiveness.
Previous-year team prior is removed only if rho=0; a league-level prior remains for stabilization.
Source attribution: BoxScore Lab (CC BY 4.0) + sportsdataverse-data ESPN-origin schedule and team box scores.
