from flask import Blueprint
import shared_data
import json

endpoints = Blueprint('endpoints', __name__)

@endpoints.route("/temp")
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

@endpoints.route("/rank_data")
def rank_data():
    return json.dumps(shared_data.get_rank_data())
