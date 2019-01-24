import sys
import unittest
sys.path.insert(0, '/etc/Smash_stats')
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
        analyze_smashgg_tournament(self.db, self.bracket, 'test', True, testing=True)

    @classmethod
    def tearDownClass(self):
        utils.teardown_db(self.db)

    def test_evo_contestants(self):
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

    def test_evo_placings(self):
        return
        exp_placings = {'armada': 1,
                'mang0': 2,
                'hungrybox': 3,
                'mew2king': 4,
                'plup': 5,
                'lucky': 5,
                'sfat': 7,
                'la luna': 7,
                'leffen': 9,
                'prince f. abu': 9,
                'pewpewu': 9,
                'axe': 9,
                'swedish delight': 13,
                'duck': 13,
                'wizzrobe': 13,
                'westballz': 13,
                'rishi': 17,
                'ryan ford': 17,
                's2j': 17,
                'chudat': 17,
                'medz': 17,
                'amsa': 17,
                'shroomed': 17,
                'llod': 17,
                'antipopular': 1025,
                'vilent magician': 1025,
                'bcd': 1025}

        obs_placings = bracket_utils.get_tournament_placings(self.bracket)
        for key in exp_placings:
            self.assertTrue(key in obs_placings)
            self.assertEqual(exp_placings[key], obs_placings[key])
