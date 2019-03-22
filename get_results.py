import bracket_utils
import copy
import json
import datetime
import re
import pysmash
import time
import challonge

from logger import logger
from pprint import pprint
from constants import TAGS_TO_COALESCE
from player_web import update_web
from urllib.error import HTTPError
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
    return re.sub("[^a-z A-Z 0-9 : /]",'',tag.lower()).rstrip().lstrip()

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

            sql = "INSERT INTO matches(player1, player2, winner, date, scene, url, display_name, score) VALUES ('{winner}', '{loser}', '{winner}', '{date}', '{scene}', '{url}', '{display_name}', '{score}');"
            args = {'winner': winner, 'loser': loser, 'winner': winner, 'date': date, 'scene': scene, 'url': url, 'display_name': display_name, 'score': score}

            db.exec(sql, args)
            
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

def analyze_tournament(db, url, scene, dated, urls_per_player=False, display_name=None, testing=False):
    match_pairs = []
    tag_to_gid = {}
    # We need to translate the name of the bracket into something the challonge api will understand.
    # eg https://challonge.com/atx122 -> atx122
    api_name = bracket_utils.translate_url_to_api_name(url)
    user = open('secrets/user.secret').readline().rstrip()
    api_key = open('secrets/api_key.secret').readline().rstrip()
    challonge.set_credentials(user, api_key)

    # Now that we are logged into the api, get all of the players
    tournament = None
    try:
        tournament = challonge.tournaments.show(api_name)
    except HTTPError as e:
        # It's possible that we got the wrong api name for this tournament
        if e.getcode() == 404:
            # Parse out the username. eg smascho-FCWUA1 -> FCWUA1
            try:
                tournament = challonge.tournaments.show(api_name.split('-')[-1])
            except HTTPError as e:
                print(e)
                LOG.exc('Couldnt find challonge info for tournament {}'.format(url))
                return False

    try:
        if not tournament.get('started-at'):
            LOG.info('URL {} has not been started. Will try again in an hour.'.format(url))
            return False
        date = str(tournament.get('started-at').strftime('%Y-%m-%d'))
        players = challonge.participants.index(tournament['id'])
        matches = challonge.matches.index(tournament["id"])
        tag_player_id_map = {}

        for player in players:
            # In case the name is missing from the field we expect it to be in, have some fall backs. These should all have the same value
            tag = player.get('display_name') or player.get('name') or player.get('challonge-username') or player.get('username')

            if not tag:
                LOG.exc('UNEXPECTED ERROR: Tag is none for player. Skipping this player. This may cause issues with analyzing the rest of this bracket'.format(player))
                continue
            # Make sure to sanitize and coalesce this tag
            tag = get_coalesced_tag(sanitize_tag(tag))
            LOG.info('about to add player {} for scene {} in url {}'.format(tag, scene, url))
            create_player_if_not_exist(tag, scene, db, testing)
            id = player.get('id')
            tag_player_id_map[id] = tag



        for match in matches:
            # If this score was never reported, then there will not be a winner-id or loser-id. Just skip this match
            if match.get('winner-id') == None or match.get('loser-id') == None:
                continue

            # I'm not sure why this could happen. May be a bug in the challonge API.
            # Sometimes the ID of the winner is not registered to a player in the tournament
            if match.get('winner-id') not in tag_player_id_map or match.get('loser-id') not in tag_player_id_map:
                continue

            winner = tag_player_id_map[match.get('winner-id')]
            loser = tag_player_id_map[match.get('loser-id')]
            scores = (match.get('scores-csv', '2-0') or '2-0').split('-')

            try:
                # Convert the score to ints, or assume the score was 2-0
                scores = [int(score) for score in scores]
                scores =  sorted(scores, reverse=True)
            except:
                scores = [2, 0]

            sql = "INSERT INTO matches(player1, player2, winner, date, scene, url, display_name, score) VALUES ('{player1}', '{player2}', '{winner}', '{date}', '{scene}', '{base_url}', '{display_name}', '{scores}');"
            args = {'player1': winner, 'player2': loser, 'winner': winner, 'date': date, 'scene': scene, 'base_url': url, 'display_name': display_name, 'scores': scores}
            db.exec(sql, args, debug=True)

    	    # We don't want to update the web if we are testing
            if not testing:
                group_id1 = calculate_and_update_group(winner, scene, db) if not winner in tag_to_gid else tag_to_gid[winner]
                tag_to_gid[winner] = group_id1
                group_id2 = calculate_and_update_group(loser, scene, db) if not loser in tag_to_gid else tag_to_gid[loser]
                tag_to_gid[loser] = group_id2

                # Also insert this match into the player web
                match_pairs.append((winner, group_id1, loser, group_id2))

        if not testing:
            update_web(match_pairs, db)

    except Exception as e:
        print(e)
        LOG.exc("Hit exception while analyzing matches in bracket {}".format(url))
        return False

    return True

def create_player_if_not_exist(p, scene, db, testing=False):
    sql = "SELECT * FROM players WHERE tag='{tag}';"
    args = {'tag': p}
    res = db.exec(sql, args)
    scenes = bracket_utils.get_list_of_scene_names() if not testing else [scene]
    if len(res) == 0:


        # This player has never player before. Assume they have no matches in any other scene
        matches_per_scene = {s:0 for s in scenes}
        if scene in scenes:
            matches_per_scene[scene] = 1
            matches_per_scene_str = json.dumps(matches_per_scene)
            sql = "INSERT INTO players (tag, matches_per_scene, scene) VALUES ('{tag}', '{matches_per_scene_str}', '{scene}');"
            args = {'tag': p, 'matches_per_scene_str': matches_per_scene_str, 'scene': scene}
            db.exec(sql, args)

    return res

def calculate_and_update_group(p, scene, db):
    p = get_coalesced_tag(p)
    sql = "SELECT * FROM players WHERE tag='{tag}';"
    args = {'tag': p}
    res = db.exec(sql, args)
    gid = 0
    scenes = bracket_utils.get_list_of_scene_names()
    if len(res) == 0:
        # Set this players scene in the web since they do not have one yet
        gid = scenes.index(scene)
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
            sql = "UPDATE players SET matches_per_scene='{matches}', scene='{scene}' WHERE tag='{tag}';"
            args = {'matches': json.dumps(matches_per_scene), 'scene': scene, 'tag': p}
            db.exec(sql, args)

        else:
            # This players scene didn't change, keep it the same
            sql = "UPDATE players SET matches_per_scene='{matches}' WHERE tag='{tag}';"
            args = {'matches': json.dumps(matches_per_scene), 'tag': p}
            db.exec(sql, args)

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
    sql = "SELECT * FROM analyzed WHERE base_url = '{url}';"
    args = {'url': url}
    result = db.exec(sql, args)
    if len(result) > 0:
        return

    # Also see if we made it partially through analyzing this bracket
    sql = "SELECT * FROM matches WHERE url = '{url}';"
    result = db.exec(sql, args)
    if len(result) > 0:
        # Clear out these matches so we can start from the beginning
        sql = "DELETE FROM matches WHERE url = '{url}';"
        db.exec(sql, args)

    success = False
    if "challonge" in url:
        success = analyze_tournament(db, url, scene, True, False, display_name)
    else:
        try:
            sucess = analyze_smashgg_tournament(db, url, scene, True, False, display_name)
        except Exception as e:
            success = False

            LOG.exc('Hit exception while trying to analyze url {}'.format(url))
            LOG.info('here is exception \n{}'.format(e))

        LOG.info('about to insert gg {}'.format(url))

    if success:
        sql = "INSERT INTO analyzed (base_url) VALUES ('{url}');"
        db.exec(sql, args)
    return success
