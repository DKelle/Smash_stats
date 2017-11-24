import bracket_utils
import copy
import json

from pprint import pprint
from constants import TAGS_TO_COALESCE

id_tag_dict = {}
sanitized_tag_dict = {}
wins_losses_dict = {} #of the form player_tag:[(tag,wins,losses), (player,wins,losses)]
urls_per_player = {} # Count the number of URLs each player was in

debug = False

def analyze_tournament(url, urls_per_player=False):
    #Scrape the challonge website for the raw bracket
    bracket = bracket_utils.get_bracket(url)

    if bracket == None:
        return

    #Sanitize the braket
    sanitized = bracket_utils.sanitize_bracket(bracket)

    analyze_bracket(sanitized, url, urls_per_player)

def analyze_bracket(bracket, base_url, include_urls_per_player=False):
    global id_tag_dict
    global sanitized_tag_dict
    global wins_losses_dict
    global urls_per_player
    #continuously find the next instances of 'player1' and 'player2'
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

        #Now that we have both players, and the winner ID, what's the tag of the winner?
        winner = player1_tag if int(winner_id) == int(player1_id) else player2_tag
        loser = player1_tag if winner == player2_tag else player2_tag

        #Add this bracket to the set of brackets
        # that 'winner' has played in
        if include_urls_per_player:
            if winner not in urls_per_player:
                urls_per_player[winner] = []
            if base_url not in urls_per_player[winner]:
                urls_per_player[winner].append(base_url)

        #sanitize both tage (by taking out whitespace)
        san_winner = "".join(winner.split())
        san_loser = "".join(loser.split())

        #add the id/tag to the global dict
        for ID,tag in [(player1_id,player1_tag), (player2_id,player2_tag)]:
            if ID not in id_tag_dict:
                id_tag_dict[ID] = tag
            sanitized = "".join(tag.split())
            if sanitized not in sanitized_tag_dict:
                sanitized_tag_dict[sanitized] = tag

        #Update the winner
        if san_winner not in wins_losses_dict:
            wins_losses_dict[san_winner] = {}

        if loser not in wins_losses_dict[san_winner]:
            wins_losses_dict[san_winner][loser] = (1,0)
        else:
            cur = wins_losses_dict[san_winner][loser]
            wins_losses_dict[san_winner][loser] = (cur[0]+1,cur[-1])

        #update the loser
        if san_loser not in wins_losses_dict:
            wins_losses_dict[san_loser] = {}

        if winner not in wins_losses_dict[san_loser]:
            wins_losses_dict[san_loser][winner] = (0,1)
        else:
            cur = wins_losses_dict[san_loser][winner]
            wins_losses_dict[san_loser][winner] = (cur[0],cur[-1]+1)

def get_player_info(bracket):
    player_dict = json.loads(bracket_utils.sanitize_bracket(bracket))
    ID = player_dict['id']
    tag = player_dict['display_name'].lower() if 'display_name' in player_dict else None
    if debug and 'hakii' in tag:
        print('tyring to get tag out of player info')
        pprint(player_dict)
    return ID, tag

def get_win_loss_data(base_urls = ['http://challonge.com/Smashbrews###'], include_urls_per_player=False):
    global wins_losses_dict
    global sanitized_tag_dict

    if debug: print('about to start getting valid ULRS')

    for base_url in base_urls:
        start, end = bracket_utils.get_valid_url_range(base_url)
        for i in range(start,  end+1):
            bracket = base_url.replace('###', str(i))
            analyze_tournament(bracket, include_urls_per_player)

    #The win loss dict is full of tags with whitespace removed. Change the tags back to the proper spacing
    temp_dict = {}
    for key in wins_losses_dict:
        tag = sanitized_tag_dict[key]
        temp_dict[tag] = wins_losses_dict[key]
    wins_losses_dict = temp_dict

    if include_urls_per_player:
        return wins_losses_dict, urls_per_player

    return wins_losses_dict

def temp():
    global wins_losses_dict
    global sanitized_tag_dict

    urls = bracket_utils.get_brackets_from_scene('https://austinsmash4.challonge.com')
    for url in urls:
        analyze_tournament(url)

    #The win loss dict is full of tags with whitespace removed. Change the tags back to the proper spacing
    temp_dict = {}
    for key in wins_losses_dict:
        tag = sanitized_tag_dict[key]
        temp_dict[tag] = wins_losses_dict[key]
    wins_losses_dict = temp_dict
    return wins_losses_dict

def coalesce_tags():
    global wins_losses_dict
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
        if main_tag in wins_losses_dict.keys():
            if debug:
                print('found the tag ' + str(main_tag) + ' to coalesce')
                print('coalescing with the tags ' + str(other))
            for o in other:
                base_data = wins_losses_dict[main_tag]

                # Is the name we want to coalesce with in the dict?
                if o in wins_losses_dict.keys():
                    coalesce_data = wins_losses_dict[o]

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

                    wins_losses_dict[main_tag] = new_data
                    del wins_losses_dict[o]

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

if __name__ == "__main__":
    #base_url = 'http://challonge.com/Smashbrews###'
    #start = bracket_utils.get_first_valid_url(base_url)
    #end = bracket_utils.get_last_valid_url(base_url, start) us Christif debug: print("Start is %s. End is %s", start, end)
    #for i in range(start,  end+1):
    #    bracket = base_url + str(i)
    #    analyze_tournament(bracket)
    #pprint(wins_losses_dict)
    temp()
