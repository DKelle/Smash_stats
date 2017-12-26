from flask import Blueprint, request
from get_ranks import get_ranks
import json
from database_writer import DatabaseWriter
import constants
import bracket_utils
#sys.path.insert(0, '/home/ubuntu/Smash_stats/tools')
#from tools import  

db = None

endpoints = Blueprint('endpoints', __name__)

@endpoints.route("/")
def temp():
    return "temp"

@endpoints.route("/wins")
def wins():
    if db == None:
        init()

    player = request.args.get('player', default="Christmas mike")
    sql = "SELECT * FROM matches WHERE winner = '"+str(player)+"' ORDER BY date DESC;"
    result = db.exec(sql)

    return json.dumps(str(result))

@endpoints.route("/losses")
def losses():
    if db == None:
        init()

    player = request.args.get('player', default="Christmas mike")
    sql = "SELECT * FROM matches WHERE (player1 = '"+str(player)+"' OR "\
            +"player2 = '"+str(player)+"') AND winner != '"+str(player)+"' ORDER BY date DESC;"
    result = db.exec(sql)

    return json.dumps(str(result))

@endpoints.route("/h2h")
def h2h():
    if db == None:
        init()

    player1 = request.args.get('player1', default="Christmas mike")
    player2 = request.args.get('player2', default="Christmas mike")
    sql = "SELECT * FROM matches WHERE (player1 = '"+str(player1)+"' OR "\
            +"player2 = '"+str(player1)+"') AND (player1 = '"+str(player2)+"' OR "\
            +"player2 = '"+str(player2)+"') ORDER BY date DESC;"
    result = db.exec(sql)

    return json.dumps(str(result))

@endpoints.route("/ranks")
def ranks():
    # Define contsants
    PLAYER1 = 0
    PLAYER2 = 1
    WINNER = 2
    DATE = 3
    SCENE = 4
    if db == None:
        init()

    # Default to Austin
    scene = request.args.get('scene', default='austin')

    # Get every match from this scene
    sql = "SELECT * FROM matches WHERE scene = '"+ scene +"';"
    matches =  db.exec(sql)

    # Iterate through each match, and build up our dict
    win_loss_dict = {}
    for match in matches:
        p1 = match[PLAYER1]
        p2 = match[PLAYER2]
        winner = match[WINNER]
        date = match[DATE]

        #Add p1 to the dict
        if p1 not in win_loss_dict:
            win_loss_dict[p1] = {}

        if p2 not in win_loss_dict[p1]:
            win_loss_dict[p1][p2] = []

        # Add an entry to represent this match to p1
        win_loss_dict[p1][p2].append((date, winner == p1))

        # add p2 to the dict
        if p2 not in win_loss_dict:
            win_loss_dict[p2] = {}

        if p1 not in win_loss_dict[p2]:
            win_loss_dict[p2][p1] = []

        win_loss_dict[p2][p1].append((date, winner == p2))

    # Compare this win_loss_dict to the tools/ genereated win_loss_dict
    urls = constants.SMS_URLS

    # TODO compare these two data to make sure we are doing it right
    #d2, _ = get_dated_data(urls, True)
    #assert(win_loss_dict == d2)
    #print(d2)

    #Now that we created this dict, calculate ranks
    ranks = get_ranks(win_loss_dict)
    return json.dumps(str(ranks))

@endpoints.route("/entrants")
def entrants(players=None):
    if db == None:
        init()

    sql = "SELECT base_url FROM analyzed;"
    urls = db.exec(sql, debug=False)

    # Create an array ofall the players that we want to search for
    if players == None:
        players = []
        for p in request.args:
            players.append(request.args[p])

    for p in players:
        # Create a long 'OR' clause. One for each 'url'
        # eg WHERE url = "url1" OR url = "url2" ...
        or_clause = "url = '{}' ".format(urls[0][0]) + " ".join(["OR url = '{}'".format(url[0]) for url in urls[1:]])
        
        # Grab all the URLs that this player has played in
        sql = "SELECT DISTINCT url FROM matches WHERE (player1 = '" + str(p) +\
                "' or player2 = '"+str(p)+"') AND (" + str(or_clause) +");"
        
        # This should be a list of all the URLs that all of the players have been in together
        urls = db.exec(sql)

        # If we ever get to an empty set of URLs, just return
        if len(urls) == 0:
            return json.dumps([])

    return json.dumps(urls)

@endpoints.route("/placings")
def placings():
    if db == None:
        init()

    tag = request.args.get('tag', default='christmas mike')

    print("args are: "+str(tag))
    # Get all the urls that this player has participated in
    sql = "SELECT * FROM placings WHERE player = '{}'".format(tag)
    results = list(db.exec(sql))
    results.sort(key=lambda x: int(x[2]))

    return json.dumps(results)

def init():
    global db
    db = DatabaseWriter()
