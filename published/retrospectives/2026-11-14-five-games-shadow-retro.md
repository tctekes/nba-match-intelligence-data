# NBA Match Intelligence 1.0 — 2026-11-14 SHADOW retrospective

**Postgame audit:** 2026-11-15 (Türkiye saati) · **NBA-local date:** 2026-11-14 · **Status:** append-only POSTGAME report, **NOT PRODUCTION**.

**Retrospective rules:** Original locks were read first, then independent finals. These are **not new pregame picks**. Original frozen Model C numbers, params, pregame locks, O/U quotes and separate pretip analyst revision were **not modified**.

## Source and lock integrity

- [Original Model C and analyst pretip lock](../forecast_locks/2026-11-14-model-c-analyst-shadow.json) — commit `9ceeb7afa8089b87a0a03d91a7786a964844fb3c`, generated `2026-11-14T20:06:54.375435+00:00`.
- [Original O/U v0.2 overlay](../forecast_locks/2026-11-14-nba-ou-shadow-overlay-v2.json) — commit `2eb3702e3ec20e70f36b761752b830ca1b4eb5cf`, quote capture `2026-11-14T20:15:40Z`, reviewed `2026-11-14T20:16:27Z`.
- [Separate DAL@CLE pretip analyst update](../forecast_locks/2026-11-14-2320tsi-cle-analyst-lean-revision.json) — commit `3fe173331f31fd02dacfced79a75299ce6e42592`; analyst changed from unknown to DAL / LOW before tipoff; original version retained.
- Original data `published/accepted_candidates/2026-11-13-accepted-320b7eae2cba.json`, SHA-256 `320b7eae2cbaceffba1bc4f43e5cef9ddb8cb33dc4d1f1f41da8093e5a94bd75`; 181 accepted / 2 excluded games, 30 teams / 362 team GP.
- Frozen code SHA-256 `b6efd52df74f540c3bda711cd37a372e1ae7cbdbda134579c4c43bc7ff1eafef`; frozen params SHA-256 `259b0dcc561c2f0400b04d9b19aba59eef53973ba06075f5db97a73497d1c640`; **no retuning**.
- [Official NBA final results](https://www.nba.com/schedule) checked against [independent RealGM league-date listing](https://basketball.realgm.com/schedules/2026-11-14/NBA). **Five ordinary regular-season games, all FINAL, 0 overtime**; 4-quarter game summaries corroborate regulation finishes. No Cup flags.
- No new eight-field statistical cross-source audit of postgame box scores was done, only final scores/periods independently validated.

## All five locked predictions versus finals

Margin is **home − away**, full-game total includes any OT; score is displayed **away–home**. All five games played in regulation.

| Fixture | Frozen winner | Final | Model W? | Home margin predicted → actual (abs error) | Total predicted → actual (abs error) | Latest pretip analyst | O/U locked pick → grade* |
|---|---|---|---|---|---|---|---|
| DEN@NOP | DEN 69.24% | 116–108 | ✓ | -6.30 → -8 (abs 1.70) | 240.96 → 224 (abs 16.96) | DEN ✓ (MEDIUM) | OVER 234.5 → LOSS* |
| DAL@CLE | CLE 66.38% | 117–127 | ✓ | 5.29 → +10 (abs 4.71) | 231.40 → 244 (abs 12.60) | DAL ✗ (LOW) | UNDER 231.5 → LOSS* |
| DET@MIA | DET 64.62% | 117–137 | ✗ | -4.68 → +20 (abs 24.68) | 230.73 → 254 (abs 23.27) | MIA ✓ (LOW) | OVER 228.5 → WIN* |
| BKN@MEM | MEM 76.52% | 110–129 | ✓ | 9.18 → +19 (abs 9.82) | 228.66 → 239 (abs 10.34) | MEM ✓ (MEDIUM) | UNDER 228.5 → LOSS* |
| CHI@MIN | MIN 89.38% | 117–106 | ✗ | 16.55 → -11 (abs 27.55) | 235.25 → 223 (abs 12.25) | MIN ✗ (MEDIUM) | UNDER 235.5 → WIN* |

## Performance — strictly separated

**Frozen Model C:**
- Winner **3/5 = 60.00%**.
- Home-win Brier **0.295850** (lower better).
- Home-minus-away margin MAE **13.6925 points**.
- Full-game total MAE **15.0851 points**.
- Mean signed total error (actual − model) **+3.4022 points**.
- Five-game sample is not a statistically adequate new calibration test; the largest miss is CHI@MIN, an 89.38%-favored home loss.

**Separate pretip winner analyst:** **3/5 = 60.00%**. MEDIUM **2/3** (DEN, MEM right; MIN wrong), LOW **1/2** (MIA right, revised DAL wrong). Model-vs-analyst disagreements: DET@MIA analyst MIA correct / Model DET wrong; DAL@CLE analyst DAL wrong / Model CLE correct. Latest pretip DAL@CLE revision is counted, with original null preserved; no retroactive changes.

**Full-game Over/Under data-integrity gate: OFFICIAL O/U N/A, coverage 0/5.** The pretip overlay contains 5 direction/price records but its own provenance admits quotes were obtained from web-search snippets of a **1xBet-branded mirror**; direct bookmaker-page reopening failed. This does **not** establish independently verifiable authentic pretip main-market odds as required by protocol v0.2. Do not promote to validated winning-rate metrics, even though the records exist and preceded tip.

**Provisional mechanical scoring of the five recorded lines ONLY (NOT official validated O/U):** **2 WIN / 3 LOSS / 0 PUSH = 40%**, with confidence MEDIUM **0/1**, LOW **2/4**. Model's separate raw line-direction would have been **3/5** at those same unverified lines; the only analyst/raw disagreement was BKN@MEM (analyst UNDER lost, raw OVER won). All five quoted lines are retained unchanged; no postgame alternate/closing line was substituted.

## Three basketball learning cases (outcome-informed diagnosis, never pretip knowledge)

### 1) CHI@MIN — huge high-probability upset, largest margin miss

- Frozen MIN **89.38%**, expected home margin **+16.55**, actual **−11** => absolute margin error **27.55**; full total **235.25 → 223**.
- Despite Chicago's previous-night OT game and travel problems, Chicago won. Bulls made **14/30 from three (46.7%)**, Minnesota **9/38 (23.7%)**. Chicago's **Norman Powell scored 23**, plus two 16-point bench contributions; Minnesota's **Anthony Edwards and Donte DiVincenzo had been verified OUT** pretip.
- Mechanism: model's strong Minnesota defense/Chicago-weak-defense season baseline was not enough to withstand lineup-dependent shot creation changes plus a substantial realized 3P split. The **3P outcome and 27.55-point residual** are not proof that model coefficients should change. Pregame counterargument had noted missing Edwards, but the analyst still selected MIN / MEDIUM; failure belongs to both model and qualitative layer.
- Sources: [NBA official game summary](https://www.nba.com/schedule), [AP/CBS box score & recap](https://www.cbssports.com/nba/gametracker/recap/NBA_20261114_CHI%40MIN/).

### 2) DET@MIA — correct contrarian lean, major baseline margin and total miss

- Frozen DET **64.62%**, expected home margin **−4.68**, actual MIA **+20** => absolute margin error **24.68**. Total **230.73 → 254** => absolute total error **23.27**, the largest total miss tonight.
- Pregame confirmed **Jalen Duren OUT**; separate analyst lean **MIA / LOW** for potential Giannis+Bam frontcourt matchup. Postgame [Miami official analysis](https://www.nba.com/heat/news/coups-takeaways-antetokounmpo-adebayo-size-too-much-detroit-cunningham) states Detroit played small with **John Collins at center**, sometimes matching Cade Cunningham to Bam Adebayo. **Giannis Antetokounmpo 34 points, 14 rebounds, 8 assists; Klay Thompson 26 points; Miami 14 team blocks** corroborated by [AP/CBS recap](https://www.cbssports.com/nba/gametracker/recap/NBA_20261114_DET%40MIA/).
- This supports the predeclared injury/matchup mechanism without converting DPM or a single game's box score into a numerical adjustment. Miami's 3P shooting and rim protection were additional realized outcomes, not known certainty pretip.

### 3) DAL@CLE — analyst injury narrative failed despite extensive confirmed absences

- Model CLE **66.38%** was correct (CLE **127–117**), expected margin **+5.29 → +10**. Latest pretip analyst revision switched to DAL / LOW following Mobley OUT and Mitchell/Harden/Allen Q listings.
- After tip, [AP/CBS recap](https://www.cbssports.com/nba/gametracker/NBA_20261114_DAL%40CLE/) established Cleveland played **without its usual starting five**, yet **Tyrese Proctor 24 points, 11 rebounds, 10 assists** led a bench/depth-driven win. This is an unusually instructive counterexample to automatically fading a team when several stars are missing.
- Pregame Q did **not** mean confirmed OUT at review, and the eventual absences do **not** make a pretip DAL lean retroactively correct. Rotation depth and replacement execution were underestimated. Total **231.40 → 244**; recorded UNDER 231.5 was a provisional loss.

## Additional O/U and tactical notes

- DEN@NOP: model correctly forecast Denver winner and near-correct margin (**−6.30 → −8**), but projected **240.96** total versus **224** actual. Recorded OVER 234.5 lost; [official NBA recap](https://www.nba.com/game/den-vs-nop-0022600231) notes Jokic/Murray led and the Pelicans remained competitive, but scoring did not reach the model's high full-game expectation.
- BKN@MEM: Memphis correctly won 129–110; combined 239 exceeded the recorded 228.5 line. [Box score](https://www.cbssports.com/nba/gametracker/recap/NBA_20261114_BKN%40MEM/): Memphis shot **15/35 threes** and **22/29 free throws**; Brooklyn **17/46 threes**, supporting the warning that Memphis shooting and Brooklyn defensive concession could defeat a qualitative UNDER lean. Model raw OVER would have won on that provisionally recorded line.
- These market observations are **conditional** on unverified bookmaker provenance; do not report a certified O/U hit rate or profit.

## Forward protocol, no hindsight adaptation

1. Preserve all original pretip artifacts. Recheck official injury report shortly before tip; stamp updates as new append-only files. Assess replacement minutes and opponent matchup rather than counting OUT stars mechanically.
2. For O/U, obtain and archive a **direct, authentic, timestamped named-book pretip primary full-game including OT quote** with both decimal odds. Search-engine snippets or an unreopenable mirror do not satisfy strict market admission; if unavailable use `MARKET_NOT_VERIFIED`.
3. Keep frozen Model C parameters and these five original forecasts unchanged. Log prospective opportunities to test star-absence/bench-depth and 3P volume-vs-shot variance on larger samples; no single-night fit or production promotion.

**Audit verdict:** FINAL results and model/analyst retrospective verified; bookmaker-based official O/U performance **not eligible**, while locked-line mechanical grades are preserved transparently as *provisional*. All five games and 0 OT scored. No new pregame picks created.
