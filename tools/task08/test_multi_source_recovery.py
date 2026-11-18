"""Synthetic fail-closed regression tests for generalized secondary-source recovery."""
import copy,unittest
from unittest.mock import patch
import multi_source_recovery as r

def fixture():
    day="2026-11-16"
    e=[]
    n=[]
    base=[
     ("BOS","home",105,38,90,20,56,9,17,9,11,1),
     ("ORL","away",115,41,82,13,34,20,25,10,13,1),
    ]
    for team,side,pts,fgm,fga,thm,tha,ftm,fta,oreb,tov,teamtov in base:
        e.append({"game_id":"401909994","season":"2027","season_type":"2","game_date":day,
        "team_home_away":side,"team_abbreviation":team,"team_score":str(pts),
        "field_goals_made":str(fgm),"field_goals_attempted":str(fga),
        "three_point_field_goals_made":str(thm),"three_point_field_goals_attempted":str(tha),
        "free_throws_made":str(ftm),"free_throws_attempted":str(fta),
        "offensive_rebounds":str(oreb),"turnovers":str(tov),"team_turnovers":str(teamtov),
        "total_turnovers":str(tov+teamtov)})
        n.append({"game_id":"0022600245","season":"2027","season_type_id":"2",
        "team_tricode":team,"side":side,"points":str(pts),
        "field_goals_made":str(fgm),"field_goals_attempted":str(fga),
        "three_pointers_made":str(thm),"three_pointers_attempted":str(tha),
        "free_throws_made":str(ftm),"free_throws_attempted":str(fta),
        "rebounds_offensive":str(oreb),"turnovers":str(tov)})
    return e,n

class SourceRecoveryTests(unittest.TestCase):
    def match(self,e,n):
        return r.one_fallback("401909994",e,r.official_index({"0022600245":n}))

    def test_recovery_valid_two_team_model_c_formulas(self):
        e,n=fixture()
        key,pair,receipt=self.match(e,n)
        self.assertEqual(key,("2026-11-16",("BOS","ORL")))
        self.assertEqual(receipt["mismatches"],{})
        self.assertEqual({x["team"]:x["turnovers"] for x in pair},{"BOS":"12","ORL":"14"})
        self.assertEqual({x["team"]:x["points"] for x in pair},{"BOS":"105","ORL":"115"})

    def test_independent_one_stat_mismatch_quarantines_whole_game(self):
        e,n=fixture();n[0]["field_goals_attempted"]="91"
        _,pair,receipt=self.match(e,n)
        self.assertEqual(len(pair),2)
        self.assertIn("BOS",receipt["mismatches"])
        self.assertIn("field_goal_attempts",receipt["mismatches"]["BOS"])

    def test_player_turnovers_independent_audit(self):
        e,n=fixture();n[1]["turnovers"]="12"
        _,_,rec=self.match(e,n)
        self.assertIn("player_turnovers",rec["mismatches"]["ORL"])

    def test_total_turnover_decomposition_mismatch(self):
        e,n=fixture();e[0]["team_turnovers"]="2"
        _,_,rec=self.match(e,n)
        self.assertIn("total_turnovers_decomposition",rec["mismatches"]["BOS"])

    def test_source_missing_fails_closed(self):
        e,n=fixture()
        ids={("2026-11-16",("BOS","ORL")):"401909994"}
        with patch.object(r,"source_csv",side_effect=[([], "h1"),(n,"h2")]):
            with self.assertRaisesRegex(ValueError,"missing completed game"):
                r.restore_missing({},ids)

    def test_ambiguous_official_pair_fails_closed(self):
        e,n=fixture()
        index=r.official_index({"0022600245":n, "0022600250":n})
        with self.assertRaisesRegex(ValueError,"missing or ambiguous"):
            r.one_fallback("401909994",e,index)

    def test_no_missing_game_does_not_fetch(self):
        k=("2026-11-16",("BOS","ORL"))
        with patch.object(r,"source_csv",side_effect=AssertionError("should not download")):
            a,b,c=r.restore_missing({k:[]},{k:"401909994"})
            self.assertEqual((len(a),len(b),c["recovered"]),(0,0,0))

    def test_bsl_only_game_fail_closed(self):
        k=("2026-11-16",("BOS","ORL"))
        with self.assertRaisesRegex(ValueError,"Unexplained BSL-only"):
            r.restore_missing({k:[]},{})
if __name__=="__main__":unittest.main()
