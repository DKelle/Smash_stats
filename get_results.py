from bs4 import BeautifulSoup
from requests import get
import subprocess
import json
from pprint import pprint

url = "http://smashco.challonge.com/CSUWW65WUS"

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

print(bracket)
