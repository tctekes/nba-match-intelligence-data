"""Unit checks for independent score/coverage probe; no network calls."""
import csv
import datetime as dt
import io
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import independent_coverage_probe as s

HEADERS = ["season","team","game_date","opponent","points","opponent_points","field_goals_made",
           "field_goal_attempts","three_point_makes","three_point_attempts","free_throws_made",
           "free_throw_attempts","offensive_rebounds","turnovers"]
BASE = [
    ["2026-27","BOS","2026-11-11","NYK","100","90","40","85","10","25","10","20","10","12"],
    ["2026-27","NYK","2026-11-11","BOS","90","100","35","83","10","25","10","20","11","14"],
]
DATE = dt.date(2026, 11, 11)
KEY = ("2026-11-11", ("BOS", "NYK"))


def csv_bytes(rows=BASE):
    f = io.StringIO()
    w = csv.writer(f)
    w.writerow(HEADERS)
    w.writerows(rows)
    return f.getvalue().encode()


def event(completed=True, home="NY", away="BOS", home_score="90", away_score="100"):
    return {
        "date": "2026-11-12T00:00:00Z",
        "season": {"type": 2},
        "status": {"type": {"completed": completed, "description": "Final" if completed else "In Progress"}},
        "competitions": [{
            "competitors": [
                {"homeAway":"home","team":{"abbreviation":home},"score":home_score},
                {"homeAway":"away","team":{"abbreviation":away},"score":away_score},
            ]
        }],
    }


class ProbeTests(unittest.TestCase):
    def test_reciprocal_game(self):
        m, rows = s.bsl_games(csv_bytes(), DATE)
        self.assertEqual(len(rows), 2)
        self.assertEqual(m[KEY], {"BOS":100, "NYK":90})

    def test_duplicate_half_rejected(self):
        with self.assertRaisesRegex(ValueError, "Missing/duplicate"):
            s.bsl_games(csv_bytes([BASE[0],BASE[1],BASE[0]]), DATE)

    def test_missing_half_rejected(self):
        with self.assertRaisesRegex(ValueError, "Missing/duplicate"):
            s.bsl_games(csv_bytes([BASE[0]]), DATE)

    def test_opponent_score_disagreement(self):
        invalid = [list(r) for r in BASE]
        invalid[0][5] = "91"
        with self.assertRaisesRegex(ValueError, "scores"):
            s.bsl_games(csv_bytes(invalid), DATE)

    def test_future_game_rejected(self):
        with self.assertRaisesRegex(ValueError, "outside complete cutoff"):
            s.bsl_games(csv_bytes(), dt.date(2026, 11, 10))

    def test_scoreboard_final(self):
        m = s.parse_espn_events({"events":[event()]}, DATE)
        self.assertEqual(m[KEY], {"BOS":100,"NYK":90})

    def test_unfinished_event_rejected(self):
        with self.assertRaisesRegex(ValueError, "not completed"):
            s.parse_espn_events({"events":[event(completed=False)]}, DATE)

    def test_date_timezone_filter(self):
        self.assertEqual(s.parse_espn_events({"events":[event()]}, dt.date(2026, 11, 12)), {})

    def test_identical_games_pass(self):
        m, _ = s.bsl_games(csv_bytes(), DATE)
        espn = s.parse_espn_events({"events":[event()]}, DATE)
        self.assertTrue(s.compare(m,espn)["pass"])

    def test_missing_game_fails(self):
        m,_ = s.bsl_games(csv_bytes(), DATE)
        self.assertFalse(s.compare(m,{})["pass"])

    def test_score_disagreement_fails(self):
        m,_ = s.bsl_games(csv_bytes(), DATE)
        self.assertEqual(len(s.compare(m,{KEY:{"BOS":99,"NYK":90}})["score_conflicts"]),1)


if __name__ == "__main__":
    unittest.main()
