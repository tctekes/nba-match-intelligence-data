"""Synthetic regression tests: no networking or publication."""
import copy
import unittest
import dual_source_backfill_probe as p

def nba_team(team,score,made):
    return {"teamTricode":team,"score":score,"statistics":{
        "fieldGoalsMade":made,"fieldGoalsAttempted":90,
        "threePointersMade":10,"threePointersAttempted":25,
        "freeThrowsMade":10,"freeThrowsAttempted":20,
        "reboundsOffensive":10,"turnovers":10}}

def espn_team(team,made):
    return {"team":{"abbreviation":team},"statistics":[
        {"name":"fieldGoalsMade-fieldGoalsAttempted","displayValue":f"{made}-90"},
        {"name":"threePointFieldGoalsMade-threePointFieldGoalsAttempted","displayValue":"10-25"},
        {"name":"freeThrowsMade-freeThrowsAttempted","displayValue":"10-20"},
        {"name":"offensiveRebounds","displayValue":"10"},
        {"name":"totalTurnovers","displayValue":"10"}]}

def fixtures():
    nba={"game":{"gameId":"0022600245","gameStatus":3,
            "gameTimeUTC":"2026-11-17T00:00:00Z",
            "homeTeam":nba_team("BOS",100,40),
            "awayTeam":nba_team("ORL",90,35)}}
    espn={"boxscore":{"teams":[espn_team("BOS",40),espn_team("ORL",35)]}}
    expected={"scores":{"BOS":100,"ORL":90}}
    return nba,espn,expected

class DualSourceProbeTests(unittest.TestCase):
    def test_16_verified_fields_in_two_reciprocal_rows(self):
        nba,espn,expected=fixtures()
        rows=p.validated_pair(nba,espn,expected,"0022600245","2026-11-16")
        self.assertEqual(len(rows),2)
        self.assertEqual(sum(int(r["points"]) for r in rows),190)

    def test_espn_one_stat_mismatch_is_fail_closed(self):
        nba,espn,expected=fixtures()
        espn["boxscore"]["teams"][0]["statistics"][-1]["displayValue"]="11"
        with self.assertRaisesRegex(ValueError,"Independent 8-field mismatch"):
            p.validated_pair(nba,espn,expected,"0022600245","2026-11-16")

    def test_nba_score_disagreement_is_fail_closed(self):
        nba,espn,expected=fixtures()
        expected["scores"]["BOS"]=101
        with self.assertRaisesRegex(ValueError,"Official NBA score mismatch"):
            p.validated_pair(nba,espn,expected,"0022600245","2026-11-16")

    def test_not_final_is_fail_closed(self):
        nba,espn,expected=fixtures()
        nba["game"]["gameStatus"]=2
        with self.assertRaisesRegex(ValueError,"not final"):
            p.validated_pair(nba,espn,expected,"0022600245","2026-11-16")

    def test_schedule_matches_et_day(self):
        nba,_,_=fixtures()
        schedule={"leagueSchedule":{"gameDates":[{"games":[{
           "gameId":"0022600245","gameDateTimeUTC":"2026-11-17T00:00:00Z",
           "homeTeam":{"teamTricode":"BOS"},"awayTeam":{"teamTricode":"ORL"}}]}]}}
        got=p.scheduled_nba_games(schedule,"2026-11-16")
        self.assertEqual(got,{("2026-11-16",("BOS","ORL")):"0022600245"})

    def test_schedule_reject_duplicate(self):
        schedule={"leagueSchedule":{"gameDates":[{"games":[
           {"gameId":"0022600245","gameDateTimeUTC":"2026-11-17T00:00:00Z",
            "homeTeam":{"teamTricode":"BOS"},"awayTeam":{"teamTricode":"ORL"}},
           {"gameId":"0022600301","gameDateTimeUTC":"2026-11-17T00:00:00Z",
            "homeTeam":{"teamTricode":"BOS"},"awayTeam":{"teamTricode":"ORL"}}]}]}}
        with self.assertRaisesRegex(ValueError,"Duplicate official"):
            p.scheduled_nba_games(schedule,"2026-11-16")

if __name__=="__main__":
    unittest.main()
