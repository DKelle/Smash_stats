import logger
import constants
import get_results
import time
import copy
import player_web
import bracket_utils
from get_ranks import get_ranks
from get_results import get_coalesced_tag, sanitize_tag
import re
from tweet import tweet

LOG = logger.logger(__name__)

class processData(object):
    def __init__(self, db):
        LOG.info('loading constants for process')
        self.dated_base_scene = bracket_utils.get_list_of_named_scenes()
        self.list_of_scene = bracket_utils.get_list_of_scenes()
        self.db = db

    def process(self, bracket, scene):
        # Send this bracket to get_results
        # We know the bracket is valid if it is from smashgg
        if 'smash.gg' in bracket:
            get_results.process(bracket, scene, self.db)
            self.insert_placing_data(bracket)

        else:
            html, status = bracket_utils.hit_url(bracket)
            if status == 200 and bracket_utils.is_valid(html):
                get_results.process(bracket, scene, self.db)
                self.insert_placing_data(bracket)

    def insert_placing_data(self, bracket):
        # Get the html from the 'standings' of this tournament
        tournament_placings = bracket_utils.get_tournament_placings(bracket)

        for player, placing in tournament_placings.items():
            player = sanitize_tag(player)

            # Coalesce tag
            player = get_coalesced_tag(player)
            sql = "INSERT INTO placings (url, player, place) VALUES " \
                    + " ('{}', '{}', '{}')".format(bracket, player, placing)

            self.db.exec(sql)

            if 'christmasmike' == player:
                if placing < 10:
                    msg = "Congrats on making {} dude! You're the best.".format(placing)
                    #tweet(msg)

        LOG.info("tournament placings for {} are {}".format(bracket, tournament_placings))


    def process_ranks(self, scene):
        PLAYER1 = 0
        PLAYER2 = 1
        WINNER = 2
        DATE = 3
        SCENE = 4

        LOG.info('About to start processing ranks for scene {}'.format(scene))
        # Get only the last n tournaments, so it doesn't take too long to process
        n = 5 if (scene == 'pro' or scene == 'pro_wiiu') else constants.TOURNAMENTS_PER_RANK
        recent_tournaments = bracket_utils.get_last_n_tournaments(self.db, n, scene)
        matches = bracket_utils.get_matches_from_urls(self.db, recent_tournaments)

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

            # add p2 to the dict
            if p2 not in win_loss_dict:
                win_loss_dict[p2] = {}

            if p1 not in win_loss_dict[p2]:
                win_loss_dict[p2][p1] = []

            win_loss_dict[p2][p1].append((date, winner == p2))

        # make sure if we already have calculated ranks for these players, we update the DB
        sql = "SELECT * FROM ranks WHERE scene = '{}'".format(str(scene))
        res = self.db.exec(sql)
        if len(res) > 0:
            sql = "DELETE FROM ranks WHERE scene = '{}'".format(str(scene))
            self.db.exec(sql)

        ranks = get_ranks(win_loss_dict)
        tag_rank_map = {}
        for i, x in enumerate(ranks):
            points, player = x
            rank = len(ranks) - i
            sql = "INSERT INTO ranks (scene, player, rank, points) VALUES ('{}', '{}', '{}', '{}');"\
                    .format(str(scene), str(player), int(rank), str(points))
            self.db.exec(sql)

            # Only count this player if this is the scene he/she belongs to
            sql = "SELECT scene FROM players WHERE tag='{}';".format(player)
            res = self.db.exec(sql)

            if len(res) == 0 or res[0][0] == scene:
                # Also create a list to update the player web
                map = {'rank':rank, 'total_ranked':len(ranks)}
                tag_rank_map[player] = map

        # TODO we need to update ranks for the web somehow
        player_web.update_ranks(tag_rank_map)
