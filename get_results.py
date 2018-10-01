import bracket_utils
import copy
import json
import datetime
import re
import pysmash
import time

from logger import logger
from pprint import pprint
from constants import TAGS_TO_COALESCE
from player_web import update_web
import os

smash = None
id_tag_dict = {}
sanitized_tag_dict = {}
debug = False 

LOG = logger(__name__)
skip_count = 0

def sanitize_tag(tag):
    tag = ''.join([i if ord(i) < 128 else ' ' for i in tag])
    # Parse out sponsor
    tag = tag.split('|')[-1].lstrip().rstrip()
    return re.sub("[^a-z A-Z 0-9 ]",'',tag.lower()).rstrip().lstrip()

def analyze_smashgg_tournament(db, url, scene, dated, urls_per_player=False, display_name=None, testing=False):
    global smash
    global skip_count
    if smash == None:
        smash = pysmash.SmashGG()


    # For testing purposes, sometimes we don't want to update the web
    use_web = not testing

    match_pairs = []
    tag_to_gid = {}
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

        try:
            start_at_epoch = smash.tournament_show(t)['start_at']
            date = datetime.datetime.utcfromtimestamp(start_at_epoch).strftime("%Y-%m-%d")
        except Exception:
            LOG.exc('We couldnt find a date for tournament {}'.format(t))
            date = '2017-09-26'

        # The event will be either 'melee' or 'wiiu'

        players = smash.tournament_show_players(t, e)
        # Sleep between requests to prevent rate limiting
        time.sleep(.5)

        # Check if these players are already in the players table
        scenes = bracket_utils.get_list_of_scene_names()
        for player in players:
            p = sanitize_tag(player['tag'])
            create_player_if_not_exist(p, scene, db, testing)
            if not testing:
                # Calculate the group for these two players
                gid = calculate_and_update_group(p, scene, db) if not p in tag_to_gid else tag_to_gid[p]
                tag_to_gid[p] = gid

        # Create a map of ID to tag
        tag_id_dict = {}
        for player in players:
            id = int(player["entrant_id"])
            tag = player["tag"]
            # sanitize the tag
            tag = sanitize_tag(tag)
            
            tag = get_coalesced_tag(tag)
            tag_id_dict[id] = tag

        sets = smash.tournament_show_sets(t, e)
        # Sleep between requests to prevent rate limiting
        time.sleep(.5)

        placings = bracket_utils.get_tournament_placings(url)
        for s in sets:
            
            l_id = int(s['loser_id'])
            w_id = int(s['winner_id'])
            s1 = s['entrant_1_score']
            s2 = s['entrant_2_score']

            # If we don't have score info, default to 3-0
            entrant_1_score = 3 if s1 == None else int(s1)
            entrant_2_score = 0 if s2 == None else int(s2)
            score = json.dumps([max(entrant_1_score, entrant_2_score), min(entrant_1_score, entrant_2_score)])
            if l_id in tag_id_dict and w_id in tag_id_dict:
                loser = tag_id_dict[l_id]
                winner = tag_id_dict[w_id]

                if loser in placings and winner in placings:
                    winner_place = placings[winner]
                    loser_place = placings[loser]

                    # Only record this match if at least one of these players got top 64
                    # Probably no one cares about r1 pools matches between two scrubs
                    # Having less matches will also reduce time needed to rank players
                    if winner_place > 64 and loser_place > 64:
                        skip_count = skip_count + 1
                        if skip_count % 100 == 0:
                            LOG.info('Both these players suck, so not entering this match {} got {} and {} got {}. Have now skipped {} total'.format(winner, winner_place, loser, loser_place, skip_count))

                        continue
                else:
                    # We don't have the placing for this player. Skip
                    continue

            else:
                continue

            sql = "INSERT INTO matches(player1, player2, winner, date, scene, url, display_name, score) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(\
                    winner, loser, winner, date, scene, url, display_name, score)

            db.exec(sql)
            
            # Get the group that these 2 players belong to
            if not testing:
                g1 = tag_to_gid[winner]
                g2 = tag_to_gid[loser]


            if not testing:
                # Also update the player web with this match
                match_pairs.append((winner, g1, loser, g2))
    else:
        LOG.info("ERROR PARSING SMASHGG: {}".format(url))
        return

    if not testing:
        # we need to pass a list of scenes to the player web
        LOG.info('about to update match pairs for bracket {}'.format(url))
        update_web(match_pairs, db)
        LOG.info('finished updating match pairs for bracket {}'.format(url))

def analyze_tournament(db, url, scene, dated, urls_per_player=False, display_name=None):
    #Scrape the challonge website for the raw bracket
    bracket = bracket_utils.get_bracket(url)

    if bracket == None:
        return

    #Sanitize the braket
    sanitized = bracket_utils.sanitize_bracket(bracket)

    analyze_bracket(db, sanitized, url, scene, dated, urls_per_player, display_name)

def analyze_bracket(db, bracket, base_url, scene, dated, include_urls_per_player=False, display_name=None, testing=False):
    match_pairs = []
    tag_to_gid = {}
    players = set()
    #continuously find the next instances of 'player1' and 'player2'
    if debug: print('analyz a bracket. Dated? ' + str(dated))
    date = bracket_utils.get_date(base_url)
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

        index = bracket.index('scores')
        bracket = bracket[index:]
        colon = bracket.index(":")
        brace = bracket.index("]")
        scores = json.loads(bracket[colon+1:brace+1])
        if len(scores) == 0:
            # If no score was reported, assume 2-0
            scores = [2, 0]

        winner_score = max(scores)
        loser_score = min(scores)
        scores = json.dumps([winner_score, loser_score])
        
        #on the off chance that the bracket was not filled out all way, and a player is left blank, skip
        if winner_id == 'null' or player1_id == None or player2_id == None:
            break

        #Before we use this tag, we should see if it is one that we should coalesce
        # eg, if this is 'thanksgiving mike', we should change it to 'christmas mike'
        player1_tag = sanitize_tag(player1_tag)
        player2_tag = sanitize_tag(player2_tag)

        player1_tag = get_coalesced_tag(player1_tag)
        player2_tag = get_coalesced_tag(player2_tag)

        players.add(player1_tag)
        players.add(player2_tag)

        #Now that we have both players, and the winner ID, what's the tag of the winner?
        winner = player1_tag if int(winner_id) == int(player1_id) else player2_tag
        loser = player1_tag if winner == player2_tag else player2_tag

        sql = "INSERT INTO matches(player1, player2, winner, date, scene, url, display_name, score) VALUES ('"
        sql += str(player1_tag) + "', '" + str(player2_tag) + "', '" + str(winner) + "', '"+ str(date) + "', '"+str(scene) + "', '"+str(base_url)+"', '"+str(display_name)+"', '"+str(scores)+"'); "

        db.exec(sql, debug=False)

        # Calculate the group for these two players
        create_player_if_not_exist(winner, scene, db, testing)
        create_player_if_not_exist(loser, scene, db, testing)
        group_id1 = calculate_and_update_group(winner, scene, db) if not winner in tag_to_gid else tag_to_gid[winner]
        tag_to_gid[winner] = group_id1
        group_id2 = calculate_and_update_group(loser, scene, db) if not loser in tag_to_gid else tag_to_gid[loser]
        tag_to_gid[loser] = group_id2

        # Also insert this match into the player web
        match_pairs.append((winner, group_id1, loser, group_id2))

    update_web(match_pairs, db)

def create_player_if_not_exist(p, scene, db, testing=False):
    sql = "SELECT * FROM players WHERE tag='{}';".format(p)
    res = db.exec(sql)
    scenes = bracket_utils.get_list_of_scene_names() if not testing else [scene]
    if len(res) == 0:


        # This player has never player before. Assume they have no matches in any other scene
        matches_per_scene = {s:0 for s in scenes}
        if scene in scenes:
            matches_per_scene[scene] = 1
            matches_per_scene_str = json.dumps(matches_per_scene)
            sql = "INSERT INTO players (tag, matches_per_scene, scene) VALUES ('{}', '{}', '{}');".format(p, matches_per_scene_str, scene)
            db.exec(sql)

    return res

def calculate_and_update_group(p, scene, db):
    p = get_coalesced_tag(p)
    sql = "SELECT * FROM players WHERE tag='{}';".format(p)
    res = db.exec(sql)
    gid = 0
    scenes = bracket_utils.get_list_of_scene_names()
    if len(res) == 0:
        # Set this players scene in the web since they do not have one yet
        group_id = scenes.index(scene)
        gid = group_id
        db.exec(sql)
    else:
        # This player has already played in other scenes. Update the counts
        matches_per_scene = json.loads(res[0][2])

        # Which scene was this player a part of before?
        sort = [(k, matches_per_scene[k]) for k in sorted(matches_per_scene, key=matches_per_scene.get, reverse=True)]
        max_scene = sort[0][0]
        group_id_before = scenes.index(max_scene)

        if not scene in matches_per_scene:
            LOG.info('the scene {} is not in their list'.format(scene))
            matches_per_scene[scene] = 0
        matches_per_scene[scene] = matches_per_scene[scene] + 1

        # Which scene is this player a part of now?
        sort = [(k, matches_per_scene[k]) for k in sorted(matches_per_scene, key=matches_per_scene.get, reverse=True)]
        max_scene = sort[0][0]
        group_id_after = scenes.index(max_scene)
        gid = group_id_after

        # If this player just changed scenes, update the player web
        if not group_id_before == group_id_after:
            LOG.info('Chaning the scene of player {} to {}'.format(p, scene))
            LOG.info('this is their matches per scene and group id after{}, {}'.format(matches_per_scene, group_id_after))
            # Update this players scene in the DB
            sql = "UPDATE players SET matches_per_scene='{}', scene='{}' WHERE tag='{}';".format(json.dumps(matches_per_scene), scene, p)
            db.exec(sql)

        else:
            # This players scene didn't change, keep it the same
            sql = "UPDATE players SET matches_per_scene='{}' WHERE tag='{}';".format(json.dumps(matches_per_scene), p)
            db.exec(sql)

    return gid


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

def process(url, scene, db, display_name):
    success = True

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
        analyze_tournament(db, url, scene, True, False, display_name)
    else:
        try:
            analyze_smashgg_tournament(db, url, scene, True, False, display_name)
        except Exception as e:
            success = False

            LOG.exc('Hit exception while trying to analyze url {}'.format(url))
            LOG.info('here is exception \n{}'.format(e))

        LOG.info('about to insert gg {}'.format(url))

    sql = "INSERT INTO analyzed (base_url) VALUES ('" + str(url)+"');"
    db.exec(sql)
    return success
