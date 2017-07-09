from bs4 import BeautifulSoup
from requests import get
from ast import literal_eval
import json
from pprint import pprint

id_tag_dict = {}
wins_losses_dict = {} #of the form player_tag:[(tag,wins,losses), (player,wins,losses)]

def get_html(pages):
    data = ''
    for page in range(1, pages+1):

        #Scrape the challonge website for the raw brackets
        url = "http://smashco.challonge.com/?page="+str(page)

        # get the html page
        r = get(url)
        html = r.text

        #return the HTML
        #collect the HTML
        data = data + '\n' + html
    return data

def scrape_urls(html):

    # Create the Python Object from HTML
    soup = BeautifulSoup(html, "html.parser")
    urls = []

    #fina all the <a> tags, because that's where we will find bracket URLs
    a_tags = soup.find_all('a')

    for a in soup.findAll('a'):
        url = a['href']

        #Check to see if this URL is to a Wii U bracket
        if 'http://' in url or 'https://' in url:
            if 'WU' in url:
                urls.append(url)

    return urls

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

def get_urls(pages = 5):
    #first get the raw HTML
    html = get_html(pages)

    #Scrape the HTML for bracket URLs
    urls = scrape_urls(html)

    return urls

if __name__ == "__main__":
    #first get the raw HTML
    html = get_html(5)

    #Scrape the HTML for bracket URLs
    urls = scrape_urls(html)

    for url in urls:
        print(url)
