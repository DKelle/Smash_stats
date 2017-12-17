from flask import Blueprint, request
import json
from database_writer import DatabaseWriter

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

@endpoints.route("/win_loss_data")
def win_loss_data():
    return json.dumps(shared_data.get_win_loss_data())

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

def init():
    global db
    db = DatabaseWriter()
