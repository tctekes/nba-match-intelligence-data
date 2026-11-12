# NBA Match Intelligence 1.0 — Locked 12 November 2026 SHADOW comparison

**Fixture NBA local date:** 2026-11-12 (games early 2026-11-13 in Türkiye)  
**Record status:** IMMUTABLE COMPARISON / SHADOW ONLY / NOT PRODUCTION  
**No postgame information used in this record:** Results deliberately not included.  
**Original experimental Keel Stats lock:** 2026-11-12 14:06:44 Europe/Istanbul, as documented in earlier NBA Match Intelligence pilot.  
**Clean-source Model C results:** Transcribed from the NBA ChatGPT Project's TASK 11A output supplied to the architect; Project reported all four fixtures not started at calculation time. Actual runtime timestamp was **not** in the submitted result, so no precise calculation timestamp is claimed. Git commit timestamp provides an audit timestamp for this file.  
**These are two separate prediction sets, NOT a retroactive change to the earlier locked pilot.**

## Predictions

All margins are **home score minus away score**. Probability is the listed predicted winner's probability. Totals are full-game expected points, not betting lines.

| NBA fixture (away @ home) | Keel pilot winner | Keel win % | Keel home margin | Keel total | Clean Model C winner | Clean win % | Clean home margin | Clean total |
|---|---|---:|---:|---:|---|---:|---:|---:|
| TOR @ PHI | PHI | 51.60% | +0.50 | 223.20 | PHI | 52.39% | +0.74 | 224.02 |
| DET @ WAS | DET | 80.50% | -11.00 | 221.10 | DET | 82.13% | -11.85 | 223.49 |
| DAL @ MIN | MIN | 73.20% | +7.80 | 224.80 | MIN | 73.37% | +7.87 | 226.21 |
| CHA @ PHX | PHX | 61.60% | +3.70 | 220.40 | PHX | 59.47% | +2.98 | 222.91 |

## How the clean-source run was verified

- **ChatGPT Project TASK 11A:** reports PASS on GitHub connector `fetch_file`, SHA-256, 30 team entries, 170 raw games, 168 accepted, 2 fully excluded, accepted team GP sum 336, frozen model SHA checks, Python self-test and actual invocation of `runtime_league_center`, `feature_values`, `predictions`.
- **Clean-source index:** `published/accepted_candidate_index.json` (main).
- **Snapshot JSON:** `published/accepted_candidates/2026-11-11-accepted-e8136e3e0310.json`.
- **Snapshot SHA-256:** `e8136e3e03103a7d7f17a3fa6e99182cf4b13321a076cb5e6b2ce84075c1d1b1`.
- **Source completed through:** NBA date `2026-11-11`.
- **Frozen model:** Model C v0.1 (`nba_baseline_v01.py`, `baseline_v01_parameters.json`); neither was changed for this comparison.
- **Excluded whole games:** `401909277` CHA–WAS 2026-10-30 (CHA turnover disagreement); `401909949` BOS–MIL 2026-11-08 (BOS FGA/OREB disagreement).
- No injury, lineups, odds or market lines included.

## Interpretation and retrospective rules

- Same four projected winners in both versions. Different inputs produced differences in expected totals and confidence, but **this one night does not establish that either source is better**.
- Do not retroactively edit either prediction set, its probability or its projected total after game results become known.
- Retrospective: collect **independently verified final scores** after completion, then compute winner accuracy, Brier score using home-win probability derived consistently from listed winner, total MAE and margin MAE for each set. Flag OT separately. Keep any result-capture time distinct from prediction time.
- Daily GitHub job is **experimental candidate publication**, not production approval. No `published/latest_valid.json` promotion is implied.

## Source/authority note

This file transcribes prior user-shared Project results; it does not claim that this GitHub-writing chat independently re-ran the frozen Python predictions. The Project itself reported the SHA and Python computation PASS. All source data and provenance are recorded in the indexed snapshot. If an original source lock artifact is later found, retain it and cite it rather than overwriting this report.
