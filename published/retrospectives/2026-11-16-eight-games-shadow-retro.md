# NBA Match Intelligence — 2026-11-16 SHADOW Retrospective

**NBA-local date:** 2026-11-16 · **Audit time:** 2026-11-17 10:11:35 UTC · **Eight pretip-locked games**, all regular-season / NBA Cup none / 0 OT.

## Locked inputs, no hindsight

[Read original model + independent analyst lock](../forecast_locks/2026-11-16-eight-games-model-c-analyst-shadow.json) (commit `a4ed90de5897ec4d5b5dde629553cf58ccfb483a`), written before first tipoff at `2026-11-16T20:56:47Z`, analyst lock at `2026-11-16T20:58:52Z`. Frozen model SHA `b6efd52df74f540c3bda711cd37a372e1ae7cbdbda134579c4c43bc7ff1eafef`, frozen params SHA `259b0dcc561c2f0400b04d9b19aba59eef53973ba06075f5db97a73497d1c640`, snapshot `published/accepted_candidates/2026-11-15-accepted-cdb31d297c6b.json` SHA `cdb31d297c6bf476dfa2a72779d49b3d4a389b47120f8f68f551d5c39ed44b8a`. No model edits, recalibration, or later pregame reconstructions.

[Pregame O/U source candidates](../context_notes/2026-11-16-pretip-ou-source-candidates-not-verified.json) were **not verified pretip market selections**, hence official O/U N/A, coverage 0/8, no quoted-line scoring and no fake win rate.

Final scores independently checked against [NBA official schedule](https://www.nba.com/schedule/2026), [RealGM 16-Nov NBA result list](https://basketball.realgm.com/schedules/2026-11-16/NBA), [Land of Basketball](https://www.landofbasketball.com/results/2026_2027_nov_scores.htm). Each finished in regulation (no OT).

## Eight results and locked pretip forecasts

Scores = away–home. Margin always **home minus away**. Model total means complete game including any OT.

| Fixture | Final | Frozen C winner | Expected home margin → actual | Expected total → actual | Locked analyst winner |
|---|---|---|---|---|---|
| ORL@BOS | 115–105 | BOS 83.26% ✗ | 12.47 → -10 | 220.34 → 220 | BOS ✗ |
| CHI@CLE | 115–126 | CLE 80.38% ✓ | 10.96 → +11 | 240.24 → 241 | CLE ✓ |
| MEM@WAS | 136–120 | MEM 74.47% ✓ | -8.32 → -16 | 235.61 → 256 | MEM ✓ |
| PHI@BKN | 135–123 | PHI 66.59% ✓ | -5.36 → -12 | 224.23 → 258 | ABSTAIN |
| HOU@MIA | 110–128 | HOU 64.03% ✗ | -4.48 → +18 | 234.27 → 238 | ABSTAIN |
| GSW@NOP | 94–115 | GSW 68.20% ✗ | -5.93 → +21 | 236.86 → 209 | ABSTAIN |
| POR@MIN | 98–106 | MIN 65.42% ✓ | 4.95 → +8 | 228.28 → 204 | MIN ✓ |
| PHX@DEN | 117–105 | DEN 68.83% ✗ | 6.16 → -12 | 232.16 → 222 | DEN ✗ |

## Scoring, separated

- Frozen Model C winner: **4/8 (50.0%)**; expected winning picks sum **5.71/8** (an expectation, not a guarantee). Home-win **Brier 0.297130**.
- Home-minus-away margin **MAE 13.43** points; full-game incl-OT total **MAE 15.16** points. Mean total actual minus frozen prediction **-0.50** points.
- Independent ANALYST_LEAN **3/5 (60%)**; one LOW **1/1** and four MEDIUM **2/4**, three explicit ABSTAIN (PHI@BKN, HOU@MIA, GSW@NOP). Of abstentions, baseline 1 WIN + 2 LOSS. No contrarian decisions tonight; analyst incremental predictive improvement **not identifiable**.
- Official market O/U selections **N/A**, verified coverage **0/8**. Eight pretip researched bookmaker price *candidates* did not pass direct-source quote verification, so not scored. Cup count 0.
- All statistics reflect the frozen pretip locks, not reconstructed postgame odds or postgame numerical forecasts.

## Selective notes — separate what was known before tip from observations

### Golden State @ New Orleans (GSW 94, NOP 115)
**Before:** GSW baseline 68.20% and star absences Curry/Butler/Moody/Porzingis known. Independent analyst **abstained** because replacement impact not validated. **After:** Pelicans led 35–11 after Q1; Golden State shot 11/46 3P (23.9%), Fears recorded 19/10/10 triple-double. Model margin from −5.93 to actual +21 (absolute error 26.93), total 236.86 versus 209 (absolute error 27.86). Mechanisms consistent with missing creators and shooting fluctuation, **not established causal breakdown**. Sources: [NBA](https://www.nba.com/game/gsw-vs-nop-0022600251), [AP/CBS](https://qa.img.cbssports.com/nba/gametracker/recap/NBA_20261116_GS%40NO/).

### Orlando @ Boston (ORL 115, BOS 105)
**Before:** frozen Boston favorite **83.26%**, analyst agreed MEDIUM. Orlando's Banchero OUT noted but offensive alternatives Wagner/Bane explicitly listed in counterargument. **After:** Orlando 40-point Q4, Bane 15 Q4 points, Magic 54–32 advantage in paint; Celtics were on the second night of a back-to-back after the Dallas game. Pregame lean **did not adequately emphasize schedule/fatigue**, but whether this changed the outcome cannot be identified from one match. Model margin +12.47 to actual −10, absolute error 22.47. Sources: [NBA game](https://www.nba.com/game/orl-vs-bos-0022600245), [Boston team analysis](https://www.nba.com/celtics/news/game-recap-keys-20261116).

### Phoenix @ Denver (PHX 117, DEN 105)
**Before:** Denver model 68.83%, analyst DEN MEDIUM, citing home advantage and Phoenix back-to-back. Counterargument included Phoenix shooting and Denver non-elite defense. **After:** Suns out-rebounded Nuggets 60–42, won second-chance points 22–11 and bench scoring 42–19; Denver recorded 17 turnovers. These are observed game outcomes, not proven a priori matchup edge or repeatable weakness. Model +6.16 margin to actual −12, absolute error 18.16. Source: [AP/CBS](https://www.cbssports.com/nba/gametracker/recap/NBA_20261116_PHO%40DEN/).

### Philadelphia @ Brooklyn (PHI 135, BKN 123)
**Before:** frozen PHI favorite 66.59%; analyst **ABSTAIN** for LeBron OUT, Embiid QUESTIONABLE, back-to-back and unverified replacement minutes. **After:** Embiid played and scored 37, Jaylen Brown 31. Model correctly forecast PHI winner but missed 258 total versus frozen 224.23 (33.77-point total error, night's largest). Q was not OUT in our pretip information and abstention should not be retroactively regarded as a wrong pick. Source: [NBA official recap](https://www.nba.com/game/phi-vs-bkn-0022600248).

## Decision and next steps

Boston and Denver are genuine wrong model/analyst outcomes; Houston and Golden State were wrong baseline choices where the independent analyst correctly declined a positive directional position, without proving extra statistical skill. Cleveland's expected +10.96 versus actual +11, and total 240.24 versus 241 are remarkable single-game fits, not evidence of global perfect calibration.

No single-night evidence proves an algorithmic blind spot, excess confidence or an injury coefficient. Track as-of injury and replacement-minute evidence and competing rest/shooting hypotheses prospectively. Preserve frozen Model C code/params, all original records, and retrospective independence.

**Audit status:** SHADOW postgame, appended only; no production promotion.
