# NBA Match Intelligence — 2026-11-20 NBA Cup Group Play RETRO

**Audited UTC:** 2026-11-21T10:03:06.649Z. **9/9 pretip Cup Group Play games**, no OT. Original SHADOW model, initial analyst and final analyst locks read first, all final scores verified afterward. Never change frozen C coefficients.

## Original pretip sources (all before first tipoff)

- [Independent pre-model analyst view](../forecast_locks/2026-11-20-pre-model-independent-analyst-first-view-v1.json) at 2026-11-20T19:37:07.706Z, commit `a1d38926022a69bbd65553a39ec0445271e27c8e`
- [Frozen C pretip prediction](../forecast_locks/2026-11-20-nine-cup-games-frozen-model-c-shadow-v1.json) at 2026-11-20T19:40:20.195Z, commit `561d792047a73459ecf219adafe14edffc0514b6`
- [Reviewed final independent analyst](../forecast_locks/2026-11-20-nine-cup-games-independent-analyst-reviewed-v1.json) at 2026-11-20T19:41:08.085Z, commit `75814e0227f4e6752fb29a7c5d67296f7015d92d`
- [Market source audit](../forecast_locks/2026-11-20-nine-cup-games-market-source-audit-unverified-v1.json) at 2026-11-20T19:41:50.408Z, commit `01a964c57fdba2c7b8a731c65a698903c8722dc3` — 0/9 eligible markets, **official O/U retro N/A**

**Frozen SHA-256:** code `b6efd52df74f540c3bda711cd37a372e1ae7cbdbda134579c4c43bc7ff1eafef`; params `259b0dcc561c2f0400b04d9b19aba59eef53973ba06075f5db97a73497d1c640`; accepted data `228913b0a099c2444c573b80f7e36b76e590ee402ad240c71249ea5cf58e98f5`.

## Summary

- Frozen C: **6/9 (66.67%)**; home-win Brier **0.191493**; home−away margin MAE **7.42**; full-game incl OT total MAE **20.06**; mean actual−forecast total **-7.39**; assigned favorite probabilities sum **6.36**.
- Independent analyst: **7/8 (87.50%)**, **one abstention**. MEDIUM **4/4** and LOW **3/4**. Initial view **7/8**, no first/final winner choice changes. Only genuine contrarian HOU@DEN **DEN correctly selected**, whereas frozen model favored HOU; analyst abstained WAS@CHI, model incorrect.
- Cup 9/9 GROUP_PLAY. Points differential a conditional tiebreak, not an invented extra upset factor. Cup outcome does not prove causal endgame motivation.
- Verified pretip bookmaker main OT totals with paired decimal odds **0/9**; no analyst O/U picks, graded results **N/A**.

| Away@Home | Final away–home | Frozen Model C | Final analyst | Expected home margin → actual | Expected full-game OT total → actual |
|---|---:|---|---|---|---|
| CHA@ATL | 97–111 | ATL 70.53% ✓ | ATL ✓ (MEDIUM) | 6.78 → 14 | 224.55 → 208 |
| IND@CLE | 119–128 | CLE 74.85% ✓ | CLE ✓ (LOW) | 8.48 → 9 | 233.11 → 247 |
| ORL@BKN | 113–111 | ORL 62.48% ✓ | ORL ✓ (MEDIUM) | -3.96 → -2 | 225.00 → 224 |
| TOR@DET | 105–102 | DET 72.01% ✗ | DET ✗ (LOW) | 7.34 → -3 | 222.67 → 207 |
| WAS@CHI | 98–94 | CHI 64.39% ✗ | ABSTAIN (LOW) | 4.60 → -4 | 239.62 → 192 |
| NOP@OKC | 120–126 | OKC 84.48% ✓ | OKC ✓ (LOW) | 13.17 → 6 | 229.17 → 246 |
| PHX@UTA | 111–101 | PHX 62.33% ✓ | PHX ✓ (MEDIUM) | -3.91 → -10 | 229.34 → 212 |
| HOU@DEN | 124–133 | HOU 56.59% ✗ | DEN ✓ (LOW) | -2.06 → 9 | 230.67 → 257 |
| SAC@LAL | 104–106 | LAL 88.47% ✓ | LAL ✓ (MEDIUM) | 15.84 → 2 | 235.35 → 210 |

## Basketball hypothesis audit: before, after, competing evidence

### Houston @ Denver — true contrarian, but a mechanism did not occur

Model C favored Houston **56.59%**, forecast home margin **−2.06**; analyst's original and final lean were Denver **LOW**. Prematch center availability was at the heart of the case: Şengün and Adams QUESTIONABLE, Capela OUT, Jokic passing/creation against potentially undermanned Houston. **Crucial counterfact:** both Şengün and Adams played, Şengün **36:03 minutes, 28 points, 11 rebounds, 10 assists**, Adams **11:57 minutes**. Denver still won **133–124** behind Jokic's **24 second-half points** and a **23–9 closing run** in a game of **32 lead changes**. Therefore the winning contrarian does not validate the pretip shortage assumption. This is a correct directional decision but mixed evidence for the hypothesized mechanism. Model total **230.67 vs 257**, error **26.33**. [NBA box](https://www.nba.com/nuggets/game/0022600050-rockets-vs-nuggets-denver-co-11-20-2026/box-score) · [Reuters](https://www.reuters.com/sports/basketball/nikola-jokic-powers-nuggets-past-rockets-with-big-second-half--flm-2026-11-21/).

### Washington @ Chicago — total and direction miss, with an honest analyst abstention

Model C Chicago **64.39%**, expected total **239.62**; analyst abstained due symmetric matchup and uncertain rotation. Wizards beat Bulls **98–94**; biggest total miss of night **47.62**. Anthony Davis **36 and 11**, AJ Dybantsa **20/10/6**. Bulls only **36/88 FG** and **9/33 from three (27.3%)**, Washington **40/90 FG**, **9/17 free throws**. Poor conversion from both teams was prominent; don't attribute all mismatch to tempo without possession analysis. This was **not** a locked Under recommendation. [Official NBA box](https://www.nba.com/wizards/game/0022600047-wizards-vs-bulls-chicago-il-11-20-2026/box-score).

### Sacramento @ Lakers — correct heavy favorite, fragile margin

Model C Lakers **88.47%** and expected home **+15.84**. Actual **106–104**, a +2 home win and **13.84 margin error**; total expected **235.35**, actual **210** (**25.35 total error**). Kings built **11-point second-half lead**, De'Andre Hunter scored **30** and Sabonis **19/16**; Luka **25/8** and Grimes' decisive three carried Lakers home. Analysts did anticipate Luka turnovers and Sabonis interior as counter. Cup differential stakes cannot turn a two-point result into a large theoretical win. [NBA box](https://www.nba.com/lakers/game/0022600051-kings-vs-lakers-los-angeles-ca-11-20-2026/box-score) · [Reuters](https://www.reuters.com/sports/basketball/lakers-rally-past-kings-avoid-back-to-back-losses--flm-2026-11-21/).

### Toronto @ Detroit — only selected analyst winner miss

Both model **DET 72.01%** and analyst DET **LOW** lost to Toronto **105–102**. Scottie Barnes **29** and go-ahead layup with **14 seconds** left. Cade played, so a pretip PROBABLE status did not resolve in a late absence; the first-view *counterargument* already highlighted Barnes/Quickley/Poeltl against Duren-less frontcourt. Home-margin expected **+7.34**, actual **−3** (**10.34 error**). One game cannot quantify Duren's absence impact. [NBA summary](https://www.nba.com/game/tor-vs-det-0022600046) · [Reuters](https://www.reuters.com/sports/basketball/scottie-barnes-late-layup-snaps-slide-raptors-win-over-pistons--flm-2026-11-21/).

### Orlando @ Brooklyn and Pelicans @ Oklahoma City — live underdogs, winner picks correct

Orlando **113–111**: Franz Wagner **35** including go-ahead jumper with **2.8s** left, a concrete test supporting the pretip Wagner/Bane shot-creation question. Brooklyn still nearly won, so a MEDIUM correct pick isn't a blowout prediction. [Reuters](https://www.reuters.com/sports/basketball/franz-wagner-delivers-game-winner-magic-beat-nets-reach-3-0-cup--flm-2026-11-21/).

OKC **126–120**: model forecast **+13.17**, realized only **+6**. SGA **40** and rookie Aday Mara **22/16** helped offset Oklahoma's absent starters; NOP Zion and Jeremiah Fears **22 each**. Analyst LOW despite model **84.48%** accounted for meaningful defensive missing roles. Avoid falsely assigning Mara's contributions to Hartenstein. [NBA summary](https://www.nba.com/game/nop-vs-okc-0022600048).

## Governance and independently checked sources

All nine final scores and Cup labels checked against [NBA official Cup schedule](https://www.nba.com/news/emirates-nba-cup-key-dates-schedule), [NBA night updates](https://www.nba.com/news/emirates-nba-cup-live-updates-november-20) and [Reuters roundup](https://www.reuters.com/sports/nba-roundup-cavs-james-harden-moves-3rd-career-50-point-games--flm-2026-11-21/). No OT indicated in regulation full-game scorebooks. Model/analyst retrospect from original locked fields only; market zero eligible, no hindsight bets; no automatic model fit, production promotion or invented Cup coefficient. [Machine-readable per-game metric file](./2026-11-20-nine-cup-games-shadow-retro-v1.json).
