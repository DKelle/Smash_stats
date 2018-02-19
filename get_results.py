import bracket_utils
import copy
import json
import datetime
import re
import pysmash

from pprint import pprint
from constants import TAGS_TO_COALESCE

smash = None
id_tag_dict = {}
sanitized_tag_dict = {}
debug = False 

def analyze_smashgg_tournament(db, url, scene, dated, urls_per_player=False):
    global smash
    if smash == None:
        smash = pysmash.SmashGG()

    # Exctract the tournament and event names
    # eg url:
    # https://smash.gg/tournament/pulsar-premier-league/events/rocket-league-3v3/brackets/68179
    # tournament name = pulsar-premier-leauge
    # event name = rocket-league-3v3
    url_parts = url.split('/')
    print("about to analyze smashgg bracket: {}".format(url))

    if 'tournament' in url_parts and 'events' in url_parts:
        t = url_parts[url_parts.index('tournament')+1]
        e = url_parts[url_parts.index('events')+1]

        # The event will be either 'melee' or 'wiiu'

        players = smash.tournament_show_players(t, e)
        print('dallas: smashgg players {}'.format(players))
        # Create a map of ID to tag
        tag_id_dict = {}
        for player in players:
            id = int(player["entrant_id"])
            tag = player["tag"]
            # sanitize the tag
            tag = ''.join([i if ord(i) < 128 else ' ' for i in tag])
            #TODO sql injection
            tag = re.sub("['-]", '', tag)
            
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

    else:
        print("ERROR PARSING SMASHGG: {}".format(url))
        return


def analyze_tournament(db, url, scene, dated, urls_per_player=False):
    #Scrape the challonge website for the raw bracket
    bracket = bracket_utils.get_bracket(url)

    if bracket == None:
        return

    #Sanitize the braket
    sanitized = bracket_utils.sanitize_bracket(bracket)

    analyze_bracket(db, sanitized, url, scene, dated, urls_per_player)

def analyze_bracket(db, bracket, base_url, scene, dated, include_urls_per_player=False):
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

        # TODO sql injection
        player1_tag = re.sub("['-]", '', player1_tag)
        player2_tag = re.sub("['-]", '', player2_tag)

        #Now that we have both players, and the winner ID, what's the tag of the winner?
        winner = player1_tag if int(winner_id) == int(player1_id) else player2_tag
        loser = player1_tag if winner == player2_tag else player2_tag

        date = get_date(base_url)
        sql = "INSERT INTO matches(player1, player2, winner, date, scene, url) VALUES ('"
        sql += str(player1_tag) + "', '" + str(player2_tag) + "', '" + str(winner) + "', '"+ str(date) + "', '"+str(scene) + "', '"+str(base_url)+"'); "

        db.exec(sql, debug=False)

def get_player_info(bracket):
    player_dict = json.loads(bracket_utils.sanitize_bracket(bracket))
    ID = player_dict['id']
    tag = player_dict['display_name'].lower() if 'display_name' in player_dict else None
    if debug and 'hakii' in tag:
        print('tyring to get tag out of player info')
        pprint(player_dict)
    return ID, tag

def coalesce_tags(dated=True):
    global wins_losses_dict
    global dated_win_loss
    data = wins_losses_dict if not dated else dated_win_loss
    # 2D list
    # Each inner list is a list of tags that should all be
    # coalesced into one
    tags_to_coalesce = TAGS_TO_COALESCE

    for tags in tags_to_coalesce:
        # The first tag in the list is the tag we want to
        # combine evertyhing to
        main_tag = tags[0]
        other = tags[1:]
        # coalesce 'christmas mike' and 'thanksgiving mike'
        if main_tag in data.keys():
            if debug:
                print('found the tag ' + str(main_tag) + ' to coalesce')
                print('coalescing with the tags ' + str(other))
            for o in other:
                base_data = data[main_tag]

                # Is the name we want to coalesce with in the dict?
                if o in data.keys():
                    coalesce_data = data[o]

                    new_data = copy.deepcopy(base_data)
                    for key, value in coalesce_data.items():
                        # Do we already have data about this tag?
                        if key in new_data.keys():
                            combine = lambda l1, l2, i: (l1[i] + l2[i])
                            combined_wins = combine(new_data[key], coalesce_data[key], 0)
                            combined_losses = combine(new_data[key], coalesce_data[key], 1)
                            combined_data = (combined_wins, combined_losses)
                            new_data[key] = combined_data
                        else:
                            new_data[key] = coalesce_data[key]

                    data[main_tag] = new_data
                    del data[o]

        elif debug:
            print(str(main_tag) + ' is not of one the tags in the win loss data')
            print('Not coalescing any of the following names:\n' + str(other))

def get_coalesced_tag(tag):
    # See if this is one of the tags we should coalesce
    for tags in TAGS_TO_COALESCE:
        # Tags is a list of all tags that are actually one player
        # eg. ['christmas mike', 'thanksgiving mike']
        if debug:
            print('trying to find tag in list: ' + str(tags))

        if tag in tags:
            if debug:
                print('found ' + str(tag) + ' in list ')
            # The first tag in this list is the main tag that we want
            # to change the others to
            # eg. ['christmas mike', 'thanksgiving mike']
            return tags[0]

    # If this is not a tag that we need to coalesce
    return tag

def get_date(url):
    url = url + "/log"
    bracket, status = bracket_utils.hit_url(url)

    first_occurance = str(bracket).index('created_at')
    bracket = bracket[first_occurance:]

    #TODO if one day this code randomly stop working, it's probably this
    s = 'created_at":"'
    s2 = '2015-03-07'
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

    if "challonge" in url:
        analyze_tournament(db, url, scene, True, False)
    else:
        analyze_smashgg_tournament(db, url, scene, True, False)

    sql = "INSERT INTO analyzed (base_url) VALUES ('" + str(url)+"');" 
    db.exec(sql)
