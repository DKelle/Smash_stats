from bs4 import BeautifulSoup
from requests import get
from ast import literal_eval
import json
from pprint import pprint
from get_brackets import get_urls
from time import sleep

id_tag_dict = {}
sanitized_tag_dict = {}
wins_losses_dict = {} #of the form player_tag:[(tag,wins,losses), (player,wins,losses)]

debug = False

def analyze_tournament(url):
    #Scrape the challonge website for the raw bracket
    bracket = get_bracket(url)

    if bracket == None:
        return

    #Sanitize the braket
    sanitized = sanitize_bracket(bracket)

    analyze_bracket(sanitized)

def get_bracket(url):

    data = hit_url(url)

    # Create the Python Object from HTML
    soup = BeautifulSoup(data, "html.parser")

    # the bracket is inside a 'script' tag
    script = soup.find_all('script')
    bracket = None
    for s in script:
        if 'matches_by_round' in str(s):
            #We found the actual bracket. S contains all data about matches
            index = str(s).index('matches_by_round')
            s = str(s)[index:]
            bracket = (s)

    return bracket

def sanitize_bracket(bracket, symbol="{}"):
    #Which symbol should we be trying to match on? It will be either () or {}
    opn = symbol[0]
    close = symbol[-1]

    index = bracket.index(opn)

    #Cut off everything up until the first open bracket
    bracket = bracket[index:]

    #use a queue to cut off everything after the aligning close bracket
    count = 0
    for i, letter in enumerate(bracket):
        if letter == opn:
            count = count + 1
        if letter == close:
            count = count - 1

            #Also check to see if this is the final closing bracket
            if count == 0:
                index = i
                break

    bracket = bracket[:index+1]
    return bracket

def analyze_bracket(bracket):
    global id_tag_dict
    global sanitized_tag_dict
    global wins_losses_dict
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

        #Now that we have both players, and the winner ID, what's the tag of the winner?
        winner = player1_tag if int(winner_id) == int(player1_id) else player2_tag
        loser = player1_tag if winner == player2_tag else player2_tag
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
    player_dict = json.loads(sanitize_bracket(bracket))
    ID = player_dict['id']
    tag = player_dict['display_name'].lower() if 'display_name' in player_dict else None
    return ID, tag

def get_win_loss_data(base_urls = ['http://challonge.com/Smashbrews###']):
    global wins_losses_dict
    global sanitized_tag_dict

    if debug: print('about to start getting valid ULRS')

    for base_url in base_urls:
        start = get_first_valid_url(base_url)
        end = get_last_valid_url(base_url, start)
        for i in range(start,  end+1):
            bracket = base_url.replace('###', str(i))
            analyze_tournament(bracket)

    #The win loss dict is full of tags with whitespace removed. Change the tags back to the proper spacing
    temp_dict = {}
    for key in wins_losses_dict:
        tag = sanitized_tag_dict[key]
        temp_dict[tag] = wins_losses_dict[key]
    wins_losses_dict = temp_dict
    return wins_losses_dict

def get_first_valid_url(base_url):

    #Start from 1, and increment the number at the end or URL until we find a valid URL
    valid = False
    index = 1
    while(not valid):
        url = base_url.replace('###', str(index))
        data = hit_url(url)

        if is_valid(data):
            if debug: print('url ' + url + ' is valid')
            valid = True
        else:
            if debug: print('url ' + url + ' is not valid')
            index = index + 1

    return index

def get_last_valid_url(base_url, start = 1):

    #We know that URL number 'start' is valid. What is the next invalid URL?
    invalid_count = 0
    end = start #Use this to keep track of the last valid URL

    #Sometimes a week is skipped -- Make sure we see 100 invalid URLs in a row before calling it quits
    while(invalid_count <= 100):
        url = base_url.replace('###', str(start))
        if debug: print('start is ' + str(start))

        data = hit_url(url)

        if is_valid(data):
            if debug: print('url ' + str(url) + ' is valid')
            invalid_count = 0
            end = start
        else:
            invalid_count = invalid_count + 1

        start = start + 1
    return end

def hit_url(url):
    #sleep, to make sure we don't go over our rate-limit
    #sleep(.1)

    #Get the html page
    r = get(url)
    data = r.text

    return data

def is_valid(html):
    # Create the Python Object from HTML
    soup = BeautifulSoup(html, "html.parser")

    #A potential 404 will be seen in the 'title' tag
    titles = soup.find_all('title')

    #Check to see if this tournament page exists
    error = '404'
    for title in titles:
        if error in str(title):
            return False
    return True

if __name__ == "__main__":
    base_url = 'http://challonge.com/Smashbrews###'
    start = get_first_valid_url(base_url)
    end = get_last_valid_url(base_url, start)
    for i in range(start,  end+1):
        bracket = base_url + str(i)
        analyze_tournament(bracket)
    pprint(wins_losses_dict)
