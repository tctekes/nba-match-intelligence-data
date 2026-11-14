# NBA Match Intelligence — NBA Cup / full-game O-U overlay helper

Validated by the [overlay CI workflow](../../.github/workflows/total-market-overlay-ci.yml). Pure Python 3.12 stdlib. **No bookmaker API or scraper**: quotes must be obtained and verified before passing them to the helper. Frozen Model C remains unchanged. See [full protocol](../../docs/NBA_CUP_AND_TOTALS_MARKET_PROTOCOL_V02.md).

## 1. Inputs

`forecast.json`: original, already **pre-tip locked** file generated using the real frozen Model C (schema `nba-locked-shadow-forecast-v1`, status `LOCKED_PREGAME_SHADOW_NOT_PRODUCTION`, `games[]` with teams/tipoff/model totals; hashes and model timestamp). Do not compute new forecasts from post-tip data.

`market.json`: use the following structure, with **NBA-local date** matching the forecast. The values below are **SYNTHETIC EXAMPLE VALUES**, not real market quotes, and must never be counted as picks. Review rationale is also invented only to show schema shape.

```json
{
  "nba_local_date": "2026-11-14",
  "cup_context": [
    {
      "away": "DEN",
      "home": "NOP",
      "is_nba_cup": false,
      "cup_stage": "NONE",
      "cup_group": null,
      "source_url": "https://www.nba.com/games?date=2026-11-14",
      "checked_at_utc": "2026-11-14T18:05:00Z"
    }
  ],
  "quotes": [
    {
      "away": "DEN",
      "home": "NOP",
      "bookmaker": "EXAMPLE ONLY - European bookmaker",
      "source_url": "https://example.org/pregame-total",
      "captured_at_utc": "2026-11-14T18:10:00Z",
      "market_kind": "FULL_GAME_INCLUDING_OT",
      "is_main_line": true,
      "line": 233.5,
      "over_decimal": 1.92,
      "under_decimal": 1.94,
      "analyst_review": {
        "direction": "OVER",
        "confidence": "MEDIUM",
        "rationale": "The independent model is above the market; transition potential supports Over, but shooting variability is a risk.",
        "reviewed_at_utc": "2026-11-14T18:15:00Z"
      }
    }
  ]
}
```

- Cup context **must have exactly one record for every model game**, from official NBA schedule, even for non-Cup days; stage is `NONE` or one of `GROUP_PLAY`, `QUARTERFINAL`, `SEMIFINAL`, `CHAMPIONSHIP`. A GROUP_PLAY game requires a verified `cup_group`.
- Quotes may cover a subset of the games. Missing quote => `MARKET_NOT_VERIFIED`, no selected direction; never manufacture a line or call an unverified market PASS.
- A quote must be a **real pre-tip main-line full-game including OT** market with a named book, actual URL and UTC capture time; the helper can verify shape and chronology, **not whether the price was truly displayed by that bookmaker**. Operator/project must preserve a source receipt.
- Make sure quote timestamps precede actual tipoff. No live odds, no regulation-only markets, no alternate line optimizations.
- Decimal odds (European format) only; different sources/bookmakers can offer different lines. Use predeclared book precedence, then lock.
- Example shows one fixture; actual market file must repeat `cup_context` for every fixture.

## 2. Overlay and grade commands

```bash
python -B tools/markets/total_market_overlay.py overlay \
  --forecast /path/to/existing-original-pregame-forecast.json \
  --market /path/to/verified-pregame-market.json \
  --output /path/to/NEW-nba-ou-shadow-overlay.json
```

The overlay links to SHA-256 of the exact original forecast file, preserves frozen hashes, validates Cup data, and requires a **pretip analyst review** with `OVER`/`UNDER`, `LOW`/`MEDIUM`/`HIGH` confidence, evidence/counterargument, and reviewed UTC timestamp **after quote capture**. It records independent model raw direction too. **No 5-point PASS threshold; no invented calibrated probabilities.** It validates format/timestamps but **does not independently verify bookmaker quote authenticity**. Results contain no final scores.

After matches end, prepare `finals.json`:

```json
{
  "nba_local_date": "2026-11-14",
  "results": [
    {
      "away": "DEN",
      "home": "NOP",
      "status": "FINAL",
      "away_score": 125,
      "home_score": 115,
      "overtime_periods": 0,
      "source_url": "https://www.nba.com/game/synthetic-example"
    }
  ]
}
```

**Example final scores are synthetic**, not the real Nov. 14 match.

```bash
python -B tools/markets/total_market_overlay.py grade \
  --overlay /path/to/existing-locked-ou-overlay.json \
  --finals /path/to/independently-verified-finals.json \
  --output /path/to/NEW-nba-ou-retrospective.json
```

Grades selected picks `WIN` / `LOSS` / `PUSH`; unquoted fixtures are `UNVERIFIED` (not picks). The retrospective also tracks accuracy by LOW/MEDIUM/HIGH qualitative confidence. Final scores **include overtime**. File creation **refuses existing output paths** to avoid silent overwrites. GitHub append-only publication requires separate explicit commit and readback.

## 3. CI checks

```bash
cd tools/markets
python -B -m unittest -v test_total_market_overlay
```

Twelve unit tests: direction even when model/market gap is small, independent analyst lean, confidence bins, immutable forecast linkage, OT and integer-line PUSH, unverified quotes, no posttip market/review, European odds, NBA Cup group/source gating, no hindsight and duplicate/missing fixtures.

## Limitations and release gates

This helper does **not** automatically access bookmakers, execute Model C, generate an NBA schedule, change historical predictions, or upload to GitHub. It only handles prospective market overlay and deterministic retrospectives **once reliable source data are supplied**. The model and market outputs should be combined in the ChatGPT Project's upcoming permanent instructions, then run a real pretip 5+ game shadow pilot and verify that GitHub stores the lock **before** any tipoffs. No O/U hit rate for pre-Nov 14 slates: they have no locked market quotes.
