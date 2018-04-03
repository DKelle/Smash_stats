from flask import Blueprint, request, render_template, send_from_directory
from player_web import get_web
import json
from database_writer import DatabaseWriter
import constants
import bracket_utils
import requests
#sys.path.insert(0, '/home/ubuntu/Smash_stats/tools')
#from tools import  

db = None

BASE_URL = 'https://localhost:5000'
endpoints = Blueprint('endpoints', __name__)

@endpoints.route("/")
def main():
    if db == None:
        init()

    tag = request.args.get('tag', default="christmasmike")
    data = get_web(db=db)
    return render_template('libraries/html/interactive.html', data=data, tag=tag)
    #return render_template('libraries/html/temp.html', data=data, tag=tag)

@endpoints.route("/temp")
def temp():
    return render_template('libraries/html/legend.html')
    #return render_template('libraries/html/temp.html', data=data, tag=tag)

@endpoints.route("/wins")
def wins():
    if db == None:
        init()

    player = request.args.get('tag', default="christmasmike")
    sql = "SELECT * FROM matches WHERE winner = '"+str(player)+"' ORDER BY date DESC;"
    result = db.exec(sql)

    result = [str(x) for x in result]
    result = '\n'.join(result)
    return json.dumps(result)
    return render_template('hello.html', wins=result)

@endpoints.route("/losses")
def losses():
    if db == None:
        init()

    player = request.args.get('tag', default="christmasmike")
    sql = "SELECT * FROM matches WHERE (player1 = '"+str(player)+"' OR "\
            +"player2 = '"+str(player)+"') AND winner != '"+str(player)+"' ORDER BY date DESC;"
    result = db.exec(sql)

    result = [str(x) for x in result]
    return json.dumps('\n'.join(result))

@endpoints.route("/h2h")
def h2h():
    if db == None:
        init()

    player1 = request.args.get('tag1', default="christmasmike")
    player2 = request.args.get('tag2', default="christmasmike")
    sql = "SELECT * FROM matches WHERE (player1 = '"+str(player1)+"' OR "\
            +"player2 = '"+str(player1)+"') AND (player1 = '"+str(player2)+"' OR "\
            +"player2 = '"+str(player2)+"') ORDER BY date DESC;"
    result = db.exec(sql)

    result = [str(x) for x in result]
    return json.dumps('\n'.join(result))

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

    #result = [str(x) for x in result]
    return json.dumps(urls)
    return json.dumps('\n'.join(urls))

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

@endpoints.route("/ranks")
def ranks():
    if db == None:
        init()

    scene = request.args.get('scene', default='austin')

    # Get all the urls that this player has participated in
    sql = "SELECT * FROM ranks WHERE scene = '{}'".format(scene)
    results = list(db.exec(sql))

    return json.dumps(results)

@endpoints.route('/graph')
def serve_page():
    tag = request.args.get('tag', default=None)
    data = web(tag)
    #return render_template('web.html', data=data)
    return render_template('libraries/vis-4.21.0/examples/network/basicUsage.html', data=data)

@endpoints.route('/web')
def web(tag=None):
    if db == None:
        init()

    return json.dumps(get_web(tag, db=db))

def init():
    global db
    db = DatabaseWriter()
    
@endpoints.route('/templates/<path:path>')
def serve(path):
    return send_from_directory('templates', path)
