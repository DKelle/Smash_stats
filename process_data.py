import logger
import constants
import get_results
import time
import copy
import bracket_utils
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


        #found_placing = False
        #for tag in tags:
        #    player_placing = tournament_placings[tag.lower()] if tag.lower() in tournament_placings else None
        #    if player_placing:
        #        found_placing = True
        #        player_placings.append((url, player_placing))
        #if not found_placing:
        #    print('cant determine placing in bracket ' + url)

        #for url, placing in sorted(player_placings, key=lambda x : x[-1]):

