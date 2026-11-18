# NBA Match Intelligence — Multi-Source Recovery v0.2

Implementation date: 18 November 2026. Experimental SHADOW only. Frozen Model C v0.1 and all historic forecast locks remain unchanged.

## Root cause, established by GitHub Actions

The BoxScore Lab (BSL) 2026–27 team-game CSV and standings stayed internally consistent at 197 completed NBA games through November 15. But the ESPN completed-game scoreboard covered 210 games through November 17. Thus the pipeline's independent full-season coverage gate correctly refused to publish: Orlando @ Boston, ESPN 401909994, was only the first of THIRTEEN whole games absent from BSL. Direct official NBA CDN backfill was independently tested and returned HTTP 403 on GitHub Actions, so it is not used.

Independent GitHub release datasets, which ARE accessible from GitHub Actions:
- ESPN team boxes: sportsdataverse-data / espn_nba_team_boxscores / team_box_2027.csv
- NBA Stats team boxes: sportsdataverse-data / nba_stats_team_boxscores / team_boxscores_2027.csv

Both releases covered 210 games. All 210 joined with correct normalized teams, final scores and home/away identity.

## Durable fix and validation protocol

1. The existing BSL game and standings files are still acquired, SHA-receipted and checked against each other for all 30 teams. Existing BSL raw rows are NEVER silently repaired.
2. Every completed ESPN scoreboard game through the previous fully closed NBA-local date must be accounted for. No live fixture or partial day enters the model.
3. Games present in BSL continue to use original BSL stats, with all eight required box fields independently checked against live ESPN game summaries. Conflicting whole games are quarantined as before.
4. Any COMPLETED game missing from BSL is reconstructed as TWO whole team rows from the ESPN team-box release. It must match ESPN event ID, league date, teams, final scores, game side and the 2*FGM+3PM+FTM scoring identity.
5. Each recovered game must also uniquely match an NBA Stats-origin team-box pair by team, exact score and home designation. Independently compare FGM, FGA, 3PM, 3PA, FTM, FTA, OREB and player turnovers. The ESPN historical model input is TEAM-INCLUSIVE turnovers. Verify the ESPN decomposition: total_turnovers = turnovers + team_turnovers, verify player turnovers against NBA Stats, and compare all eight model fields with live ESPN summary. The ESPN team-turnover component itself is NOT independently corroborated by the NBA Stats release; this provenance limitation is explicitly recorded. Do not substitute NBA player turnovers for the team-inclusive total.
6. Conflicting core stats, duplicated identities, ambiguous official team match, missing independent data, or misaligned dates fail closed. Any detected field conflict quarantines the WHOLE game for both teams. Cumulative excluded-game caps remain active.
7. Convert fallback date/team-pair keys to the original Task08 scoreboard validator's flat keys explicitly. Check full ESPN universe, source SHA receipts, raw=accepted+excluded, 30 teams, sum(GP)=2*accepted, JSON SHA-256 and fallback manifests before commit.
8. Publish only immutable experimental accepted candidates and the accepted_candidate_index.json pointer. Do NOT advance any production pointer or modify the frozen model.

## First verified recovery

GitHub Actions run 44356110673 succeeded: 210 completed through 17 November 2026, 197 BSL-present + 13 whole-game fallbacks, 208 accepted, 2 fully excluded, 30 teams and 416 accepted team observations. The original Boston–Orlando game is included. The excluded games are 30 October CHA–WAS and 16 November GSW–NOP. Both sources' release SHA-256s and the full fallback game list are in the published candidate JSON.

The CI additionally includes 8 focused recovery tests, the 6 original whole-game-exclusion tests and 10 Task08 validation tests. Recovered-vs-original score-key equivalence now has dedicated regression coverage.

## Operating limitations

This redesign removes the single-provider completeness dependency, but does not guarantee release timeliness or solve an outage of multiple independent sources. If verification is unavailable or fails, hold model forecasts at NO-GO rather than inventing figures. Check the next 20:23 and 20:53 TSİ scheduled runs to confirm sustained daily reliability. This remains a SHADOW candidate and is not a production promotion.

Paths: tools/task08/multi_source_recovery.py, tools/task08/build_accepted_candidate.py, tools/task08/test_multi_source_recovery.py, tools/task08/test_accepted_candidate.py, .github/workflows/accepted-candidate.yml and published/accepted_candidate_index.json.
