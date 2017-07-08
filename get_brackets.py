from bs4 import BeautifulSoup
from requests import get
from ast import literal_eval
import json
from pprint import pprint

id_tag_dict = {}
wins_losses_dict = {} #of the form player_tag:[(tag,wins,losses), (player,wins,losses)]

def get_html(pages):
    #Scrape the challonge website for the raw brackets
    url = "http://smashco.challonge.com/?page="+str(pages)

    # get the html page
    r = get(url)
    data = r.text

    print(data)

    # Create the Python Object from HTML
    soup = BeautifulSoup(data, "html.parser")

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

if __name__ == "__main__":
    get_html(1)
