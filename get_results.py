import bracket_utils
import copy
import json
import datetime
import re
import pysmash

from logger import logger
from pprint import pprint
from constants import TAGS_TO_COALESCE
from player_web import update_web, update_group
import os

smash = None
id_tag_dict = {}
sanitized_tag_dict = {}
debug = False 

LOG = logger(__name__)

def sanitize_tag(tag):
    tag = ''.join([i if ord(i) < 128 else ' ' for i in tag])
    return re.sub("[^a-z A-Z 0-9]",'',tag.lower())

def analyze_smashgg_tournament(db, url, scene, dated, urls_per_player=False):
    global smash
    if smash == None:
        smash = pysmash.SmashGG()

    winner_loser_pairs = []
    # Exctract the tournament and event names
    # eg url:
    # https://smash.gg/tournament/pulsar-premier-league/events/rocket-league-3v3/brackets/68179
    # tournament name = pulsar-premier-leauge
    # event name = rocket-league-3v3
    url_parts = url.split('/')
    LOG.info("about to analyze smashgg bracket: {}".format(url))

    if 'tournament' in url_parts and 'events' in url_parts:
        t = url_parts[url_parts.index('tournament')+1]
        e = url_parts[url_parts.index('events')+1]

        # The event will be either 'melee' or 'wiiu'

        players = smash.tournament_show_players(t, e)

        # Check if these players are already in the players table
        scenes = bracket_utils.get_list_of_scene_names()
        for player in players:
            p = sanitize_tag(player['tag'].lower())
            p = re.sub("['-_]", '', p)
            LOG.info('dallas: here is the tag we are about to select {}'.format(p))

            sql = "SELECT * FROM players WHERE tag='{}';".format(p)
            res = db.exec(sql)
            if len(res) == 0:
                # This player has never player before. Assume they have no matches in any other scene
                matches_per_scene = {s:0 for s in scenes}
                if scene in scenes:
                    matches_per_scene[scene] = 1
                    matches_per_scene_str = json.dumps(matches_per_scene)
                    sql = "INSERT INTO players (tag, matches_per_scene, scene) VALUES ('{}', '{}', '{}');".format(p, matches_per_scene_str, scene)
                # Set this players scene in the web since they do not have one yet
                group_id = scenes.index(scene)
                update_group(p, group_id)
                db.exec(sql)
            else:
                # This player has already played in other scenes. Update the counts
                matches_per_scene = json.loads(res[0][2])

                # Which scene was this player a part of before?
                sort = [(k, matches_per_scene[k]) for k in sorted(matches_per_scene, key=matches_per_scene.get, reverse=True)]
                max_scene = sort[0][0]
                group_id_before = scenes.index(max_scene)

                if not scene in matches_per_scene:
                    matches_per_scene[scene] = 0
                matches_per_scene[scene] = matches_per_scene[scene] + 1

                # Which scene is this player a part of now?
                sort = [(k, matches_per_scene[k]) for k in sorted(matches_per_scene, key=matches_per_scene.get, reverse=True)]
                max_scene = sort[0][0]
                group_id_after = scenes.index(max_scene)

                # If this player just changed scenes, update the player web
                if not group_id_before == group_id_after:
                    update_group(p, group_id_after)

                    # Update this players scene in the DB
                    sql = "UPDATE players SET matches_per_scene='{}', scene='{}' WHERE tag='{}';".format(json.dumps(matches_per_scene), scene, p)
                    db.exec(sql)
                else:
                    # This players scene didn't change, keep it the same
                    sql = "UPDATE players SET matches_per_scene='{}' WHERE tag='{}';".format(json.dumps(matches_per_scene), p)
                    db.exec(sql)


        LOG.info('dallas: smashgg players {}'.format(players))
        # Create a map of ID to tag
        tag_id_dict = {}
        for player in players:
            id = int(player["entrant_id"])
            tag = player["tag"]
            # sanitize the tag
            tag = sanitize_tag(tag)
            
            #TODO coalesce here
            tag_id_dict[id] = tag

        sets = smash.tournament_show_sets(t, e)
        e = "pro" if "melee" in e else "pro_wiiu"
        for s in sets:
            # Temporary
            date = '2017-09-26'

            l_id = int(s['loser_id'])
            w_id = int(s['winner_id'])
            if l_id in tag_id_dict and w_id in tag_id_dict:
                loser = tag_id_dict[l_id]
                winner = tag_id_dict[w_id]
            else:
                continue

            sql = "INSERT INTO matches(player1, player2, winner, date, scene, url) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(\
                    winner, loser, winner, date, e, url)

            db.exec(sql)

            # Also update the player web with this match
            winner_loser_pairs.append((winner, loser))

    else:
        LOG.info("ERROR PARSING SMASHGG: {}".format(url))
        return

    # we need to pass a list of scenes to the player web
    scenes = bracket_utils.get_list_of_scene_names()
    update_web(winner_loser_pairs)

def analyze_tournament(db, url, scene, dated, urls_per_player=False):
    #Scrape the challonge website for the raw bracket
    bracket = bracket_utils.get_bracket(url)

    if bracket == None:
        return

    #Sanitize the braket
    sanitized = bracket_utils.sanitize_bracket(bracket)

    analyze_bracket(db, sanitized, url, scene, dated, urls_per_player)

def analyze_bracket(db, bracket, base_url, scene, dated, include_urls_per_player=False):
    winner_loser_pairs = []
    players = set()
    #continuously find the next instances of 'player1' and 'player2'
    if debug: print('analyz a bracket. Dated? ' + str(dated))
    while 'player1' in bracket and 'player2' in bracket:
        index = bracket.index("player1")
        bracket = bracket[index:]
        player1_id, player1_tag = get_player_info(bracket)

        index = bracket.index("player2")
        bracket = bracket[index:]
        player2_id, player2_tag = get_player_info(bracket)

        index = bracket.index("winner_id")
        bracket = bracket[index:]
        colon = bracket.index(":")
        comma = bracket.index(",")
        winner_id = bracket[colon+1:comma]

        #on the off chance that the bracket was not filled out all way, and a player is left blank, skip
        if winner_id == 'null' or player1_id == None or player2_id == None:
            break

        #Before we use this tag, we should see if it is one that we should coalesce
        # eg, if this is 'thanksgiving mike', we should change it to 'christmas mike'
        player1_tag = get_coalesced_tag(player1_tag)
        player2_tag = get_coalesced_tag(player2_tag)

        player1_tag = sanitize_tag(player1_tag)
        player2_tag = sanitize_tag(player2_tag)

        players.add(player1_tag)
        players.add(player2_tag)

        #Now that we have both players, and the winner ID, what's the tag of the winner?
        winner = player1_tag if int(winner_id) == int(player1_id) else player2_tag
        loser = player1_tag if winner == player2_tag else player2_tag

        date = get_date(base_url)
        sql = "INSERT INTO matches(player1, player2, winner, date, scene, url) VALUES ('"
        sql += str(player1_tag) + "', '" + str(player2_tag) + "', '" + str(winner) + "', '"+ str(date) + "', '"+str(scene) + "', '"+str(base_url)+"'); "

        db.exec(sql, debug=False)

        # Also insert this match into the player web
        winner_loser_pairs.append((winner, loser))
    # we need to pass a list of scenes to the player web
    scenes = bracket_utils.get_list_of_scene_names()
    update_web(winner_loser_pairs)

    # Check if these players are already in the players table
    scenes = bracket_utils.get_list_of_scene_names()
    for p in players:
        sql = "SELECT * FROM players WHERE tag='{}';".format(p)
        res = db.exec(sql)
        if len(res) == 0:
            # This player has never player before. Assume they have no matches in any other scene
            matches_per_scene = {s:0 for s in scenes}
            if scene in scenes:
                matches_per_scene[scene] = 1
                matches_per_scene_str = json.dumps(matches_per_scene)
                sql = "INSERT INTO players (tag, matches_per_scene, scene) VALUES ('{}', '{}', '{}');".format(p, matches_per_scene_str, scene)

            # Set this players scene in the web since they do not have one yet
            group_id = scenes.index(scene)
            update_group(p, group_id)
            db.exec(sql)
        else:
            LOG.info('dallas: have detected that {} has played before'.format(p))
            # This player has already played in other scenes. Update the counts
            matches_per_scene = json.loads(res[0][2])

            # Which scene was this player a part of before?
            sort = [(k, matches_per_scene[k]) for k in sorted(matches_per_scene, key=matches_per_scene.get, reverse=True)]
            max_scene = sort[0][0]
            group_id_before = scenes.index(max_scene)
            LOG.info('dallas: here is this players matches per scene {}, which is ndex {}'.format(matches_per_scene, group_id_before))

            if not scene in matches_per_scene:
                LOG.info('dallas: the scene {} is not in their list'.format(scene))
                matches_per_scene[scene] = 0
            matches_per_scene[scene] = matches_per_scene[scene] + 1

            # Which scene is this player a part of now?
            sort = [(k, matches_per_scene[k]) for k in sorted(matches_per_scene, key=matches_per_scene.get, reverse=True)]
            max_scene = sort[0][0]
            group_id_after = scenes.index(max_scene)
            LOG.info('dallas: this is their matches per scene and group id after{}, {}'.format(matches_per_scene, group_id_after))

            # If this player just changed scenes, update the player web
            if not group_id_before == group_id_after:
                LOG.info('about to update group for player {}'.format(p))
                update_group(p, group_id_after)
                LOG.info('dallas: Chaning the scene of player {} to {}'.format(p, scene))
                # Update this players scene in the DB
                sql = "UPDATE players SET matches_per_scene='{}', scene='{}' WHERE tag='{}';".format(json.dumps(matches_per_scene), scene, p)
                db.exec(sql)

            else:
                # TODO remove
                LOG.info('dallas: Updating players scene count: {} {}'.format(p, matches_per_scene))
                # This players scene didn't change, keep it the same
                sql = "UPDATE players SET matches_per_scene='{}' WHERE tag='{}';".format(json.dumps(matches_per_scene), p)
                db.exec(sql)




def get_player_info(bracket):
    player_dict = json.loads(bracket_utils.sanitize_bracket(bracket))
    ID = player_dict['id']
    tag = player_dict['display_name'].lower() if 'display_name' in player_dict else None
    if debug and 'hakii' in tag:
        print('tyring to get tag out of player info')
        pprint(player_dict)
    return ID, tag

def get_coalesced_tag(tag, debug=debug):
    # See if this is one of the tags we should coalesce
    for tags in TAGS_TO_COALESCE:
        # Tags is a list of all tags that are actually one player
        # eg. ['christmas mike', 'thanksgiving mike']
        if debug:
            print('trying to find tag {} in list: {}'.format(tag, tags))

        tag = tag.lower()
        if tag in tags:
            if debug:
                print('found ' + str(tags[0]) + ' in list ')
            # The first tag in this list is the main tag that we want
            # to change the others to
            # eg. ['christmas mike', 'thanksgiving mike']
            return tags[0]

    # If this is not a tag that we need to coalesce
    return tag

def get_date(url):
    url = url + "/log"
    bracket, status = bracket_utils.hit_url(url)

    # TODO figure out what to do if this string is not in
    s2 = '2015-03-07'
    if 'created_at' not in bracket:
        return s2

    first_occurance = str(bracket).index('created_at')
    bracket = bracket[first_occurance:]

    #TODO if one day this code randomly stop working, it's probably this
    s = 'created_at":"'
    i = len(s)
    i2 = len(s2) + i
    date = bracket[i:i2]
    y = date.split('-')[0]
    m = date.split('-')[1]
    d = date.split('-')[2]

    return date

def process(url, scene, db):
    # Just to be sure, make sure this bracket hasn't already been analyzed
    sql = "SELECT * FROM analyzed WHERE base_url = '" + str(url) + "';"
    result = db.exec(sql)
    if len(result) > 0:
        return

    # Also see if we made it partially through analyzing this bracket
    sql = "SELECT * FROM matches WHERE url = '{}';".format(url)
    result = db.exec(sql)
    if len(result) > 0:
        # Clear out these matches so we can start from the beginning
        sql = "DELETE FROM matches WHERE url = '{}';".format(url)
        db.exec(sql)

    if "challonge" in url:
        analyze_tournament(db, url, scene, True, False)
    else:
        analyze_smashgg_tournament(db, url, scene, True, False)

    sql = "INSERT INTO analyzed (base_url) VALUES ('" + str(url)+"');" 

    db.exec(sql)
