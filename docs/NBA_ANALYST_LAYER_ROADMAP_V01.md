# NBA Match Intelligence 1.0 — Analyst Intelligence Layer Roadmap v0.1

**Owner:** ChatGPT Project NBA Expert / analyst, architect-driven proof-of-value.  
**Date:** 2026-11-14 Europe/Istanbul  
**Research basis:** [Sourced NBA Stat Atlas](./NBA_ANALYST_INTELLIGENCE_STAT_ATLAS_V01.md).  
**Status:** PROPOSAL with priority and acceptance gates; no model retuning; no claim of deployed analyst-data ETL.

## The outcome we want

**Every nightly game becomes a meaningful NBA analysis**, not an Excel-row score prediction. ChatGPT Project acts as an independent NBA analyst who understands player roles, game state, tactical matchups, season context, verified OUTs, opponent-adjusted trends, NBA Cup and O/U, grounded in source + sample sizes.

It must keep separate:
- `MODEL_C` frozen quantitative base (P, home margin, total);
- `BASKETBALL_EVIDENCE` sourced observations;
- `ANALYST_LEAN` independent winner interpretation (may disagree with model if justified; not a fake revised model probability);
- `O_U_MARKET` independent verified main-line full-game including OT with decimal odds;
- `O_U_DIRECTION` and `O_U_QUALITATIVE_CONFIDENCE`, identified separately, not misrepresented as calibrated probabilities;
- `AUDIT_LOCK` date/timestamp/source/model hashes and pretip qualitative lean.
- `POSTGAME_RETRO` outcomes, reason codes, conditional context and qualitative-confidence hit rates.

## Priority list — return on analytical effort

| Priority | Module | NBA question answered | Practical source | Development need |
|---|---|---|---|---|
| **P0** | Confirmed OUT + player role/impact | How much of tonight's offense/defense/creation changes? | NBA official injury, DARKO (DPM Off/Def+projected MPG), NBA roles | Web-based expert lookup first; archive verified statuses |
| **P0** | Matchup of team Four Factors and shot zones | How does A attack B's vulnerabilities? | NBA.com/stats Four Factors, opponent shooting, Synergy play-type | Expert research now; source feasibility before daily auto-ETL |
| **P0** | NBA Cup + rest/availability | Is this a materially different competition/stakes context? | NBA official schedule/Cup rules, injury reports | Already defined Cup gate in new market protocol; Project instructions must reference |
| **P0** | Full-game O/U plus analyst qualitative confidence | What's the model relative to actual bookmaker main line and key variance risks? | Existing Model C lock + verifiable European book | **IMPLEMENTED in v0.2**: verified main-line prices require pretip analyst-reviewed OVER/UNDER, qualitative LOW/MEDIUM/HIGH and evidence; no arbitrary PASS threshold |
| **P1** | Team DNA Card for all 30 | Which repeatable styles and weaknesses characterize each team? | Official team tracking, PBP Stats, Synergy, Four Factors | Pilot **six teams**, then automate 30 if viable |
| **P1** | Clutch / lead protection and comeback | Does either team have a robust close-game finishing edge? | NBA clutch + PBP score/time | Need sample sizes, opponent context, shrinkage; avoid premature winner flip |
| **P1** | Rotation and on/off WOWY | Does replacing an OUT star preserve the relevant style? | PBP Stats on/off, official lineups, DARKO minutes | Query on confirmed injuries only; avoid minutes/source mismatch |
| **P2** | Shot quality / halfcourt and variance | Why might expected total be high/low, independent of book line? | PBP expected eFG, offensive playtype, seconds/poss | Verify access & definitions; no arbitrary +/- points |
| **P2** | Opponent-adjusted rolling form | Is win/loss trend strong or weak-opponent schedule illusion? | public as-of ratings, original verified boxscore history | Backtest only if strict as-of data boundary |

## Execution phases, ordered by proof of value

### Phase 0 — expert instructions without bulk infrastructure

- Put **Atlas v0.1** into the ChatGPT Project's sources. In permanent Project Instructions, define NBA expert persona, mandatory official Cup/injury check, frozen model vs independent analyst lean, opponent-context first, no bluffing, short cards + expandable deep dives.
- For each matchup, investigate **2–3 most relevant signals**, not the whole metric catalog by rote. For close expected margins use clutch/closing availability; for missing star use DPM+replacement; for O/U use possessions mix and shooting/foul profiles.
- Start manually assisted shadow analysis. User can request “Why is your analyst lean different from Model C?” and get a sourced explanation.
- Acceptance: 4 real prospective match cards verified as-of before tip, no fabricated stats, model hashes and original results unchanged, expert judgment timestamped. **No numerical adjustments.**

### Phase 1 — **Codex low-cost source feasibility pilot (next recommended technical task)**

- Teams: **NYK, IND, ATL, CHI, OKC, LAC** (contrasting recent close-game/losses); strictly 2026–27 data **as of date tested**; do not time-travel fresh data back to 2026-11-13 pregame.
- Discover and test free machine-readable sources for: (1) Four Factors with opponent splits; (2) shot/3PA/foul distribution; (3) clutch with possession/sample count; (4) on/off and matchup rotations; (5) PBP fourth-quarter lead/deficit conversion; (6) play-type frequencies/PPP if actually available.
- Distinguish **FETCHED_VERIFIED**, **WEB_ONLY**, **DERIVABLE_FROM_FREE_PBP**, **BLOCKED/REQUIRES_PAYMENT**, **NOT_AVAILABLE**. Never claim access from a link alone.
- Build **six dated JSON Team DNA candidates and one Markdown analyst comparison** if, and only if, enough source data truly accessible. Include source URL, timestamp, season, games/possessions, data definition, data lineage. For missing fields use `null` plus status.
- Source id/team mapping and returned team-game counts verified; existing private model and params untouched; no new workflow schedule or production writes.
- GO gate: ≥4/6 teams with ≥4 independent relevant **verified** feature families (not four variants of same stat), correct dates/units, matching authoritative samples, at least 2 counterexamples/unknowns in the analyst comparison, and tests in an isolated directory. On failure produce source feasibility report with reasons, **NO invented Team DNA cards**.
- Only after GO create 30-team weekly Team DNA refresh with cache, backoff, provenance and sample thresholds. Daily detailed clutch/player data request triggered by important fixture/injury, not eagerly for all teams.

### Phase 2 — player-impact case study

- Pick **two prospectively confirmed OUT** examples. NBA official injury PDF time, DARKO Off/Def DPM and projected minutes, WOWY only if enough possession history, replacement players' roles, opponent attack.
- Build two **Player Absence Evidence Cards** with what player changes, whom opponent can target, alternative lineup adjustment, a strong counterargument; never fit numeric spread shift.
- GO gate: status timestamp, available minutes, exposure sample, matched identifiers, two separated independent sources and explicit unknown/uncertainty. No body of text like “missing 3.2 DPM means -3.2 margin”.

### Phase 3 — same-day game cards + long-term retro

- Introduce a 2-layer Project output: brief nightly slate overview then **per-match forecast cards** (opening heading/score expectation, verified O/U, 2–3 relevant evidence cues, context caution, qualitative analyst lean, counterargument, provenance). User may open deeper per-match factor and source tables.
- Store append-only pregame **Model C baseline** plus separately frozen **analyst lean/confidence**, `is_nba_cup`, injury statuses with timestamp, market line and O/U confidence **before tip**. Never overwrite previous lock; future notes are revisions only with second timestamp and a new ID.
- In postgame retro separately measure (a) Model C winner accuracy, Brier, margin/total MAE; (b) pretip analyst-lean winner accuracy by confidence and disagreement slice; (c) O/U WIN/LOSS/PUSH, correct denominator/coverage by confidence; (d) material context flags and failure modes.
- GO gate: at least 4 distinct dates of leak-free source/lock/retrospective, no invented pretip markets, UI usable without requiring spreadsheet reading. More days needed to conclude real predictive value.

### Phase 4 — quantified challenger (not yet approved)

- If several weeks of prospective data show a consistent, repeatable blind spot, define separate `MODEL_D_CHALLENGER`: candidate official OUT effect, rest, Cup, opponent-specific playtype or calibrated late-game. Predeclare feature windows, as-of timestamps, out-of-sample holdout and numeric acceptance criteria before fitting.
- Frozen Model C retains published SHA and historical predictions; compare on same fixture set with same scoring and input cutoff. No auto-promotion.

## Analyst team character tag rule

Each `Team_DNA` label must have ≥2 distinct related metrics, source dates, span/sample, a clear competing hypothesis, and `VERIFIED` or `TENTATIVE` status. `LEAD_PROTECTOR` uses actual Q4 conditional conversion *versus lead-size expected league baseline*, not raw close-game W%; `STAR_DEPENDENT` uses player creation share plus meaningful availability/lineup evidence, not 35 PPG.

## Practical match card sketch (sample numbers are **NOT REAL**, for UI guidance only)

```
NBA Cup · Away @ Home · kickoff in TSİ
MODEL C       Home 54.3% · home margin +1.4 · total 229.6
MARKET O/U    MAIN LINE 231.5 · ÜST 1.91 / ALT 1.91 · provider timestamp
ANALYST O/U   ALT 231.5 · LOW confidence (delta -1.9; line near model)
MODEL WINNER  HOME 54.3%, unchanged
ANALYST LEAN  AWAY · LOW confidence (confirmed home lead creator OUT)
MATCHUP       Home struggles vs away high-pressure PnR defense (source + possessions)
FINISH        Away credible finishing unit, but clutch N small
RISK          Away turnover propensity and home offensive rebounding counterbalance
AUDIT         Frozen model SHA, accepted snapshot SHA, pretip source time
```

All quantitative source claims on a real card require actual evidence. If market missing, do not invent lines; O/U direction is unavailable, not PASS. Bookmaker selection and European odds rules from [totals protocol](./NBA_CUP_AND_TOTALS_MARKET_PROTOCOL_V02.md).

## Technical item resolved after the initial plan

The previous `tools/markets/total_market_overlay.py` v0.1 selected `PASS` when model/market gap was <5 points. On **2026-11-14** that was replaced with the **v0.2 analyst-review schema** (`nba-ou-shadow-overlay-v2`) and [revised O/U protocol](./NBA_CUP_AND_TOTALS_MARKET_PROTOCOL_V02.md):

- Valid bookmaker main-line quote requires a **pretip NBA analyst-reviewed OVER/UNDER** choice, `LOW/MEDIUM/HIGH` confidence, dated rationale and counterargument; never auto-PASS on a small gap.
- `raw_direction` from frozen model stays separately recorded; analyst may disagree if source-grounded.
- Missing verified bookmaker quote is `MARKET_NOT_VERIFIED` with no pick (not a forced/pretend direction).
- `LOW/MEDIUM/HIGH` are **qualitative**, not statistically calibrated probabilities. Postgame WIN/LOSS/PUSH and confidence-bin stats are supported by the new test suite.
- A prior-date pretip O/U lock was **not** created retroactively. The real dated market ingest/analyst review integration remains to be piloted.
- Original frozen Model C, previous winner locks and snapshots remain unchanged.

## Developer guardrails

- No GitHub claims of auto daily official NBA tracking retrieval unless successful and repeated independently tested GitHub Action.
- Continue existing verified boxscore exclusions as originally agreed; separate context sources do not silently modify accepted inputs.
- Do not add proprietary, paid, login-restricted or scraping-dependent services as a hard dependency.
- Avoid dumping player-by-player scouting data into the **public** repo unless usage/redistribution rights established; derived metadata/attributed summaries plus sources preferred.
- All program outputs with dates/cutoffs consistent with US-local NBA game date vs UTC vs Europe/Istanbul.
- Keep evaluation metrics separate for baseline/qualitative/market direction, with correct sample counts and no hindsight.
