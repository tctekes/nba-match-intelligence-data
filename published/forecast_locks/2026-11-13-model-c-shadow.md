# NBA Match Intelligence 1.0 — 13 November 2026, pregame locked SHADOW

**Status: LOCKED · SHADOW ONLY · NOT PRODUCTION**  
**NBA local date:** Friday, 2026-11-13 (all games occur early Saturday, Nov 14 in Türkiye)  
**Calculation as-of:** 2026-11-13 18:59:10 UTC = 21:59:10 Europe/Istanbul  
**Unmodified frozen predictor:** Model C v0.1. No injury, lineup, odds, rest, or scouting adjustment to the numeric probabilities.  
**Numerical record:** [2026-11-13-model-c-shadow.json](2026-11-13-model-c-shadow.json) (full-precision probabilities; immutable separate file).  
**All listed start times are after model calculation as-of.**

## All nine games — ORIGINAL LOCK

| TR kickoff | Away @ home | Frozen C winner | Winner P | Expected home − away | Full game total |
|---|---|---|---:|---:|---:|
| Sat 03:00 | NYK @ IND | **NYK** | **71.78%** | -7.26 | 222.07 |
| Sat 03:00 | MIL @ ORL | **ORL** | **74.15%** | +8.19 | 227.37 |
| Sat 04:00 | CLE @ MIA | **CLE** | **53.98%** | -1.24 | 236.83 |
| Sat 04:00 | ATL @ CHI | **ATL** | **73.33%** | -7.86 | 239.50 |
| Sat 04:00 | MEM @ NOP | **MEM** | **60.73%** | -3.39 | 238.18 |
| Sat 04:30 | UTA @ HOU | **HOU** | **88.34%** | +15.74 | 227.49 |
| Sat 05:30 | GSW @ SAS | **SAS** | **69.98%** | +6.58 | 230.54 |
| Sat 06:00 | POR @ SAC | **POR** | **78.11%** | -9.89 | 231.74 |
| Sat 06:30 | OKC @ LAC | **OKC** | **66.49%** | -5.32 | 224.47 |

Note: a minus sign under home margin means the visitor is favored. Total is full game including possible overtime. P is the selected winner's probability; see JSON for explicitly saved home-win probability.

## Data receipts and gates

- GitHub repository: `tctekes/nba-match-intelligence-data`, branch `main`.
- Snapshot index: `published/accepted_candidate_index.json`.
- **Snapshot JSON:** `published/accepted_candidates/2026-11-12-accepted-5aabf4a8efe0.json`.
- **Published snapshot JSON SHA-256:** `5aabf4a8efe0c11fe4ec998b9167b1d33eff255a15a5ebbf453889e9a9100db4`.
- Source team-game CSV SHA-256: `a9d4be339a8ae56b8a610f4b41b4ed48060b32be498e2e062d0036885106b895`.
- Source through NBA ET 2026-11-12. 174 raw completed, **172 accepted, 2 whole-game excluded**, 30 teams, accepted GP sum 344.
- Frozen model code SHA-256: `b6efd52df74f540c3bda711cd37a372e1ae7cbdbda134579c4c43bc7ff1eafef`.
- Frozen model parameter SHA-256: `259b0dcc561c2f0400b04d9b19aba59eef53973ba06075f5db97a73497d1c640`.
- Local real Python `nba_baseline_v01.predict_html` called once per matchup, using `runtime_league_center`, `feature_values` and `predictions`. Actual frozen code and parameter bytes were SHA-verified in the Python environment.
- 30 team input rows were **manually transferred at full numeric precision from the GitHub connector response** and checked for 30 unique teams and GP sum 344; published full JSON SHA is as reported by index, not independently reconstructed in the local Python file. This limitation is disclosed rather than concealed.
- [NBA official schedule](https://www.nba.com/games?date=2026-11-13) checked for nine fixtures and venues. No neutral venue for these home-arena group games.

## Injury and tactical context — deliberately separate from raw mathematical lock

The frozen baseline does **not** consume injuries or starting lineups. Contextual risks and basketball commentary may be appended **in a separate dated, non-mutating analysis file**; they must not modify probabilities in this immutable lock.

Before reporting a strong independent 'basketball confidence', inspect the latest verified league injury report and first-five news. Early-day reports suggest meaningful status problems for NYK@IND (Haliburton out), MIL@ORL (Banchero out; Suggs uncertain), CLE@MIA (Mobley out), GSW@SAS (Curry out), UTA@HOU (Markkanen and Jackson absent), and OKC@LAC (Holmgren, Jalen Williams absent). These are **provisional research flags** and NOT modeled inputs, and may change before tip.

**Retro scoring:** no editing this record after any of the games start. Once final, independently verify results; compute winner accuracy, home-win Brier, full-game total MAE, home-margin MAE. Tag overtime, last-minute lineup changes, quick rematches, and current-vs-previous source input days without applying hindsight retuning.

**Production:** No pointer promotion or parameter updates authorized.
