# NBA Match Intelligence — TASK 10B/10C completed handoff

**Recorded:** 2026-11-12 (Europe/Istanbul)  
**Production approval:** CONDITIONAL / NOT YET FULL GO

## Real data and code gates passed

1. Original uploaded `static_snapshot.py` and `test_static_snapshot.py` were run locally against byte-verified frozen `nba_baseline_v01.py` (SHA-256 `b6efd52df74f540c3bda711cd37a372e1ae7cbdbda134579c4c43bc7ff1eafef`): **9/9 PASS**.
2. Original 9 tests were also run on GitHub Actions against a validation-only module containing the five exact data-validation/aggregation functions from the frozen source. No private model parameters were published.
3. GitHub original Task08 gate captured fresh upstream CSV, downloads build claim and daily ESPN scoreboards. **170 finalized games**, **30 teams**, **340 team-game records**, all scores matched. Published aggregate vs reconstructed Model C per-game means maximum absolute difference **0.00004907474914261911**. Candidate Task08 run [43271365211](https://github.com/tctekes/nba-match-intelligence-data/actions/runs/43271365211).
4. Independent per-game core-field audit [43272429597](https://github.com/tctekes/nba-match-intelligence-data/actions/runs/43272429597): **2,720 / 2,720 values compared** (340 teams × 8 stats), **zero missing box scores**, **3 disagreements across 2 games**. It correctly returned FAIL for unqualified use of all BoxScore Lab statistics.
5. The frozen Model C historical exclusion policy was then applied: **entire disputed games omitted from aggregate state updates**, rather than patching individual numbers.
6. Accepted-data candidate job [43273468042](https://github.com/tctekes/nba-match-intelligence-data/actions/runs/43273468042): original **9/9** plus 6 quarantine tests PASS. **170 raw complete games → 168 accepted**, 2 whole-game exclusions, **30 teams** and **336 accepted team-game observations**. All 8 fields for both teams checked independently in every completed game.

## Exact data disputes (omitted, not repaired)

- 2026-10-30 **CHA–WAS**, ESPN event `401909277`: CHA turnovers BoxScore Lab 12, ESPN total turnovers 13.
- 2026-11-08 **BOS–MIL**, ESPN event `401909949`: BOS field goal attempts BSL 94 / ESPN 95; BOS offensive rebounds BSL 19 / ESPN 20.

Publisher BSL team-game CSV SHA-256: `c77c09771bf7664fbae7c813d12d89546f1797b41d58a2fe0e1a8548695dbbbb`. Exclusion reasons are fully visible in snapshot JSON.

## Published candidate to read in ChatGPT Project

- Index: `published/accepted_candidate_index.json`
- Clean model input JSON: `published/accepted_candidates/2026-11-11-accepted-e8136e3e0310.json`
- Human-readable model input Markdown: `published/accepted_candidates/2026-11-11-accepted-e8136e3e0310.md`
- JSON SHA-256: `e8136e3e03103a7d7f17a3fa6e99182cf4b13321a076cb5e6b2ce84075c1d1b1`
- GitHub repository: `tctekes/nba-match-intelligence-data`, branch `main`.

**Status:** `ACCEPTED_GAMES_EXPERIMENTAL_NOT_PRODUCTION`. Do not treat this as a full production authorization. The immutable data covers completed NBA dates through 2026-11-11. Original source metrics are not silently mixed into the accepted-game calculations: each team's `n`, ORtg, DRtg and Pace are recomputed after excluding BOTH teams in each disputed game.

## Automation

`.github/workflows/accepted-candidate.yml` is set to **17:00 UTC (20:00 Europe/Istanbul) daily**, plus manual `workflow_dispatch`. It validates before publishing a new experimental accepted-game candidate. GitHub's scheduled runs may be delayed or fail upstream; the Project must not assume successful publication.

`published/latest_valid.json` is intentionally **not created**. The ChatGPT Project already proved it can read this repository through the GitHub connector (`fetch_file`); the clean candidate's actual JSON and SHA and the full inference path must still be tested in the Project. Three distinct NBA dates of on-time verified delivery remain an operational pilot requirement.

The workflow currently re-audits all historical game boxes every day (not incremental). As the season grows, monitor ESPN request limits, duration and GitHub quota; migrate to a checksum-based validated per-game cache only after proving correctness. No paid services or daily local PC dependency.

## Next gate — ChatGPT Project

Use the connector (not web reader) to fetch the exact index and linked JSON, verify content hash, all 30 teams, 336 accepted GP, 168/2 game audit, and execute the frozen Python model with its already attached private parameters for one current-season matchup. Do not promote to production or silently overwrite the earlier Keel Stats pilot predictions.

After that PASS, establish permanent Project reader instructions, make publication pointer and daily pipeline production-ready after repeated date-scoped operational checks, and track model forecasting separately from data delivery.
