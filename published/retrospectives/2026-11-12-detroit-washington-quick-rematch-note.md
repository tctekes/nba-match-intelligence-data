# NBA retrospective research note — DET vs WAS quick rematch

**Added:** 2026-11-13.  
**Type:** Evidence-based retrospective hypothesis; NOT a Model C adjustment.

## Confirmed facts

- Nov 9, 2026 (NBA date): WAS 111 – DET 122. [NBA official matchup history](https://www.nba.com/game/was-vs-det-0022600228).
- Nov 11, 2026: Washington also played Indiana before the Nov 12 rematch. [NBA.com Nov 12 preview](https://www.nba.com/game/det-vs-was-0022600228).
- Nov 12, 2026: DET 144 – WAS 140 (two overtimes), regulation tied **121–121**, and Detroit outscored Washington 23–19 in overtime periods. [Official NBA game](https://www.nba.com/game/det-vs-was-0022600228).
- Model C clean pregame forecast: **DET 82.13%**, expected home-minus-away margin **−11.85**, projected full-game total 223.49. Frozen in [original lock](../forecast_locks/2026-11-12-shadow-keel-vs-clean.md).
- Final home-minus-away margin = **−4**; model's margin absolute error **7.85**. Model correctly predicted the winner.
- DET Cade Cunningham posted 52 points, 11 assists, no turnovers; WAS Trae Young 37, Anthony Davis 30 and Alex Sarr 30. Young tied regulation at buzzer; AJ Dybantsa's shot tied first overtime. [CBS/AP recap](https://www.cbssports.com/nba/gametracker/NBA_20261112_DET%40WAS/).

## Research interpretation, not a causal conclusion

The user noticed Detroit had faced Washington in its previous game, while Washington faced Indiana in between: a short-spaced **rematch (3 days)**. Earlier scouting may help both teams anticipate matchups, calls, personnel and counters. The losing side may adjust more, but this is **not** an established one-sided effect.

The 82.13% model probability concerns *winning*, NOT margin or assurance of a comfortable game. This result is not evidence by itself that the win probability was numerically wrong: the 82%-favored team **won**. Overtime and clutch-shot variance made the encounter close; 2OT generated 42 extra points, explaining much of the total surprise. Do not treat one rematch as proof of an adjustment.

## Pre-register a challenger diagnostic (no update now)

1. Use date-specific historical NBA game records. Define quick rematch before looking at outcomes: same opponent inside **seven calendar days**; predeclare exact inclusivity and sample scope.
2. Record venue switch, roster changes, rest/B2B, schedule density, whether either team changed starting five, and which team won the first match.
3. Compare Model C out-of-sample winner Brier, margin absolute error and total absolute error in quick-rematch vs other games **after adjusting for team strength, opponent strength, home court and rest**. Include interaction for first-game loser and home-court switch; do not assume direction.
4. Report sample sizes, uncertainty intervals and sensitivity to 3-/5-/7-day windows; predeclare test before model tuning.
5. If a credible, repeatable lift exists on untouched chronological holdout, evaluate as **separate Model C v0.2 challenger**, retaining untouched v0.1 benchmark and prior nightly locks.

**Current action:** add quick-rematch tag to NBA analysis / retrospective playbook and watchlist only. **No probability or coefficient change authorized.**
