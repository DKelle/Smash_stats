from bs4 import BeautifulSoup
from requests import get
from ast import literal_eval
import json
from pprint import pprint

id_tag_dict = {}
wins_losses_dict = {} #of the form player_tag:[(tag,wins,losses), (player,wins,losses)]

def analyze_tournament(week):
    url = "http://smashco.challonge.com/CSUWW" + str(week) + "WUS"
    #Scrape the challonge website for the raw bracket
    bracket = get_bracket(url)

    #Sanitize the braket
    sanitized = sanitize_bracket(bracket)

    analyze_bracket(sanitized)

def get_bracket(url):

    # get the html page
    r = get(url)
    data = r.text

    # Create the Python Object from HTML
    soup = BeautifulSoup(data, "html.parser")

    # the bracket is inside a 'script' tag
    script = soup.find_all('script')
    bracket = None
    for s in script:
        if 'TournamentStore' in str(s):
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
    global wins_losses_dict
    #continuously find the next instances of 'player1' and 'player2'
    while 'player1' in bracket:
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

        #Now that we have both players, and the winner ID, what's the tag of the winner?
        winner = player1_tag if int(winner_id) == int(player1_id) else player2_tag
        loser = player1_tag if winner == player2_tag else player2_tag

        #add the id/tag to the global dict
        for ID,tag in [(player1_id,player1_tag), (player2_id,player2_tag)]:
            if ID not in id_tag_dict:
                id_tag_dict[ID] = tag

        #Update the winner
        if winner not in wins_losses_dict:
            wins_losses_dict[winner] = {}

        if loser not in wins_losses_dict[winner]:
            wins_losses_dict[winner][loser] = (1,0)
        else:
            cur = wins_losses_dict[winner][loser]
            wins_losses_dict[winner][loser] = (cur[0]+1,cur[-1])

        #update the loser
        if loser not in wins_losses_dict:
            wins_losses_dict[loser] = {}

        if winner not in wins_losses_dict[loser]:
            wins_losses_dict[loser][winner] = (0,1)
        else:
            cur = wins_losses_dict[loser][winner]
            wins_losses_dict[loser][winner] = (cur[0],cur[-1]+1)



def get_player_info(bracket):
    player_dict = json.loads(sanitize_bracket(bracket))
    ID = player_dict['id']
    tag = player_dict['display_name']
    return ID, tag

if __name__ == "__main__":
    for i in range(64,68):
        analyze_tournament(i)
    pprint(wins_losses_dict)
