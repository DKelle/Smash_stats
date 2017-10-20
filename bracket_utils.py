from time import sleep
from bs4 import BeautifulSoup
from requests import get
import re
import os
import pickle

DEFAULT_BASE_URLS = ['https://challonge.com/NP9ATX###', 'http://challonge.com/heatwave###', 'https://austinsmash4.challonge.com/atx###']

debug = True
def _get_first_valid_url(base_url):

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

def _get_last_valid_url(base_url, start=1):

    #We know that URL number 'start' is valid. What is the next invalid URL?
    invalid_count = 0
    end = start #Use this to keep track of the last valid URL

    #Sometimes a week is skipped -- Make sure we see 100 invalid URLs in a row before calling it quits
    while(invalid_count <= 50):
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

def get_valid_url_range(base_url):
    cwd = os.getcwd()
    fname = base_url.split('/')[-1]
    f = cwd+'/pickle/'+str(fname)+'.p'
    # Attempt to get this data from pickle

    try:
        with open(f, 'rb') as p:
            start, end = pickle.load(p)
            if debug: print('start and end FROM PICKLE', start, end)

            # Check for new brackets since the last time we pickled this data
            end = _get_last_valid_url(base_url, end)
    except FileNotFoundError:
        print('in erro')
        start = _get_first_valid_url(base_url)
        end = _get_last_valid_url(base_url, start)

    # If there has been more tournaments, pickle the new data back up
    with open( f, "wb") as p:
        pickle.dump((start, end), p)

    return start, end

def hit_url(url):
    #sleep, to make sure we don't go over our rate-limit
    sleep(.1)

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

    if debug: print('got bracket: \n', bracket)

    return bracket

def get_sanitized_bracket(url, symbol="{}"):
    bracket = get_bracket(url)
    sanitized = sanitize_bracket(bracket, symbol) if bracket else None
    return sanitized

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

def get_tournament_placings(bracket_url):
    # Map tags to their respective placings in this bracket
    placings_map = {}
    standings_html = hit_url(bracket_url+'/standings')
    soup = BeautifulSoup(standings_html, "html.parser")
    tds = soup.find_all('td')

    # Cycle thorugh these tds, and find the ones that represent different placings
    current_placing = 1
    for td in tds:
        if td.has_attr('class') and td['class'][0] == 'rank':
            current_placing = int(td.getText())
        span = td.find('span')
        # Player tags are kept in <span> elements
        if span:
            player = span.getText()
            placings_map[player.lower()] = current_placing

    return placings_map

def player_in_bracket(player, bracket):
    if re.search(player, bracket, re.IGNORECASE):
        return True
    return False

def get_urls_with_player(player="Christmas Mike", base_urls=DEFAULT_BASE_URLS):
    urls = []
    for base in base_urls:
        start, end = get_valid_url_range(base)
        for i in range(start, end+1):
            bracket_url = base.replace('###', str(i))
            bracket = get_sanitized_bracket(bracket_url)
            if bracket and player_in_bracket(player, bracket):
                urls.append(bracket_url)
    return urls

start, end = get_valid_url_range('https://challonge.com/NP9ATX###')
