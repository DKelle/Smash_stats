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

def sanitize_bracket(bracket):
    index = bracket.index("{")

    #Cut off everything up until the first open bracket
    bracket = bracket[index:]

    print(bracket)
    #use a queue to cut off everything after the aligning close bracket
    count = 0
    for i, letter in enumerate(bracket):
        if letter == "{":
            count = count + 1
        if letter == "}":
            count = count - 1

            #Also check to see if this is the final closing bracket
            if count == 0:
                index = i
                break

    bracket = bracket[:index+1]
    return bracket

def analyze_bracket(bracket):
    dump = json.dumps(bracket)
    print(dump)

    bracket_dict = json.loads(dump)

    for r in bracket_dict:
        analyze_round(r, bracket_dict)

def analyze_round(r, bracket):
    pass

if __name__ == "__main__":
    #Scrape the challonge website for the raw bracket
    bracket = get_bracket()

    #Sanitize the braket
    sanitized = sanitize_bracket(bracket)

    analyze_bracket(sanitized)

