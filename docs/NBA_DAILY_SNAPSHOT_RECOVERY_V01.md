# NBA Match Intelligence 1.0 — Daily Snapshot Self-Recovery v0.1

**Applies to:** NBA Project's daily SHADOW operation when `accepted_candidate_index.json` is not fresh. **Does not override data gates.** Update: 2026-11-15.

## Purpose

NO-GO on stale inputs is correct, but it is **not the final action** when the Project can safely trigger a validated retry using its connected GitHub permissions. On user's normal daily request (e.g. “bu gece NBA maçları”), attempt the existing safe recovery path before asking them to switch to the architecture chat.

## Protocol

1. Determine NBA-local date, local TSİ time, and which **completed and fully closed NBA dates** are required. Check `published/accepted_candidate_index.json` plus the accepted JSON, current GitHub Actions run history and latest status of `.github/workflows/accepted-candidate.yml`.
2. If the snapshot is fresh and valid: use it. If a refresh run is currently in progress: wait/check that run, never start a competing duplicate. If before normal scheduled window: never preempt just to avoid waiting; user can request explicit recovery.
3. If both scheduled windows have elapsed and no fresh snapshot exists, and the user asked for nightly predictions: **one controlled self-recovery attempt per NBA-local date**:
   - Fetch `ops/refresh-request.txt` and its current file SHA.
   - Commit **only** that file to `main`, adding a new dated request with the intended last fully closed NBA date, reason and non-production controls. This path alone has a GitHub Actions `push` trigger.
   - Verify the new Actions run exists. Follow its actual steps and completion; if the run is unsuccessful, inspect its failure log. Do not repeatedly spam retries.
   - If repository write access is unavailable, provide the user a one-sentence escalation with the exact workflow URL and an optional ready-to-send request for architecture chat.
4. On SUCCESS, fetch the newly published `published/accepted_candidate_index.json` and `json_path`, verify its **raw SHA-256**, 30 teams, GP=2× accepted games, full-game exclusions and independent eight-field source check. Confirm it covers the desired previously completed NBA date; do not infer success merely from green Actions status (the workflow may skip when fresh).
5. On FAIL classify error: scheduled event missing/delayed; data-source CSV lag; live/current-day-vs-closed-day misalignment; independent box-score mismatch; validation/test failure; permissions; unknown. Never edit frozen Model C, relax validations, insert fabricated replacement games, or publish stale data as fresh. Complex code issues belong in architecture chat, with run/job/error line.
6. If refreshed and all gates pass, proceed with **only future-tipoff games**. Already started games are excluded from prospective Model C and analyst/market locks. Keep timestamps, original evidence and append-only audit. Source research and quote unavailability may remain PARTIAL without changing model math.
7. Report recovery succinctly: source date, raw/accepted/excluded counts, action run ID, outcome, whether it unlocked today's forecasts and number of still-eligible unstarted fixtures.

**Prevention note:** GitHub native `schedule` has already been observed materially delayed. Adding a second native cron reduces neither the dependence on GitHub's scheduler nor proves reliability. Do not count scheduled green runs that skipped work as successful data refreshes.

## Permanent generalized source fallback (implemented 2026-11-18)

See [multi-source recovery v0.2](NBA_MULTI_SOURCE_RECOVERY_V02.md). The normal accepted-candidate GitHub workflow now internally checks BoxScore Lab plus completed ESPN game coverage and, when BSL is delayed, reconstructs whole missing games from the separately published ESPN release after independent NBA Stats checks. Missing NBA games are no longer treated as an automatic terminal NO-GO merely because BSL has not updated. This is an ordinary validated feature of the single standard daily workflow, NOT a request to bypass coverage.

Follow the full-source manifest and the accepted candidate index. When fallback_completed_games > 0, explain to the user that seven full fields and the player-turnover component are independently verified against NBA Stats; ESPN's team-turnover component is checked by ESPN decomposition/live summary but not independently available from the NBA Stats release. Never claim all eight fallback fields are independently sourced. Quarantine any source conflict as a WHOLE game. An independently missing or ambiguous official match still stops the full workflow. The daily Project must verify the snapshot through the last CLOSED NBA day, full SHA, 30 teams and accepted GP before calculating any future forecasts.

**First recovery evidence:** GitHub Actions run 44356110673 published 2026-11-17 through, 210 completed, 197 BSL, 13 whole-game alternatives, 208 accepted, 2 quarantined, 30 teams and 416 GP. Original issue 401909994 is resolved in the new dataset. Frozen Model C remains untouched.

## Known incident (2026-11-15)

Initial manual attempt `43758451415`: Task08 tests passed, but snapshot builder failed with `AssertionError: Missing completed game 401909985 (2026-11-15)`. It was checking a **current NBA-local day's partly completed schedule**, when the target snapshot was the previous fully closed date **2026-11-14**. A fail-closed fix limited the daily ESPN reference to closed NBA dates (through yesterday), preserving full-completed-day coverage and independent eight-box-field audit. Follow-up Actions run **43758700332** completed successfully and published NBA-local **2026-11-14** candidate: **188 raw, 186 accepted, 2 whole-game exclusions, 30 teams, 372 team GP, 376 independently checked team box rows**. This is an **experimental SHADOW snapshot, not production**. Do not weaken full-game rejection rules to paper over lag.

## Incident 2026-11-21: GitHub schedule delay and transient ESPN TLS

At 21:26 TSİ, neither the declared 20:23 nor 20:53 TSİ GitHub-native scheduled daily run had appeared in the repository Actions history. This is a scheduler delivery delay/nonappearance, not evidence that NBA research code changed the snapshot workflow. Research experiments on 2026-11-21 used separate research paths and their separate workflow.

A user-authorized 21:17 TSİ path-triggered daily refresh (run 44934720377) failed during ESPN independent team-box summary acquisition with urllib.error.URLError wrapping [SSL: TLSV1_ALERT_INTERNAL_ERROR]. Its preflight and 26 established unit tests had passed. This was a transient upstream transport failure, not an indication of source-stat disagreement or Model C parameter corruption.

Permanent fail-closed resilience change:
- Shared tools/independent_coverage_probe.py get_bytes and tools/task08/cloud_capture_candidate.py acquire now retry ONLY explicitly transient transport errors / retryable HTTP 408,425,429,500,502,503,504; maximum FOUR attempts, delays 1/2/4 seconds; permanent HTTP errors, certificate verification errors, missing/invalid response and exhausted retries still fail closed.
- tools/task08/build_accepted_candidate.py spaces ESPN live box requests at 0.12s to reduce burst load. The same ESPN scoreboard, full 8-field per-team, source-receipt, 30-team, full-game exclusion and candidate SHA checks still run.
- tools/task08/test_transient_fetch.py adds 8 deterministic no-network tests for TLS recovery/exhaustion, 429, permanent HTTP errors, untrusted empty content, certificate failure and source capture retry.
- End-to-end path-triggered Actions run 44935756165 PASSED. Accepted snapshot through 2026-11-20: 235 raw, 234 accepted, 1 whole-game exclusion, 30 teams, 468 GP, 470 ESPN team rows independently checked, SHA verified before commit. Frozen Model C, model parameters, old locks and production pointer untouched.

This fixes transport fragility but does NOT guarantee GitHub-native scheduled jobs start exactly at their nominal cron time; GitHub schedule delays require separate operational monitoring. A green diagnostic/test run is NOT a substitute for checking published accepted_candidate_index.json freshness.
