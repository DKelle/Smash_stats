from bs4 import BeautifulSoup
from requests import get
from ast import literal_eval
import json

def get_bracket():
    url = "http://smashco.challonge.com/CSUWW65WUS"
    username = open('username').read()
    key = open('api_key').read()

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
    #continuously find the next instances of 'player1' and 'player2'

    index = bracket.index("player1")
    bracket = bracket[index:]
    player1 = get_player_info(bracket)

def get_player_info(bracket):
    player_dict = json.loads(sanitize_bracket(bracket))
    print(player_dict['display_name'])
    return player_dict

if __name__ == "__main__":
    #Scrape the challonge website for the raw bracket
    bracket = get_bracket()

    #Sanitize the braket
    sanitized = sanitize_bracket(bracket)

    analyze_bracket(sanitized)

