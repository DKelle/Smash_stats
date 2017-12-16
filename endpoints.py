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

    palyer = request.args.get('player', default="Christmas mike")
    sql = "SELECT * FROM matches WHERE winner = '"+str(player)"';"
    result = db.exec(sql)

    return result

def init():
    db = DatabaseWriter()
