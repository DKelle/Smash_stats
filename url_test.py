from bs4 import BeautifulSoup
from requests import get
from ast import literal_eval
import json
from pprint import pprint
from get_brackets import get_urls

def get_first_valid_url(base_url):

    #Start from 1, and increment the number at the end or URL until we find a valid URL
    valid = False
    index = 1
    while(not valid):
        url = base_url.replace('###', str(index))

        # get the html page
        r = get(url)
        data = r.text

        if is_valid(data):
            valid = True
        else:
            index = index + 1

    return index

def get_last_valid_url(base_url, start = 1):

    #We know that URL number 'start' is valid. What is the next invalid URL?
    invalid_count = 0
    end = start #Use this to keep track of the last valid URL

    #Sometimes a week is skipped -- Make sure we see 5 invalid URLs in a row before calling it quits
    while(invalid_count <= 5):
        url = base_url.replace('###', str(start))

        # get the html page
        r = get(url)
        data = r.text

        if is_valid(data):
            invalid_count = 0
            end = start
        else:
            invalid_count = invalid_count + 1

        start = start + 1
    return end


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

    base_urls = ['http://smashco.challonge.com/CSUWW###WUS', 'http://smashco.challonge.com/CSUWW###WUD', 'http://smascho.challonge.com/FCWUA###', 'http://smascho.challonge.com/FCWUIB###', 'http://smashco.challonge.com/FCWUDC###']

    for base_url in base_urls:
        start = get_first_valid_url(base_url)
        end = get_last_valid_url(base_url, start)
        print('The initial start for base URL ' + str(base_url) + ' is ' + str(start))
        print('The final end for base URL ' + str(base_url) + 'is ' + str(end))
