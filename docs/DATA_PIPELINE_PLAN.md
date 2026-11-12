# NBA Match Intelligence 1.0 — Data Pipeline Decision (TASK 09C)

**Status:** ARCHITECTURE APPROVED FOR IMPLEMENTATION PLANNING; DAILY DATA PIPELINE NOT YET PRODUCTION-READY  
**Recorded:** 2026-11-12  
**Scope:** Public data delivery for frozen Model C v0.1 only. No new model, deployment, or prediction in this document.

## What has actually passed

- The NBA ChatGPT Project used the GitHub connector `fetch_file` to read `snapshots/reader-test.md` from this repository on `main`. The title, sentinel marker, validation flag, final sentinel, and blob SHA matched.
- This is a **GitHub read-channel PASS**, not a data-quality PASS. The reader-test fixture is explicitly invalid as NBA model input.
- Existing local `static_snapshot.py` and `test_static_snapshot.py` reportedly passed 9 tests. The 2026-11-10 snapshot was correctly marked FAIL: ten completed 2026-11-11 games were missing from the upstream BoxScore Lab data.
- Frozen v0.1 model and prior holdout are unchanged.

## Reuse the established football-project pattern

Inspected actual GitHub workflow files (2026-11-12):

- `tctekes/football-team-library`, `.github/workflows/manual-update.yml` on `main`: scheduled and manual triggering; regression tests first; download/validate/build; atomic publish of a validated package; audit artifact on failure. Readable outputs in `published/index.json` and `published/build.json` with data version, freshness and integrity metadata.
- `tctekes/goal-radar`, `.github/workflows/goal-radar.yml` on `main`: scheduled and manual triggering; validation; separate analyze and publish jobs; versioned immutable outputs on `publications` branch, with a dated publication index.

**NBA adaptation:** small GitHub Action, validating source inputs before it writes a single authoritative publication. Access the output with the GitHub connector (`fetch_file`) rather than ChatGPT's web reader.

## The critical unsolved input problem

BoxScore Lab's standings fields are consistent with Model C v0.1 within published rounding, but the observed upstream build `20261111T1405` did not include all ten 2026-11-11 NBA games. A fixed 24-hour schedule or a fresh HTML publication timestamp does **not** establish complete game coverage.

First investigate:
1. Source publication latency over multiple NBA mornings; record source build, actual final NBA game included, expected and observed game counts.
2. Whether an official/licensed, accessible alternate provides every required team-game field on time.
3. An ESPN game-boxscore **fallback as a candidate only** (not authorized or validated yet). Compare overlapping complete games with BoxScore Lab's score, FGA, FTA, OREB, TOV, opponent-paired possessions, per-game ORtg/DRtg and Pace; check terms and reliability. Do not mix different definitions or silently fill missing boxscore fields.
4. If no source can establish completeness at the forecast cutoff, report NO DATA / FAIL; never claim model-ready snapshot.

## Proposed daily publication contract

- `published/latest_valid.json`: pointer to last **validated** dated snapshot, its source through-date, cutoff, game count, SHA-256 and generation time. Never advance on validation FAIL.
- `published/snapshots/YYYY-MM-DD.md` (or JSON plus Markdown): all thirty canonical teams, GP/W/L, Model C-compatible ORtg, DRtg, Pace and explicit definitions, provenance, source revision, UTC timestamps and checksums. Immutable for each finalized data revision, or use a versioned filename if a correction is necessary.
- `published/health.json` (optional): most recent attempt status with diagnostic message and missing-game count; FAIL health must not masquerade as new production statistics.
- Full manifest, 30-team integrity, paired team-game uniqueness, W/L reconstruction, date cutoffs, numerical parity, and independent completed-game coverage must pass before the pointer advances.
- Ensure one logical publication commit. On failure leave prior valid publication intact and retain an audit log; the Project must also check freshness against the requested game schedule and **refuse** forecasts using stale data.

## Suggested GitHub Actions phases

1. **Reader PASS — COMPLETE.** Verified `main/snapshots/reader-test.md` with Project's GitHub connector.
2. **Source gate — BLOCKED.** Validate timeliness/coverage and make a bounded fallback decision based on parity evidence; do not pretend GitHub can repair missing upstream matches.
3. **Manual cloud dry run.** Upload the existing local generator/tests to this repository (only public/licensed code/data; no private model parameters or Windows paths). Run tests and build on GitHub Actions using `workflow_dispatch`. Assert the expected output is FAIL when source coverage is incomplete.
4. **First full PASS publication.** Require all gates, then publish and independently read from the ChatGPT Project with GitHub connector.
5. **Daily automation.** Enable scheduled checks plus manual dispatch, retry delayed source updates within GitHub free-tier limits, run tests, publish only on PASS, preserve audit and last good snapshot.
6. **Project production instructions.** Read `latest_valid.json` and matching snapshot; independently verify requested date, coverage and checksum before invoking unchanged Model C v0.1. Lock forecasts pre-game.
7. **Repeated operations gate.** Three separate eligible NBA dates must show timely valid snapshots and Project-readable inputs. This establishes delivery reliability, **not** model predictive accuracy.

## Scope & safety

No edits to frozen model files. No resurrection of the Cloudflare bridge. No player-prop market, EuroLeague, or private datasets. Public repository must not receive secrets, local personal files, or unrelated football projects. Preserve credit and usage constraints of every external data provider.

**Next concrete engineering step:** decide and test an admissible, on-time team-game input or fallback; then wire existing validated generator into a manual GitHub Action. Do not spend Codex credits writing a scheduler before source completeness is solved.
