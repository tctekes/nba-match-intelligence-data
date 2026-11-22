# NBA Match Intelligence — 2026-11-21 SHADOW retrospective

**Created:** 2026-11-22 06:29:42 UTC · **NBA-local game date:** 2026-11-21 · Append-only postgame, not production.

## Locked inputs before results

- [Frozen Model C lock](../forecast_locks/2026-11-21-five-games-frozen-model-c-after-recovery-shadow-v1.json) (2026-11-21 18:35:45 UTC)
- [Independent analyst first view](../forecast_locks/2026-11-21-pre-model-independent-analyst-first-view-v1.json) (2026-11-21 18:17:08 UTC)
- [Independent analyst final pretip](../forecast_locks/2026-11-21-five-games-analyst-only-final-no-go-v1.json) (2026-11-21 18:19:03 UTC)
- Snapshot SHA-256: `5a3fcbc40a26e98d878563b985a77a8e3fa533e9b7bbacf401c513d87faadc35`; code `b6efd52df74f540c3bda711cd37a372e1ae7cbdbda134579c4c43bc7ff1eafef`; params `259b0dcc561c2f0400b04d9b19aba59eef53973ba06075f5db97a73497d1c640`.
- **Six** NBA-local fixtures, **five** genuine pretip Model C locks. MIL@PHI tipped before lock, excluded from all metrics. No Cup. No OT. Scores checked using dated [Reuters recaps](https://www.reuters.com/sports/basketball/keegan-murray-plays-hero-lead-kings-past-celtics-first-home-win--flm-2026-11-22/) and [independent Nov21 results](https://www.landofbasketball.com/results/2026_2027_nov_scores.htm).

## Final vs unchanged pregame forecast

Final is **away–home**; margin is **home minus away**; full-game total includes OT. Analyst picks are the independently locked pre-model final view; no postgame amendments.

| Fixture | Final | Frozen winner (p) | Predicted margin → actual margin | Predicted total → actual total | Independent analyst |
|---|---|---|---|---|---|
| POR@NYK | 96–97 | NYK 63.22% ✓ | 4.21 → 1 | 221.03 → 193 | ABSTAIN (LOW) — |
| LAC@DAL | 100–110 | DAL 57.13% ✓ | 2.23 → 10 | 228.48 → 210 | DAL (MEDIUM) ✓ |
| MEM@MIN | 95–104 | MIN 64.58% ✓ | 4.67 → 9 | 228.69 → 199 | MEM (LOW) ✗ |
| NOP@SAS | 91–114 | SAS 88.66% ✓ | 15.98 → 23 | 233.25 → 205 | SAS (MEDIUM) ✓ |
| BOS@SAC | 96–97 | BOS 87.99% ✗ | -15.48 → 1 | 223.88 → 193 | BOS (LOW) ✗ |

## Exact metrics

- Frozen Model C winner **4/5 = 80%**, home-win Brier **0.246329**, home–away margin MAE **7.7612**, full-game total MAE **27.0649**.
- Model signed total bias (actual minus expected): **-27.0649**; all 5 scores below their own frozen total forecast. Mean prediction 227.06, mean observed 200.00. N=5 does not establish a structural total bias.
- Independent analyst **2/4** from selected winners, **1 abstention**; MEDIUM 2/2, LOW 0/2. Exactly one contrarian: Memphis @ Minnesota, **0/1 correct**; NYK abstention is not counted as a success.
- **Official O/U N/A, 0/5 coverage**; no pretip verified main full-game including OT market line and two prices, so even though actual totals were all less than the Model C total, this is **NOT 5 official UNDER wins**. No hindsight bookmaker line.
- 0/5 OT; no Cup; no postgame modifications to Model C or pretip picks.

## Selective basketball review (facts ≠ proven causes)

### 1. BOS @ SAC — 87.99% model favorite loses

**Pretip known:** Boston heavy favorite by 15.48 expected points; independent analyst Boston LOW; Tatum and White QUESTIONABLE (not OUT). SAC competitive in previous Lakers loss. **Observed:** Sacramento 97–96 Boston; both Tatum and White sat. Boston made 13/58 threes, the third quarter was 13–35, and Keegan Murray scored the decisive putback with 5 seconds left. **Alternative explanations:** unpriced role replacement, shooting variance, rebounds, clutch randomness. We cannot allocate causal shares from one result; the high probability miss is penalized by Brier (individual Brier 0.7743). [Dated Reuters recap](https://www.reuters.com/sports/basketball/keegan-murray-plays-hero-lead-kings-past-celtics-first-home-win--flm-2026-11-22/).

### 2. MEM @ MIN — independent contrarian view loses

**Pretip known:** Model C Minnesota 64.58%; independent analyst Memphis LOW, on recent road offense and MIN Edwards/DiVincenzo OUT. Counterpoint already recorded: Wolves elite defense (DRtg 101.92), Memphis Boozer OUT. **Observed:** Minnesota 104–95, Memphis held to 95; McDaniels scored 25 and Dosunmu 19; MIN won Q2 28–12, Q3 27–16. **Interpretation:** Defense was a known signal that our independent lean may have underweighted, but one result cannot establish an enduring analyst mechanism flaw. [Reuters recap](https://www.reuters.com/sports/basketball/timberwolves-deal-grizzlies-first-road-loss-this-season--flm-2026-11-22/).

### 3. Five totals — unusual single-night directional miss

**Pretip known:** Independent frozen total scores were 221.03, 228.48, 228.69, 233.25, 223.88. **Observed:** 193, 210, 199, 205, 193. Errors −28.03, −18.48, −29.69, −28.25, −30.88. **Hypotheses:** scoring efficiency, 3P variance, pace/possessions, context effects; not isolated or proven. No model parameters adjusted. Recheck repeated signed residuals across nights with adequate sample size before considering a change.

### 4. NOP @ SAS — avoid converting unknown pretip injuries into known advantages

**Pretip known:** SAS 88.66% favorite; NOP team report was officially not yet submitted, so player availability was unverified. **Observed:** SAS 114–91; Wembanyama scored 50 and grabbed 19 rebounds; Zion was a *late scratch*. These were not validated pretip facts in the lock; do not retroactively enhance the analyst view. [Reuters recap](https://www.reuters.com/sports/basketball/victor-wembanyama-posts-50-points-19-rebounds-spurs-roll-pelicans--flm-2026-11-22/).

### 5. Dallas and Knicks

Dallas beat Clippers 110–100, and the one-point Knicks win 97–96 survived the analyst abstention; both winner model choices correct. Clippers committed 16 turnovers to Dallas 9 in the [Reuters Dallas recap](https://www.reuters.com/sports/basketball/mavericks-finish-strong-hold-off-clippers--flm-2026-11-22/). An actual result does not make the previously cautious/abstaining choice wrong if its pretip evidence supported uncertainty.

## Verdict

**Good winner/margin night, bad total night, mixed analyst night.** Record and investigate without a forced explanation. Do not infer calibration or permanent overconfidence from one big upset. Neither model coefficients nor existing forecast files/production index are touched.
