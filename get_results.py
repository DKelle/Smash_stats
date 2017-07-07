from bs4 import BeautifulSoup
from requests import get
from urllib.request import urlopen

username = open('username').read()
key = open('api_key').read()
url = "https://api.challonge.com/v1/tournaments/smashco-CSUWW65WUS/matches.json?username=Christmas_mike&api_key="+str(key)


data = urlopen(url)
print(data.read())
