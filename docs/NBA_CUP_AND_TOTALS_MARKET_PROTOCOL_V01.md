# NBA Match Intelligence 1.0 — NBA Cup & Full-Game Totals Market Protocol v0.1

**Status:** APPROVED WORKING PROTOCOL for future **SHADOW** forecasts; **not** a change to the frozen Model C v0.1 or its parameters.  
**Introduced:** 2026-11-14, AFTER the 2026-11-13 NBA Cup games were finalized.  
**Fundamental rule:** No hindsight. Add this protocol **prospectively only**; never invent pregame market lines or count retrospectively reconstructed totals picks as locked results.

## A. NBA Cup schedule/context gate (required for EVERY NBA slate)

1. Retrieve the **NBA-local game date** and every game/event from the official [NBA schedule](https://www.nba.com/schedule), or [NBA Cup 2026 schedule](https://www.nba.com/news/emirates-nba-cup-key-dates-schedule). Check **EACH** game, never infer Cup status simply from its date.
2. Record the following per fixture:
   - `is_nba_cup`: true/false;
   - `cup_stage`: GROUP_PLAY / QUARTERFINAL / SEMIFINAL / CHAMPIONSHIP / NONE;
   - `cup_group`: verified group (e.g. East B / West C) or null;
   - `cup_context_source_url`, `cup_context_checked_at_utc`;
   - `cup_stakes_known_pretip`: verified group standing, win/loss, head-to-head or elimination/advancement significance, **or unknown**.
3. On Cup nights, **explicitly display** “NBA Cup” next to each Cup fixture and include a short **context caution**, not an automatically increased upset probability: tournament stakes, possible stronger motivation for **both** teams, rotation choices, possession intensity and late-game margin incentives may alter outcomes.
4. Official rules [NBA Cup 101](https://www.nba.com/news/nba-cup-101): Cup group games also count as regular-season games. Group tiebreakers include head-to-head, **regulation point differential**, then **regulation points scored**. For group play games going to OT, OT points are not counted toward the *NBA Cup's tiebreaker* differential or points-scored; **THIS DOES NOT CHANGE** the full-game game score, Model C's full-game target, or sportsbook's full-game-with-OT total. Do not mix the definitions.
5. Player prize-pool and chance to advance may create incentives, but **no causal cup upset effect or numeric uplift has been calibrated**. Compare Cup vs non-Cup only on sufficiently large, pre-declared analyses controlling for team strength, injuries, opponent, schedule, and home.
6. For retro, include Cup flags and pregame known stakes. In postgame narrative label observed events, prospective cautions and untested user hypotheses separately. Do **not** say a team won *because of* NBA Cup without independent evidence.

### Verified audit case: 2026-11-13

Official [NBA Friday Nov. 13 slate](https://www.nba.com/schedule?cal=November&pd=all&region=1) lists **ALL NINE** fixtures as Emirates NBA Cup Group Play: NYK@IND, MIL@ORL, CLE@MIA, ATL@CHI, MEM@NOP, UTA@HOU, GSW@SAS, POR@SAC, OKC@LAC.  
The original immutable 9-match record remains untouched. User's **preferred discussion subset excludes MEM@NOP and GSW@SAS**, handled in an append-only [retro addendum](../published/retrospectives/2026-11-13-cup-and-scope-addendum.md), NOT by deleting those two from the original nine-match model-score report.

## B. European-format full-game Over/Under market capture (required for new nightly forecasts when available)

**One immutable PRIMARY MAIN-LINE quote per game.** Pre-tipoff, fetch an actual **FULL GAME TOTAL (incl. OT)** line from an accessible bookmaker or aggregator and show its **source, UTC capture time, exact line, and Over & Under decimal odds**. Never convert a 48-minute (regulation-only), team total, 1H/1Q, Asian alternative line or a live/in-play line into a full-game pregame quote.

**Predeclared sourcing precedence:**
1. 1xBet-branded NBA basketball book page when publicly readable, e.g. `https://1xbet.mobi/en/line/basketball/13589-nba`, **subject to confirming live/pre-tip availability and direct quote fidelity**. Do NOT assume this mirror is always official, current, or stable. Record the actual source domain.
2. If unavailable/ambiguous, one identified European bookmaker such as **bet365, Betano, Betsson, Unibet** with a visible full-game pregame quote.
3. If individual book inaccessible, an attributed, timestamped aggregator showing its **named source bookmaker** and full-game line, with decimal odds or a properly labelled conversion; retain URL and named book. Do not pretend aggregator is the bookmaker.
4. If no eligible and verifiable quote is available, label **`MARKET_NOT_VERIFIED`** and abstain from O/U selection for that fixture. Never fabricate a market barem.

**Which line to use:**
- Select that bookmaker's default **main total** (the centrally priced market with approximately balanced O/U odds), not a cherry-picked alternate line that maximizes the model's apparent edge.
- If several lines appear and no primary is labelled, prefer the line with the smallest absolute difference between the **vig-adjusted implied over and under probabilities** (balanced main market); if still ambiguous, abstain and mark `MAIN_LINE_AMBIGUOUS`. Do not search different bookmakers merely to find a favourable line.
- Check O and U are two sides of the **same line** and both decimal prices >1.0.
- In the table show, e.g., `Full game O/U 233.5 | Over 1.92 / Under 1.94 | Source: 1xBet-branded page, captured [UTC]`. Decimal is the required European odds format.
- Market prices can change: stored capture is a **point-in-time quotation**, not a claim of current availability. Add final pretip recheck as a second append-only quote **without altering the original forecast** if materially changed.

## C. Deterministic Model C ↔ market comparison, NO unvalidated probabilities

For each verified quoted game:
- `model_total` = original frozen Model C expected full-game total.
- `market_line` = locked, pretip full-game total line.
- `delta` = model_total − market_line.
- `raw_direction` = **OVER** if delta>0, **UNDER** if delta<0, **NEUTRAL** if delta=0.
- **Pilot selection gate** (pre-declared pragmatic abstention heuristic, NOT a validated advantage/confidence/profitability threshold): `abs(delta) < 5.0` => **PASS / WEAK SIGNAL**. `abs(delta) >= 5.0` => **SHADOW OVER or UNDER CANDIDATE**. The 5-point threshold is an operational proposal, not retrospectively optimized; evaluate its calibration and coverage prospectively before revising.
- Include `abs(delta)` and `injury_context_warning` / `cup_context_warning` as separate **non-numeric** qualifiers. Do not transform a 5- or 10-point gap into a fake win probability or a “lock”, do not claim market is inefficient, and do not conflate qualitative player scouting with quantitative model output.
- Every candidate must include the original predicted winner % and margin from the frozen Model C too, without revision.

### Required pregame fixture table

`NBA Cup? | Fixture | winner, P | model total | bookmaker main O/U line | Over decimal / Under decimal | delta | OVER/UNDER or PASS | factual context warning`

### Minimum append-only pretip record

`nba_local_date`, `fixture_id`, `tipoff_utc`, `prediction_generated_at_utc`, `market_captured_at_utc`, `market_source_url`, `bookmaker`, `market_kind=FULL_GAME_INCLUDING_OT`, `market_line`, `over_decimal`, `under_decimal`, `is_nba_cup`, `cup_stage`, `cup_group`, `model_version`, `model_sha256`, `params_sha256`, `snapshot_path`, `snapshot_sha256`, `model_expected_total`, `delta`, `raw_direction`, `selected_direction` (or PASS), `selection_rule_version`, `data_quality_status`.

Fail closed on missing tipoff/date, missing actual quote, post-tip market capture, inconsistent book/line, missing snapshot checksum or other unverifiable provenance. Do not silently reuse prior day's line. Save **new** per-date `published/forecast_locks/YYYY-MM-DD-model-c-with-ou-shadow.json` + human-readable companion; never overwrite existing winner forecasts.

## D. Retrospective and performance

After game is FINAL, independently validate full-game score and OT flag; *full-game INCLUDING OT* total = away points + home points.

- For each **pretip locked, selected** `OVER`/ `UNDER`, grade **WIN** if total respectively > or < the exact captured line, **LOSS** if reverse, **PUSH** on equality (possible on integer lines), **UNGRADABLE** if provenance missing, **PASS** for no selected candidate.
- Track selected O/U **correct / (wins+losses)** with pushes separately, **coverage = (wins+losses+pushes) / all eligible games**, and raw-direction accuracy separately when a captured line exists. No stake sizing, ROI claim, or betting advice inferred from accuracy alone.
- Keep **total MAE** and **margin MAE** alongside winner accuracy and Brier; Over/Under classification is a *new parallel metric*, not a replacement for raw total error.
- Evaluate Cup vs non-Cup; group-play vs knockouts; OT; main-line quote age; injury warnings; pretip line movement. Declare any filters **before** outcomes and show small sample counts.
- **Historical safeguard:** 2026-11-12 and 2026-11-13 original locks did **not** include a pretip O/U quote plus selection: their **official prospective O/U score remains N/A**. You may show a **clearly-labelled retrospective illustration** using historical odds if a sound timestamped market record exists, but NEVER count it as a locked hit, never claim pretip selection.

## E. Ownership and sequence

1. Daily GitHub source accepted candidate via independent tests; do not alter model.
2. Official fixture + NBA Cup metadata verification.
3. Fresh bookmaker market quote and decimal odds receipt; fail closed per-game if missing.
4. Real Python frozen Model C predictions, independent source SHA and selftests.
5. Compare totals to **predeclared fixed** bookmaker main line; add qualitative NBA expert scouting separately.
6. GitHub immutable append-only pregame lock **before the first relevant fixture begins**.
7. Next morning final-result verification and separate append-only winner/Brier/total MAE/margin MAE/**selected O/U** retrospective.
8. Investigate hypotheses with accumulated prospective evidence; challenger separate; frozen Model C stays frozen.

**Release gate:** This document defines a workflow, **NOT** implementation or proof that live automatic odds fetching or daily O/U locking exists yet. The daily accepted snapshot publisher is separate and still experimental. Initial market capture can be performed by the ChatGPT Project with web access, with provenance checked and persisted; fully automated collection must be independently tested for stable lawful access, correct bookmaker markets, date/time and odds format.
