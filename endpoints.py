from flask import Blueprint, request
from get_ranks import get_ranks
import json
from database_writer import DatabaseWriter
#sys.path.insert(0, '/home/ubuntu/Smash_stats/tools')
#from tools import  

db = None

endpoints = Blueprint('endpoints', __name__)

@endpoints.route("/")
def temp():
    return "temp"

@endpoints.route("/valid_urls")
def valid_urls():
    return json.dumps(shared_data.get_valid_range())

@endpoints.route("/dated_data")
def dated_data():
    return json.dumps(shared_data.get_dated_data())

#@endpoints.route("/win_loss_data")
#def win_loss_data():
#    return json.dumps(shared_data.get_win_loss_data())

@endpoints.route("/rank_data/")
def rank_data():
    scene = request.args.get('scene', default=None)
    rank_data = shared_data.get_rank_data()

    if scene in rank_data:
        return json.dumps(rank_data[scene])
    return json.dumps(rank_data)

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
    d2, _ = get_dated_data(urls, True)
    assert(win_loss_dict == d2)
    print(d2)

    #Now that we created this dict, calculate ranks
    ranks = get_ranks(win_loss_dict)
    return json.dumps(str(ranks))

@endpoints.route("/both_entrants")
def both_entrants():
    if db == None:
        init()

    sql = "SELECT base_url FROM analyzed;"
    urls = db.exec(sql)

    player1 = request.args.get('player1', default="Christmas mike")
    player2 = request.args.get('player2', default="Christmas mike")
    # Collect all the URLs that these players were in together
    common = []
    for url in urls:
        sql = "SELECT * FROM matches WHERE url = '"+str(url[0])+"';"
        matches = db.exec(sql)

        p1_matches = []
        p2_matches = []
        perge = lambda l, p: [x for x in l if p == x[0] or p == x[1]]
        urls_p1_in = [] 
        for match in matches:
            if player1 in match and match[5] not in urls_p1_in:
                urls_p1_in.append(match[5])
                # We have all the brackets, now find the ones p2 has played in
                sql = "SELECT * FROM matches WHERE (player1 = '" + str(player2) +\
                        "' or player2 = '"+str(player2)+"') AND url = '" + str(match[5]) +\
                        "';"
                both_entered = db.exec(sql)
                no_dups = list(set([x[5] for x in both_entered]))
                common = common + list(no_dups)
                print(both_entered)

    return json.dumps(common)

def init():
    global db
    db = DatabaseWriter()
