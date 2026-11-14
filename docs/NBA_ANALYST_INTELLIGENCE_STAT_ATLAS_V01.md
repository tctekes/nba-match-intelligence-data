# NBA Match Intelligence 1.0 — Analyst Intelligence Stat Atlas v0.1

**Created:** 2026-11-14 (Europe/Istanbul)  
**Purpose:** Give the ChatGPT Project a sourced NBA-scouting vocabulary that goes beyond frozen Model C v0.1 team OffRtg / DefRtg / pace, without changing its math or inventing quantified probability adjustments.  
**Status:** Research / analyst playbook. **Not** a proof that all sources can be acquired daily, no live data ingestion implemented here, and **not** a model promotion.

## Guiding analyst principle

A team's *season-average strength* (frozen Model C) is different from *tonight's available lineup, opponent-specific tactical fit, possession profile, game-state behavior, and motivation*. Use research to **explain circumstances under which a model outcome becomes fragile**, then label an **independent qualitative analyst lean**, which may disagree with the model. Never silently substitute the analyst's opinion for the original model forecast/probability. Cite concrete quantities with date, source, span/sample, and reliability.

### Signal selection hierarchy

- **P0 / routinely useful, observable:** Official injury OUT / active availability and minutes replacement; offensive/defensive Four Factors; offensive/defensive shot profile; opponent shot-zone defense; possession mix (transition/half-court); major role/rotation changes; NBA Cup status/stakes; rest, home, back-to-back.
- **P1 / situation-dependent:** Clutch possession sample and NetRtg; fourth-quarter lead protection/comeback; scorer/creator dependency; lineup net ratings and WOWY on/off with possessions; Synergy play-type Frequency and PPP against specific defense; 3PT volume/shooting volatility; opponent strength-adjusted form; seconds per possession.
- **P2 / specialist evidence:** Expected eFG shot quality; player-level matchup tracking (defender assignment); defensive deterrence at rim; box-outs and screen assists; bench-vs-starters lineups; possession-by-score leverage and tactical late-game changes.

## 1. Close game / team "finishing character" (focus when model margin is small)

| Statistic | Analytic question | Caveat |
|---|---|---|
| **Clutch OffRtg, DefRtg, NetRtg** | Is the team executing offense/defense efficiently in official clutch possessions? | Last 5 minutes, margin ≤5; very small possessions and selection effects |
| **Clutch W/L + games + possessions** | Did this team actually win the close finishes? | W/L alone confounded by opponents, luck, high-leverage shooting |
| **Clutch TOV%, eFG%, TS%, AST/TO and FTr** | Are losses due to creation/turnovers, shot selection, or fouls? | Use absolute attempts/possessions; no narratives from 2 games |
| **Clutch player USG%, on/off, TS% and available closing five** | Is a trusted late-clock creator/finisher available tonight? | Five-man combos/players need minute thresholds |
| **Lead Protection Rate, Q4 entering lead of 6+, 10+** | Does a team keep a sizable lead into the final? | **Derived** from PBP / quarter scores; opponent strength, lineups, win probability expected conditional on lead |
| **Comeback Rate from Q4 deficit 6+, 10+** | Is the team legitimately strong at reversing deficits? | Base rate is low; tiny samples and game-state biased |
| **Close-game points per possession by score/time (PBP)** | What happens in the *relevant* 1–2 possessions? | Custom play-by-play segmentation; do not conflate with whole season strength |

**Responsible vocabulary:** “İki takımın baz tahmini birbirine yakın; [team] kapanış beşlisi/creator availability açısından avantajlı görünüyor. Ancak clutch örneklemi N pozisyon ve güven düşük.” That can legitimately motivate a distinct *ANALYST_LEAN* opposite to a ~50–50 MODEL_C_BASELINE; do not modify Model C's probability numerically.

Sources: [NBA clutch advanced](https://www.nba.com/stats/teams/clutch-advanced), [NBA stats glossary](https://www.nba.com/stats/help/glossary), [PBP Stats score-time / leverage summaries](https://api.pbpstats.com/docs), [PBP Stats](https://www.pbpstats.com/).

## 2. Player absence and rotation impact (especially **confirmed OUT**, not rumors)

| Statistic | Analytic question | Caveat |
|---|---|---|
| **DARKO DPM** and **Offensive / Defensive DPM** | How valuable is the missing player in projected points/100 possessions relative to average? | A **player** projection, not a direct game spread adjustment |
| **DARKO Projected MPG / Roster Lab** | How many minutes/roles need redistribution; who replaces him? | Projections are not lineup confirmations |
| **Dunks & Threes expected EPM Off/Def and expected minutes** | Does independent impact modeling see similar role/value? | Independent model; access/usage conditions need feasibility check |
| **WOWY On/Off ORtg, DRtg, pace, 4 Factors** | How did team play with/without player, with role-specific teammates? | Raw on/off confounded by teammates/opponent and tiny possessions |
| **Lineup possession-weighted NetRtg** | Does actual replacement lineup remain viable? | 5-player net ratings highly noisy; show possessions/minutes and shrink |
| **USG%, AST%, potential assists, time of possession, touches, drive assists/PTS** | Which on-ball creation role disappears? | Usage is dependence, NOT overall impact |
| **Rim defense DFG%, contested rim shots, opponent rim attempts, DREB%** | What defensive deterrence/rim protection disappears? | Boxscore blocks alone do not capture rim deterrence |
| **3PA rate, catch-and-shoot volume, spacing** | Which shot quality and spacing ecosystem changes? | Does not mean all missing shots become missed |

**Three-part injury note:** (1) Verified status and timestamp from [official NBA injury report](https://official.nba.com/nba-injury-report-2026-27-season/), confirmed before tip; (2) Player value and role, cross-check DPM vs estimated EPM / actual usage; (3) Replacement and opponent who can exploit lost skill, plus counterargument. If injury is questionable/unknown, do not phrase as confirmed absent. Record pretip status separately from postgame did-play.

Sources: [DARKO method](https://www.darko.app/about), [DARKO Roster Lab](https://www.darko.app/lab), [Dunks & Threes EPM methodology](https://dunksandthrees.com/about/epm), [NBA player advanced](https://www.nba.com/stats/players/advanced), [NBA lineups advanced](https://www.nba.com/stats/lineups/advanced), [PBP on/off and WOWY](https://www.pbpstats.com/).

## 3. Tactical matchup — attack meets a specific defensive weakness

| Statistic | Questions to answer | Caution |
|---|---|---|
| **Offensive / defensive Synergy play-type FREQ% and PPP** for isolation, PnR handler/roll man, transition, spot-up, post-up, putback, cuts | A loves this play; does B allow high PPP defending it? | Compare **frequency AND efficiency**; play-type labeling and sample thresholds |
| **Shooting zone distribution: restricted area / paint / midrange / corners / above-the-break 3** | Is the preferred shot map naturally available vs this opponent? | Attempt rate more stable than tiny-zone FG% |
| **Opponent 3PA allowed, rim FGA allowed, defensive rim DFG%** | Does the defense deter or surrender volume, quality, or makes? | DFG% can be shooting-luck affected |
| **Deflections, steals, forced live-ball TOV vs opponent live-ball TOV** | Could pressure initiate easy transition points? | Deflections ≠ steals; rate per possession is better than per game |
| **OREB% vs opponent DREB%, second-chance PPP, box-outs** | Could extra possessions tilt points and margins? | Don't add OREB twice to an existing efficiency estimate |
| **Free-throw attempt rate vs foul rate** | Does one team pressure the paint against a foul-prone defense? | Whistle style/no referee causation without robust evidence |

Sources: [NBA Synergy team playtypes](https://www.nba.com/stats/teams/ball-handler), [NBA transition attack/defense](https://www.nba.com/stats/teams/transition), [NBA opponent shooting](https://www.nba.com/stats/teams/opponent-shots-general), [NBA team hustle](https://www.nba.com/stats/teams/hustle), [NBA Four Factors](https://www.nba.com/stats/teams/four-factors), [NBA stat glossary](https://www.nba.com/stats/help/glossary).

## 4. Total points / O-U narrative (model first, market second)

**Model C full-game expected total is independent of odds.** After freezing the number and quote, use these descriptive signals in the expert assessment:

| Stat | Interpretation for total | Caveat |
|---|---|---|
| **Pace + seconds per offensive/defensive possession** | Total possessions and speed, including whether team plays quickly after misses or live-ball steals | NBA official pace = per 48 min; frozen Model C source construction is different (full-game). NEVER substitute raw values into the frozen model |
| **Transition FREQ%, transition PPP and defense transition allowed** | Open-floor scoring opportunities | Focus on both frequency and efficiency; teammate injury changes opportunities |
| **3PA/FGA, above-break 3 FREQ, catch-and-shoot volume** | High-volume 3P creates wider scoring distributions | Volume and shooting luck distinct; raw last-three-game 3P% ≠ stable skill |
| **eFG%, TS%, FTr and opponent rates** | Shot efficiency and free throws, score expectation | Possessions and efficiency must be disentangled |
| **OREB% + 2nd-chance possessions** | Extra scoring opportunities on otherwise missed possessions | Their points already influence historical ORtg; commentary not additive formula |
| **Live-ball turnover frequency, transition conceded** | Both lower own shot possessions and give opponent early offense | Turnovers may alter total in either direction |
| **Half-court PPP, late-clock / isolation dependence** | Can opponent turn efficient early offense into grind? | Not every source exposes stable half-court splits |
| **Bench quality, rotation depth, garbage-time, Cup regulation margin incentives** | Late game scoring/tempo may depart from starters' mean | Explicitly separate Cup ranking tie-break from real full-game totals |
| **OT tag and close-game variance** | OT can increase full-game total | Never retrospectively exclude OT from the scored full-game prediction |

Sources: [PBP Stats possession-length and play-start metrics](https://www.pbpstats.com/), [NBA team tracking](https://www.nba.com/stats/teams), [NBA stat glossary](https://www.nba.com/stats/help/glossary), [NBA Cup regulation-only tiebreaker](https://www.nba.com/news/nba-cup-101).

## 5. Form, opponent quality and environment

| Signal | Question | Caution |
|---|---|---|
| Rolling 5/10 game ORtg, DRtg, NetRtg vs season baseline | Is trend persistent or one hot-shooting night? | Current season still 10–12 games as of initial experiment |
| Opponent strength-adjusted NetRtg / schedule strength | Were wins vs weak opponents, losses vs elite defenses? | Need *as-of* date; opponent season endpoint can leak future games |
| Home/away splits, venue and altitude | Is context relevant to this matchup? | Shrink small sample splits |
| Rest days, back-to-back, travel, minutes load | Is projected stamina/rotation affected? | "Tired" narratives need pregame objective schedule evidence |
| NBA Cup stage, group standings / advancement stakes, rematches | What stakes and incentives are verifiable **before tip**? | Both teams can be motivated; no invented Cup upset multiplier |
| Team 3PT rate / volatility and scoring spread | Is lineup/system a high-variance scoring engine? | Volatility must be empirically measured, not inferred solely from 3P volume |

Sources: [NBA Cup format](https://www.nba.com/news/nba-cup-101), [CraftedNBA schedule strength context](https://craftednba.com/strength-of-schedule), [sportsdataverse as-of opponent-adjusted ratings](https://sportsdataverse-py.sportsdataverse.org/docs/0.0.73/nba/reference/additional), [NBA schedule](https://www.nba.com/schedule).

## 6. Team DNA Card — descriptive tags, no premature labels

**Candidate team tags, not automatic truth:** `FAST_TRANSITION`, `HALFCOURT_SLOW`, `PNR_HEAVY`, `DRIVE_AND_KICK`, `THREE_POINT_HEAVY`, `RIM_ATTACK`, `RIM_PROTECTOR`, `DEFLECTION_PRESSURE`, `OFFENSIVE_GLASS`, `FOUL_PRESSURE`, `BENCH_DEPTH`, `STAR_CREATOR_DEPENDENT`, `CLUTCH_CREATOR`, `LEAD_PROTECTOR`, `HIGH_VARIANCE`.

A tag is **assigned only if at least two relevant measurements**, with source/date/sample, support it. Each must have a **counter-signal or stated uncertainty**. Examples: `THREE_POINT_HEAVY` = high 3PA share + above-break/catch-and-shoot frequency; `STAR_CREATOR_DEPENDENT` = high player USG/AST creation share + credible on/off/rotation split; `LEAD_PROTECTOR` = Q4-leading conversion + conditional late-game per-possession net, benchmarked against expected conversion at same lead. Tags must not be invented from a win streak or one television narrative.

**Team card fields:** team/season/as-of date; sample GP and possessions; model baseline Off/Def/Pace **unchanged**; last-10 efficiency vs opponent strength; possessions style/shot mix; defense vulnerabilities; creator concentration; clutch/lead-comeback; known starters and replacement depth; dated injuries; NBA Cup/rest; 3 evidence-backed tags plus 1 weakness; source provenance; `DATA_MISSING` fields.

## 7. Game analyst use — contextual lean, not fake model refitting

Per matchup, the ChatGPT analyst reads the locked original Model C winner %, projected home-away margin, total; then **selects at most three material signals**:

1. Who is confirmed OUT and which teammate absorbs actual minutes?
2. Where does A's most-used offense meet B's specific defense?
3. In close games, do reliable lineup and clutch/game-state signals support a lean, after sample caution?
4. For full-game totals, which possession and shot-efficiency mechanisms justify OVER/UNDER contextual confidence, relative to a **verified pretip main line**?
5. What counter-evidence contradicts the favorite and what is not knowable yet?

Use a distinct `ANALYST_LEAN` (same winner, other winner, or insufficient evidence) and qualitative `LOW / MEDIUM / HIGH` confidence. If opposite the model pick, explain facts, dates, sample and alternatives; **the model number NEVER changes**. Track separately whether the analyst beat the baseline in prospective retros; do not retro-edit the lean or infer a new percentage.

### Match Card (human presentation, NOT a single-row-only dump)

```text
NBA CUP · [Away @ Home] · [Tipoff in Europe/Istanbul]
MODEL C   Winner [team] 64.2% | Expected home margin +4.5 | Total 231.7
MARKET    Full Game O/U 228.5 | Over 1.92 / Under 1.92 | verified book + captured UTC
O/U       OVER 228.5 · LOW/MEDIUM/HIGH qualitative confidence (not probability)
MATCHUP   [One offensive-vs-defensive mechanism with source and sample]
ROTATION  [Confirmed OUT, DPM Off/Def, replacement who absorbs minutes, uncertainty]
FINISH    [Clutch/lead data if relevant; otherwise OMIT]
CUP/REST  [Verified stakes and schedule context]
ANALYST   [Same as model or conditional opposite-side lean] · LOW/MEDIUM/HIGH
RISK      [Best 1-2 counterarguments]
AUDIT     Source time, Model C SHA, snapshot SHA, pretip lock link
```

Cards in the conversational UI should have a compact heading + standout forecast and O/U + explanatory prose; do not expose 30 metrics in every card. Provide an optional deep dive with the metric and evidence table when the user selects a game. Underlying data should remain structured; no image generation is needed.

## 8. Data access / trust tiers

| Source | What it can supply | Access/automation assessment |
|---|---|---|
| **NBA.com/stats & official injury report** | Official team/player advanced, clutch, 4 factors, tracking, shot zone, Synergy, status | **High authority**; web UI public, automatic Python/API extraction and stable rate limits **must be tested**. Sometimes pages render no data or are protected |
| **PBP Stats site and documented API** | WOWY/on-off, possession length, quarter lead / comeback, time-score, starts, expected eFG, bench | **Promising** for reproducible derived team character. API documented; request limits/stability and permissions **unverified** in our GitHub Actions |
| **DARKO** | Forward-looking DPM Off/Def, projected MPG, as-of history, CSV, lineup/Roster Lab | Research UI and CSV exist. Bulk automated redistribution rights and accessibility need validation |
| **Dunks & Threes** | EPM / Expected EPM, projected minutes, team-strength comparison | Public methodological description; full exports/API/access tier must be checked. No paid dependencies assumed |
| **BoxScore Lab** | Our known verified Model C season game inputs; potential extra box-derived rates | Already validated independent data pipeline; derivative fields require separate audit and timestamped schema |
| **sportsdataverse hoopR / Python** | Official report history, PBP, opponent-adjusted as-of ratings | Published docs suggest useful **free/open feasibility candidates**, but date coverage and connector automation must be checked |
| **Cleaning the Glass** | Garbage-time filtered lineup, halfcourt, transition, percentiles | Useful as a research reference; membership access means **not** default free production dependency |

Source links: [NBA Quick Links](https://www.nba.com/stats/quicklinks), [official 2026-27 injury report](https://official.nba.com/nba-injury-report-2026-27-season/), [PBP API docs](https://api.pbpstats.com/docs), [DARKO about / CSV](https://www.darko.app/about), [EPM method](https://dunksandthrees.com/about/epm), [hoopR injury history](https://hoopr.sportsdataverse.org/reference/load_nba_stats_injury_report.html), [Cleaning the Glass](https://cleaningtheglass.com/).

## 9. Hard reasoning and integrity rules

- **No double counting.** OffRtg already reflects historical 3P%, OREB, turnovers and free throws; derived component stats are descriptive (why), not additive to point projections.
- **No source-definition substitution.** NBA official Pace/48 minutes and Model C frozen full-game pace are not identical. Some Synergy PPP uses play-type possessions; compare only same-source definitions.
- **Clutch and lineup sample-size caution.** Show GP, possessions and MIN. Prefer prior-season context for 10-game current samples and shrink extremes. Do not classify a team as “clutch” from three wins.
- **Time-travel integrity.** Past-date tests may use only available player ratings/injury reports/lineups from BEFORE those games, never present-day rating to evaluate prior picks. Player DPM Time Machine and historical NBA injury reports may help.
- **Opponent-quality and game-state confounding.** Beware garbage time, easy schedule, simultaneous player absences, opponent shooting luck and player on/off teammate co-linearity.
- **Provenance every time.** Every nontrivial numeric claim links to source URL, exact season, timestamp, possessions/games/minutes and freshness; if unknown, say unknown.
- **No fabricated O/U market:** Independent Model C total first; actual bookmaker full-game including OT main line and European decimal odds second; qualitative OVER/UNDER direction and transparent source confidence. Absence of verifiable line => no fake barem.
- **No invented analyst confidence:** LOW/MEDIUM/HIGH are qualitative judgment, NOT % chance. Track prospective hit rate by tier; no ROI/profit or stake recommendations.
- **No premature contender changes:** Any numerical injury/Cup/clutch adjustments are separate challenger models needing holdout/backtest, not modifications to frozen Model C.
