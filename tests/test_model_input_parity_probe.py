"""Small deterministic tests of the Model C input reconstruction."""
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import model_input_parity_probe as p


def sample():
    return [
        dict(team="BOS", opponent="NYK", game_date="2026-11-11",
             points="100", opponent_points="90", field_goal_attempts="85",
             free_throw_attempts="20", offensive_rebounds="10", turnovers="12"),
        dict(team="NYK", opponent="BOS", game_date="2026-11-11",
             points="90", opponent_points="100", field_goal_attempts="83",
             free_throw_attempts="20", offensive_rebounds="11", turnovers="14"),
    ]


class MetricTests(unittest.TestCase):
    def test_recomputed_possessions_per_game(self):
        r=p.reconstruct(sample())
        pos=((85+.44*20-10+12)+(83+.44*20-11+14))/2
        self.assertAlmostEqual(r["BOS"]["pace"],pos,10)
        self.assertAlmostEqual(r["NYK"]["pace"],pos,10)

    def test_arithmetic_efficiency_and_win_loss(self):
        r=p.reconstruct(sample())
        self.assertEqual((r["BOS"]["gp"],r["BOS"]["wins"],r["BOS"]["losses"]),(1,1,0))
        self.assertAlmostEqual(r["BOS"]["ortg"],100*100/r["BOS"]["pace"],10)
        self.assertAlmostEqual(r["NYK"]["drtg"],100*100/r["NYK"]["pace"],10)

    def test_disallow_nonfinite_stats(self):
        x=sample();x[0]["turnovers"]="nan"
        with self.assertRaisesRegex(ValueError,"Non-finite"):
            p.reconstruct(x)

    def test_duplicate_half(self):
        with self.assertRaisesRegex(ValueError,"reciprocal"):
            p.reconstruct([sample()[0]])

    def test_audit_rejects_missing_teams(self):
        r=p.reconstruct(sample())
        with self.assertRaisesRegex(ValueError,"30"):
            p.audit({},r)


if __name__=="__main__":
    unittest.main()
