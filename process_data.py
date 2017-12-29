import logger
import constants
import get_results
import time
import copy
import bracket_utils
from get_ranks import get_ranks
from database_writer import DatabaseWriter
import re

LOG = logger.logger(__name__)

class processData(object):
    def __init__(self):
        print('loading constants for process')
        self.dated_base_scene = bracket_utils.get_list_of_named_scenes()
        self.list_of_scene = bracket_utils.get_list_of_scenes()
        self.db = DatabaseWriter()

    def process(self, bracket, scene):
        # Send this bracket to get_results
        get_results.process(bracket, scene, self.db)

        self.insert_placing_data(bracket)


    def insert_placing_data(self, bracket):
        # Get the html from the 'standings' of this tournament
        tournament_placings = bracket_utils.get_tournament_placings(bracket)

        for player, placing in tournament_placings.items():
            player = re.sub("['-]", '', player)
            sql = "INSERT INTO placings (url, player, place) VALUES " \
                    + " ('{}', '{}', '{}')".format(bracket, player, placing)

            self.db.exec(sql)

        print(tournament_placings)


    def process_ranks(self, scene):
        print("Dallas! About to process ranks")
        PLAYER1 = 0
        PLAYER2 = 1
        WINNER = 2
        DATE = 3
        SCENE = 4

        # Get every match from this scene
        sql = "SELECT * FROM matches WHERE scene = '"+ scene +"';"
        matches =  self.db.exec(sql)

        # Iterate through each match, and build up our dict
        win_loss_dict = {}
        for match in matches:
            p1 = match[PLAYER1]
            p2 = match[PLAYER2]
            winner = match[WINNER]
            date = match[DATE]

            #Add p1 to the dict
            if p1 not in win_loss_dict:
                win_loss_dict[p1] = {}

            if p2 not in win_loss_dict[p1]:
                win_loss_dict[p1][p2] = []

            # Add an entry to represent this match to p1
            win_loss_dict[p1][p2].append((date, winner == p1))
            print("appending to win loss dict {}".format((date, winner, p2)))

            # add p2 to the dict
            if p2 not in win_loss_dict:
                win_loss_dict[p2] = {}

            if p1 not in win_loss_dict[p2]:
                win_loss_dict[p2][p1] = []

            win_loss_dict[p2][p1].append((date, winner == p2))

        ranks = get_ranks(win_loss_dict)
        print('dallas - {}'.format(ranks))

