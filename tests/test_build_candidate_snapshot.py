"""No-network fail-closed publication tests for candidate snapshot."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"tools"))
import build_candidate_snapshot as b

class BuildCandidateTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.old=os.getcwd()
        os.chdir(self.tmp.name)
        self.standings=("team\n" + "\n".join(sorted(b.cov.TEAM_SET)) + "\n").encode()
        self.data=[{"game_date":"2026-11-11","team":"BOS","opponent":"NYK"},
                   {"game_date":"2026-11-11","team":"NYK","opponent":"BOS"}]
        self.rates={t:{"gp":1,"wins":1,"losses":0,"ortg":110.0,"drtg":108.0,"pace":99.0}
                    for t in b.cov.TEAM_SET}
        keys=("2026-11-11",("BOS","NYK"))
        self.mocks=[
            patch.object(b.cov,"get_bytes",side_effect=[b"example-game-csv",self.standings]),
            patch.object(b.cov,"bsl_games",return_value=({keys:{"BOS":100,"NYK":90}},self.data)),
            patch.object(b.cov,"esn_games",return_value=({keys:{"BOS":100,"NYK":90}},23)),
            patch.object(b.parity,"reconstruct",return_value=self.rates),
            patch.object(b.parity,"audit",return_value=[]),
        ]
        self.active=[m.start() for m in self.mocks]
    def tearDown(self):
        for m in reversed(self.mocks):m.stop()
        os.chdir(self.old)
        self.tmp.cleanup()

    def test_success_publishes_candidate_not_production(self):
        idx=b.build()
        self.assertEqual(idx["status"],"EXPERIMENTAL_CANDIDATE_NOT_PRODUCTION")
        self.assertTrue(Path(idx["markdown_path"]).exists())
        self.assertTrue(Path(idx["json_path"]).exists())
        self.assertFalse(Path("published/latest_valid.json").exists())
        data=json.loads(Path(idx["json_path"]).read_text())
        self.assertEqual(len(data["teams"]),30)
        self.assertEqual(data["quality"]["independent_espn_box_stat_field_parity"],"NOT_CHECKED")

    def test_missing_game_blocks_everything(self):
        with patch.object(b.cov,"compare",return_value={"pass":False,"missing_from_bsl":["BOS-NYK"]}):
            with self.assertRaisesRegex(ValueError,"FAIL CLOSED"):
                b.build()
        self.assertFalse(Path("published/candidate_index.json").exists())

    def test_metric_mismatch_blocks_everything(self):
        with patch.object(b.parity,"audit",return_value=["BOS drtg"]):
            with self.assertRaisesRegex(ValueError,"FAIL CLOSED"):
                b.build()
        self.assertFalse(Path("published/candidate_index.json").exists())

    def test_empty_standings_blocks(self):
        self.active[0].side_effect=[b"example-game-csv",b"team\nBOS\n"]
        with self.assertRaisesRegex(ValueError,"duplicated standings team|Not exactly 30"):
            b.build()
        self.assertFalse(Path("published/latest_valid.json").exists())

if __name__=="__main__":
    unittest.main()
