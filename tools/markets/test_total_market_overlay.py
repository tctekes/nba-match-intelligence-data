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
             "line": 233.5, "over_decimal": 1.92, "under_decimal": 1.94,
             "analyst_review": {"direction": "OVER", "confidence": "MEDIUM",
               "rationale": "Model total exceeds the quote, with real uncertainty from both teams' shooting variance.",
               "reviewed_at_utc": "2026-11-14T19:01:00Z"}},
            {"away": "DAL", "home": "CLE", "market_kind": "FULL_GAME_INCLUDING_OT",
             "is_main_line": True, "bookmaker": "Example European book",
             "source_url": "https://example.org/dal-cle",
             "captured_at_utc": "2026-11-14T19:00:00Z",
             "line": 232.5, "over_decimal": 1.91, "under_decimal": 1.93,
             "analyst_review": {"direction": "UNDER", "confidence": "LOW",
               "rationale": "The model is only slightly below the line and no robust matchup edge is verified.",
               "reviewed_at_utc": "2026-11-14T19:01:00Z"}},
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
    def test_small_gap_always_has_reviewed_direction_not_pass(self):
        f, m = sample()
        o = build_overlay(f, m, lock(f))
        self.assertEqual(o["schema_version"], "nba-ou-shadow-overlay-v2")
        self.assertEqual(o["games"][0]["selected_direction"], "OVER")
        self.assertEqual(o["games"][0]["delta"], 7.0)
        self.assertEqual(o["games"][1]["raw_direction"], "UNDER")
        self.assertEqual(o["games"][1]["selected_direction"], "UNDER")
        self.assertEqual(o["games"][1]["analyst_confidence"], "LOW")
        self.assertFalse(o["confidence_is_calibrated"])
        self.assertTrue(o["original_model_outputs_unchanged"])
        self.assertEqual(o["model_file_sha256"], "a"*64)
        self.assertEqual(len(o["original_forecast_sha256"]), 64)

    def test_grade_including_overtime_and_confidence(self):
        f, m = sample()
        o = build_overlay(f, m, lock(f))
        r = grade_overlay(o, finals())
        self.assertEqual(r["schema_version"], "nba-ou-shadow-retro-v2")
        self.assertEqual([x["grade"] for x in r["games"]], ["WIN", "WIN"])
        self.assertEqual(r["summary"]["selected_accuracy_excluding_push"], 1)
        self.assertEqual(r["summary"]["selection_coverage"], 1)
        self.assertEqual(r["summary"]["qualitative_confidence_bins"]["MEDIUM"]["win"], 1)
        self.assertEqual(r["summary"]["qualitative_confidence_bins"]["LOW"]["win"], 1)

    def test_push_for_integer_line(self):
        f, m = sample()
        m["quotes"][0]["line"] = 240.0
        f["games"][0]["expected_full_game_total"] = 246.0
        o = build_overlay(f, m, lock(f))
        r = grade_overlay(o, finals())
        self.assertEqual(r["games"][0]["grade"], "PUSH")
        self.assertEqual(r["summary"]["selected_pushes"], 1)

    def test_absent_quote_is_unverified_not_fake_pass(self):
        f, m = sample()
        m["quotes"].pop()
        o = build_overlay(f, m, lock(f))
        self.assertEqual(o["games"][1]["market_status"], "MARKET_NOT_VERIFIED")
        self.assertIsNone(o["games"][1]["selected_direction"])
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

    def test_missing_review_or_invalid_confidence_rejected(self):
        f, m = sample()
        del m["quotes"][0]["analyst_review"]
        with self.assertRaisesRegex(ValueError, "review required"):
            build_overlay(f, m, lock(f))
        f, m = sample()
        m["quotes"][0]["analyst_review"]["confidence"] = "CERTAIN"
        with self.assertRaisesRegex(ValueError, "confidence"):
            build_overlay(f, m, lock(f))

    def test_review_has_to_be_after_quote_and_before_tip(self):
        f, m = sample()
        m["quotes"][0]["analyst_review"]["reviewed_at_utc"] = "2026-11-14T18:00:00Z"
        with self.assertRaisesRegex(ValueError, "review must follow"):
            build_overlay(f, m, lock(f))
        f, m = sample()
        m["quotes"][0]["analyst_review"]["reviewed_at_utc"] = "2026-11-15T00:00:00Z"
        with self.assertRaisesRegex(ValueError, "review must follow"):
            build_overlay(f, m, lock(f))

    def test_analyst_can_disagree_with_raw_direction_and_zero_gap(self):
        f, m = sample()
        m["quotes"][0]["analyst_review"]["direction"] = "UNDER"
        o = build_overlay(f, m, lock(f))
        self.assertEqual(o["games"][0]["raw_direction"], "OVER")
        self.assertEqual(o["games"][0]["selected_direction"], "UNDER")
        self.assertEqual(grade_overlay(o, finals())["games"][0]["grade"], "LOSS")
        f, m = sample()
        f["games"][0]["expected_full_game_total"] = 233.5
        o = build_overlay(f, m, lock(f))
        self.assertEqual(o["games"][0]["raw_direction"], "NEUTRAL")
        self.assertEqual(o["games"][0]["selected_direction"], "OVER")


if __name__ == "__main__":
    unittest.main()
