"""Tests of whole-game quarantine and fail-closed daily model inputs."""
import datetime as dt
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parent))
import build_accepted_candidate as c

def one_game(date,a,b):
    def row(team,opp,points,op):
        return {
          "season":"2026-27","game_date":date,"team":team,"opponent":opp,
          "points":str(points),"opponent_points":str(op),
          "field_goals_made":str((points-20)//2),"field_goal_attempts":"90",
          "three_point_makes":"10","three_point_attempts":"25",
          "free_throws_made":"10","free_throw_attempts":"20",
          "offensive_rebounds":"10","turnovers":"10",
        }
    return row(a,b,100,90),row(b,a,90,100)

def fixtures():
    teams=c.model.TEAMS
    games=[]
    for d in ("2026-11-10","2026-11-11"):
        for i in range(0,30,2):
            games += list(one_game(d,teams[i],teams[i+1]))
    return games

class AcceptedTests(unittest.TestCase):
    def test_grouping_reciprocal(self):
        p=c.groups_of_pairs(fixtures())
        self.assertEqual(len(p),30)

    def test_exclude_entire_game_and_keep_all_teams(self):
        p=c.groups_of_pairs(fixtures())
        k=sorted(p)[0]
        rates,count=c.accepted_aggregates(p,{k:{"test":1}})
        self.assertEqual(count,29)
        self.assertEqual(len(rates),30)
        for t in k[1]:
            self.assertEqual(rates[t]["n"],1)
        self.assertEqual(sum(r["n"] for r in rates.values()),58)

    def test_all_games_included(self):
        p=c.groups_of_pairs(fixtures())
        rates,count=c.accepted_aggregates(p,{})
        self.assertEqual(count,30)
        self.assertTrue(all(r["n"]==2 for r in rates.values()))

    def test_insufficient_teams_fail_closed(self):
        p=c.groups_of_pairs(fixtures())
        a,b=sorted(p)[0][1]
        excluded={k:{} for k in p if a in k[1] or b in k[1]}
        with self.assertRaisesRegex(ValueError,"lacks"):
            c.accepted_aggregates(p,excluded)

    def test_summary_one_team_conflict_excludes_game(self):
        a,b=one_game("2026-11-11","BOS","NYK")
        k=("2026-11-11",("BOS","NYK"))
        g={k:[a,b]}
        stats=[
            {"name":"fieldGoalsMade-fieldGoalsAttempted","displayValue":"40-90"},
            {"name":"threePointFieldGoalsMade-threePointFieldGoalsAttempted","displayValue":"10-25"},
            {"name":"freeThrowsMade-freeThrowsAttempted","displayValue":"10-20"},
            {"name":"offensiveRebounds","displayValue":"10"},
            {"name":"totalTurnovers","displayValue":"10"},
        ]
        other=[dict(x) for x in stats]
        other[-1]["displayValue"]="11"
        response={"boxscore":{"teams":[
          {"team":{"abbreviation":"BOS"},"statistics":other},
          {"team":{"abbreviation":"NYK"},"statistics":stats},
        ]}}
        with patch.object(c.independent.shared,"get_bytes",return_value=json.dumps(response).encode()),patch.object(c.time,"sleep"):
            excluded,seen=c.compare_full_box_stats(g,{k:"999"})
        self.assertEqual(seen,2)
        self.assertIn(k,excluded)
        self.assertIn("turnovers",excluded[k]["mismatches"]["BOS"])

    def test_missing_summary_refuses_all(self):
        a,b=one_game("2026-11-11","BOS","NYK")
        k=("2026-11-11",("BOS","NYK"))
        with patch.object(c.independent.shared,"get_bytes",return_value=b'{"boxscore":{"teams":[]}}'):
            with self.assertRaisesRegex(ValueError,"Missing independent"):
                c.compare_full_box_stats({k:[a,b]},{k:"999"})

if __name__=="__main__":
    unittest.main()
