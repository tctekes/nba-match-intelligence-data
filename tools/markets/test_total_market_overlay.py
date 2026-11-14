"""Tests for prospective O/U market overlay; no network calls or model changes."""
import json
import unittest

from total_market_overlay import build_overlay, grade_overlay


def sample():
    forecast = {
        "status": "LOCKED_PREGAME_SHADOW_NOT_PRODUCTION",
        "nba_local_date": "2026-11-14",
        "generated_at_utc": "2026-11-14T18:00:00Z",
        "model": "Frozen Model C v0.1",
        "model_file_sha256": "a"*64,
        "parameter_file_sha256": "b"*64,
        "current_snapshot_sha256": "c"*64,
        "games": [
            {"away": "DEN", "home": "NOP", "tipoff_utc": "2026-11-15T00:00:00Z",
             "expected_full_game_total": 240.5, "predicted_winner": "DEN",
             "win_probability": .75, "expected_home_margin": -8.5},
            {"away": "DAL", "home": "CLE", "tipoff_utc": "2026-11-15T00:30:00Z",
             "expected_full_game_total": 230.1, "predicted_winner": "CLE",
             "win_probability": .60, "expected_home_margin": 3.5},
        ],
    }
    market = {
        "nba_local_date": "2026-11-14",
        "cup_context": [
            {"away": "DEN", "home": "NOP", "is_nba_cup": False, "cup_stage": "NONE",
             "cup_group": None, "source_url": "https://www.nba.com/games?date=2026-11-14",
             "checked_at_utc": "2026-11-14T18:05:00Z"},
            {"away": "DAL", "home": "CLE", "is_nba_cup": False, "cup_stage": "NONE",
             "cup_group": None, "source_url": "https://www.nba.com/games?date=2026-11-14",
             "checked_at_utc": "2026-11-14T18:05:00Z"},
        ],
        "quotes": [
            {"away": "DEN", "home": "NOP", "market_kind": "FULL_GAME_INCLUDING_OT",
             "is_main_line": True, "bookmaker": "Example European book",
             "source_url": "https://example.org/den-nop",
             "captured_at_utc": "2026-11-14T19:00:00Z",
             "line": 233.5, "over_decimal": 1.92, "under_decimal": 1.94},
            {"away": "DAL", "home": "CLE", "market_kind": "FULL_GAME_INCLUDING_OT",
             "is_main_line": True, "bookmaker": "Example European book",
             "source_url": "https://example.org/dal-cle",
             "captured_at_utc": "2026-11-14T19:00:00Z",
             "line": 232.5, "over_decimal": 1.91, "under_decimal": 1.93},
        ],
    }
    return forecast, market


def lock(f):
    return json.dumps(f, sort_keys=True).encode("utf-8")


def finals():
    return {
        "nba_local_date": "2026-11-14",
        "results": [
            {"away": "DEN", "home": "NOP", "status": "FINAL", "away_score": 125,
             "home_score": 115, "overtime_periods": 0, "source_url": "https://www.nba.com/game/den-vs-nop"},
            {"away": "DAL", "home": "CLE", "status": "FINAL", "away_score": 111,
             "home_score": 119, "overtime_periods": 1, "source_url": "https://www.nba.com/game/dal-vs-cle"},
        ],
    }


class TotalsOverlayTests(unittest.TestCase):
    def test_main_line_is_selected_and_small_gap_passes(self):
        f, m = sample()
        o = build_overlay(f, m, lock(f))
        self.assertEqual(o["games"][0]["selected_direction"], "OVER")
        self.assertEqual(o["games"][0]["delta"], 7.0)
        self.assertEqual(o["games"][1]["raw_direction"], "UNDER")
        self.assertEqual(o["games"][1]["selected_direction"], "PASS")
        self.assertTrue(o["original_model_outputs_unchanged"])
        self.assertEqual(o["model_file_sha256"], "a"*64)
        self.assertEqual(len(o["original_forecast_sha256"]), 64)

    def test_grade_including_ot_with_pass(self):
        f, m = sample()
        o = build_overlay(f, m, lock(f))
        r = grade_overlay(o, finals())
        self.assertEqual([x["grade"] for x in r["games"]], ["WIN", "PASS"])
        self.assertEqual(r["summary"]["selected_accuracy_excluding_push"], 1)
        self.assertEqual(r["summary"]["selection_coverage"], .5)

    def test_push_for_integer_line(self):
        f, m = sample()
        m["quotes"][0]["line"] = 240.0
        o = build_overlay(f, m, lock(f))
        # 240.5 model total -> gap 0.5 -> PASS, so require model delta>=5
        f["games"][0]["expected_full_game_total"] = 246.0
        o = build_overlay(f, m, lock(f))
        r = grade_overlay(o, finals())
        self.assertEqual(r["games"][0]["grade"], "PUSH")
        self.assertEqual(r["summary"]["selected_pushes"], 1)

    def test_absent_quote_is_verifiably_ungraded(self):
        f, m = sample()
        m["quotes"].pop()
        o = build_overlay(f, m, lock(f))
        self.assertEqual(o["games"][1]["market_status"], "MARKET_NOT_VERIFIED")
        r = grade_overlay(o, finals())
        self.assertEqual(r["games"][1]["grade"], "UNVERIFIED")

    def test_fail_closed_posttipoff_quote(self):
        f, m = sample()
        m["quotes"][0]["captured_at_utc"] = "2026-11-15T00:00:00Z"
        with self.assertRaisesRegex(ValueError, "after tipoff"):
            build_overlay(f, m, lock(f))

    def test_fail_closed_wrong_market_and_odds_format(self):
        f, m = sample()
        m["quotes"][0]["market_kind"] = "REGULATION_ONLY"
        with self.assertRaises(ValueError):
            build_overlay(f, m, lock(f))
        f, m = sample()
        m["quotes"][0]["over_decimal"] = -110
        with self.assertRaises(ValueError):
            build_overlay(f, m, lock(f))

    def test_cup_group_and_official_source_required(self):
        f, m = sample()
        m["cup_context"][0]["is_nba_cup"] = True
        m["cup_context"][0]["cup_stage"] = "GROUP_PLAY"
        m["cup_context"][0]["cup_group"] = "West B"
        self.assertTrue(build_overlay(f, m, lock(f))["games"][0]["is_nba_cup"])
        m["cup_context"][0]["source_url"] = "https://other.example.com/games"
        with self.assertRaisesRegex(ValueError, "official NBA"):
            build_overlay(f, m, lock(f))

    def test_no_hindsight_and_different_slate_fails(self):
        f, m = sample()
        f["generated_at_utc"] = "2026-11-15T00:00:00Z"
        with self.assertRaisesRegex(ValueError, "Forecast created after start"):
            build_overlay(f, m, lock(f))
        f, m = sample()
        m["nba_local_date"] = "2026-11-13"
        with self.assertRaisesRegex(ValueError, "slate date mismatch"):
            build_overlay(f, m, lock(f))

    def test_duplicate_fixture_and_missing_cup_rejected(self):
        f, m = sample()
        m["quotes"].append(dict(m["quotes"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            build_overlay(f, m, lock(f))
        f, m = sample()
        m["cup_context"].pop()
        with self.assertRaisesRegex(ValueError, "Cup context must cover"):
            build_overlay(f, m, lock(f))


if __name__ == "__main__":
    unittest.main()
