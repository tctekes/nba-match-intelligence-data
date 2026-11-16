# NBA Match Intelligence 1.0 — 2026-11-15 eight-game SHADOW retrospective

**Postgame audited:** 2026-11-16 07:09:17 UTC · **NBA-local game date:** 2026-11-15 · **Status:** append-only SHADOW retrospective, NOT production.

## Audit and lock provenance

Original [frozen Model C + ANALYST_LEAN pretip lock](../forecast_locks/2026-11-15-eight-games-model-c-analyst-shadow.json), [market unverified overlay](../forecast_locks/2026-11-15-nba-ou-market-unverified-overlay-v2.json), and [timestamped pretip injury-source correction](../forecast_locks/2026-11-15-2347tsi-injury-source-correction-v1.json) were read **before** inspecting game scores. No earlier locks or model parameters were changed.

- Model pretip lock: `2026-11-15T20:40:26Z`; analyst `2026-11-15T20:42:45Z`.
- Snapshot: `published/accepted_candidates/2026-11-14-accepted-d66848107276.json`, SHA-256 `d66848107276304def5e287b548cd5b972768fff17c7778cd54f7380c36c10da` (188 raw, 186 accepted, 2 excluded).
- Frozen code SHA-256: `b6efd52df74f540c3bda711cd37a372e1ae7cbdbda134579c4c43bc7ff1eafef`. Frozen params SHA-256: `259b0dcc561c2f0400b04d9b19aba59eef53973ba06075f5db97a73497d1c640`.
- [Independent Sunday final scores](https://craftednba.com/scores?game=0022600136), [second independent list](https://www.landofbasketball.com/results/2026_2027_nov_scores.htm), [third result list](https://www.4basketball.com/scores/nba/). [Official NBA Knicks–Raptors linescore](https://www.nba.com/game/nyk-vs-tor-0022600241) verifies **one overtime**.
- Indiana@Philadelphia was already underway when the lock was generated, so it is **outside the eight-game denominator**. All eight forecasted games are regular-season non-Cup.

## Exact frozen forecast vs final

Scores are shown away–home. Margin is **home minus away**; totals include OT.

| Game | Final (away–home) | Frozen C winner | Home-margin predicted → actual | Total predicted → actual | Independent analyst lean |
|---|---|---|---|---|---|
| LAL@PHX | 131–123 | LAL 61.14% ✓ | -3.52 → -8 | 233.08 → 254 | LAL |
| CHA@LAC | 105–113 | LAC 61.57% ✓ | +3.66 → +8 | 222.53 → 218 | LAC |
| SAS@UTA | 110–102 | SAS 87.27% ✓ | -14.96 → -8 | 230.21 → 212 | SAS |
| DAL@BOS | 94–131 | BOS 81.46% ✓ | +11.50 → +37 | 222.80 → 225 | BOS |
| NYK@TOR | 112–108 OT | NYK 56.26% ✓ | -1.96 → -4 | 221.46 → 220 | ABSTAIN |
| HOU@WAS | 147–119 | HOU 81.29% ✓ | -11.42 → -28 | 229.24 → 266 | HOU |
| ATL@MIL | 113–106 | ATL 74.69% ✓ | -8.41 → -7 | 232.04 → 219 | ATL |
| OKC@SAC | 125–103 | OKC 83.24% ✓ | -12.45 → -22 | 224.28 → 228 | OKC |

## Performance

- **Model C winner: 8/8 (100%)**. Home-win **Brier 0.083463**.
- **Home-margin MAE 8.8570** points; **full-game (OT included) total MAE 12.6039** points.
- Total signed actual minus model: **+3.2951** points per game.
- **Analyst winner: 7/7 among selections, 1 explicit abstention NYK@TOR** (Model C chose NYK and was correct). LOW 3/3, MEDIUM 4/4; no HIGH. **No disagreements with Model C in 7 decided games**, so incremental independent analyst predictive value is **NOT IDENTIFIABLE** from tonight; not "8/8 analyst".
- **Full-game Over/Under official N/A, 0/8 valid coverage**. The pretip overlay contains no independently verified main-market totals/decimals and no directions. Do not derive winning bets from later bookmaker closing lines. NBA Cup 0/8.
- Compare previous Nov 14 night: Model C winner 3/5, Brier 0.295850, margin MAE 13.6925 and total MAE 15.0851. These are only descriptive nights, not a calibration claim.

## Selective analysis — knowledge before tip vs outcomes after tip

### HOU@WAS: Largest full-game total deviation, **not a proven structural issue**

Pretip: Houston stronger on both ends versus Washington in the 186-game accepted snapshot, with known Houston rotation outs; model forecast 229.24 total and HOU by 11.42. Final: **HOU 147–119 WAS**, 266 points (**36.76 over forecast**); Houston shot **52/90 FG, 15/33 3P** and recorded **40 assists**. This supports a high-efficiency *observed* shooting night, not proof it was predictable in advance. Alternative causes: defensive matchup, realized shooting, rotation and ordinary game variance. Source: [AP/CBS](https://qa.img.cbssports.com/nba/gametracker/recap/NBA_20261115_HOU%40WAS/).

### DAL@BOS: Winner correct, final spread underestimated

Pretip: Boston C favorite **81.46%**, predicted home margin **+11.50**; Dallas back-to-back and lineup uncertainty known. Final: Boston won **131–94** (**+37**) with first quarter **42–9**, Boston **23/55** on threes vs Dallas **14/41**. Absolute margin error **25.50**, largest. Which mechanism (rest, shot variation, opponent-fit, rotations) drove how much is unknown; do not fit a rest factor based on this observation. Source: [CBS box](https://www.cbssports.com/nba/gametracker/recap/NBA_20261115_DAL%40BOS/).

### NYK@TOR: Useful abstention and OT total caveat

Pretip: model Knicks **56.26%**, expected total **221.46**, analyst **ABSTAIN** due close matchup and Scottie Barnes uncertain. Final: Knicks won **112–108 after one overtime**; regulation **95–95**, OT **17–13**. Full-game 220 implies total absolute error only **1.46**, but the OT supplied 30 points; near-exact aggregate should not be interpreted as the model forecasting overtime occurrence. Official [NBA linescore](https://www.nba.com/game/nyk-vs-tor-0022600241). Abstaining was a legitimate pretip expert decision even though Model C was correct.

### ATL@MIL: Match outcome right, not the match path

Pretip Atlanta C 74.69%, analyst ATL MEDIUM. Final Atlanta won 113–106 but overcame a **22-point Milwaukee lead**. Winner scoring is correct; the in-game game state was not predicted. No generalized clutch diagnosis from one match. Source: [AP/CBS recap](https://www.cbssports.com/nba/gametracker/recap/NBA_20261115_ATL%40MIL/).

## Confidence and methodological guardrails

The 8/8 should be celebrated as a well-called slate but not overinterpreted as evidence of model calibration or proof of improvement after the preceding 3/5 slate. The model has high-prior favorites in several fixtures; no additional player/injury or team effect is retrospectively adjusted. Hypotheses remain unproven, and pregame status and postgame observations remain separately timestamped.

Original pretip LAL/PHX player-team attribution and HOU/WAS availability errors were recorded in the original **append-only pretip correction**, not overwritten. No complete postgame per-player minutes/rotation attribution audit is claimed.

**Final:** 8/8 frozen C, analyst 7/7 chosen + one abstention, home Brier 0.083463, margin MAE 8.86, total MAE 12.60, one OT, no eligible O/U markets. No model changes, no production promotion.
