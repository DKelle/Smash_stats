import sys
import unittest
sys.path.insert(0, '/home/ubuntu/venv/Smash_stats')
import bracket_utils
from process_data import processData
from utils import utils
from database_writer import get_db
from get_results import analyze_smashgg_tournament

class TestAnalyzeSmashgg(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.bracket = "https://smash.gg/tournament/evo-2017/events/super-smash-bros-melee"
        self.db = get_db('test_analyze_smashgg')
        utils.setup_db(self.db)

    #@classmethod
    #def tearDownClass(self):
    #    utils.teardown_db(self.db)

    def test_analyze_evo(self):
        analyze_smashgg_tournament(self.db, self.bracket, 'test', True, testing=True)

        # Armada beat Mango in grand finals, and winners finals. Make sure we have these matches
        sql = "SELECT * FROM matches WHERE player1='armada' and player2='mang0'"
        res = self.db.exec(sql)
        self.assertEqual(len(res), 2)

        # Check that amrada, hbox, mango, and m2k are all players in the tournament
        players = ['armada', 'mang0', 'mew2king', 'hungrybox']
        for p in players:
            sql = "SELECT * FROM players WHERE tag='{}';".format(p)
            res = self.db.exec(sql)

            self.assertEqual(len(res), 1)

        # Make sure these players are not in the tournament
        players = ['christmasmike', 'ashleyismylove', 'meleeisgood']
        for p in players:
            sql = "SELECT * FROM players WHERE tag='{}';".format(p)
            res = self.db.exec(sql)

            self.assertEqual(len(res), 0)
