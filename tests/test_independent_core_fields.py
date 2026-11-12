"""No-network unit checks for eight independent NBA core box fields."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"/"task08"))
import independent_core_fields as audit

def record(overrides=None):
    d={
      "fieldGoalsMade-fieldGoalsAttempted":"37-90",
      "threePointFieldGoalsMade-threePointFieldGoalsAttempted":"11-35",
      "freeThrowsMade-freeThrowsAttempted":"16-22",
      "offensiveRebounds":"15",
      "turnovers":"14",
      "teamTurnovers":"1",
      "totalTurnovers":"15",
    }
    d.update(overrides or {})
    return {"statistics":[{"name":k,"displayValue":v} for k,v in d.items()]}

class IndependentCoreTests(unittest.TestCase):
    def test_eight_fields(self):
        got=audit.espn_team_fields(record())
        self.assertEqual(len(got),8)
        self.assertEqual(got["field_goals_made"],37)
        self.assertEqual(got["field_goal_attempts"],90)
        self.assertEqual(got["turnovers"],15)

    def test_total_turnovers_not_player_only(self):
        got=audit.espn_team_fields(record())
        self.assertNotEqual(got["turnovers"],14)

    def test_missing_total_turnovers_fails(self):
        with self.assertRaisesRegex(ValueError,"totalTurnovers"):
            audit.espn_team_fields(record({"totalTurnovers":"-"}))

    def test_made_greater_than_attempts_fails(self):
        with self.assertRaisesRegex(ValueError,"makes exceed"):
            audit.espn_team_fields(record({"freeThrowsMade-freeThrowsAttempted":"23-22"}))

    def test_stat_conflict_identified(self):
        got=audit.espn_team_fields(record())
        row={k:str(v) for k,v in got.items()}
        row["field_goal_attempts"]="89"
        mismatches=audit.compare_team(row,got)
        self.assertEqual(mismatches["field_goal_attempts"],{"bsl":89,"espn":90})

    def test_missing_stat_fails(self):
        with self.assertRaisesRegex(ValueError,"offensiveRebounds"):
            audit.espn_team_fields(record({"offensiveRebounds":"unknown"}))

if __name__=="__main__":
    unittest.main()
