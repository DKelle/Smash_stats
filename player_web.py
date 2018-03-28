import logger
import threading
import time
import requests
import constants
import queue
from worker import Worker
from json import dumps, loads
from random import randint
LOG = logger.logger(__name__)

player_web = None
q = None
ranks = {}
worst_rank = 1 
def update_web(winner_loser_pairs):
    if player_web == None:
        init_player_web()
    q.put_nowait(winner_loser_pairs)

def init_player_web():
    global player_web
    global q
    q = queue.Queue()
    player_web = PlayerWeb(q)

    # Start running the player web in a thread
    w = Worker(target=player_web.run, name="PlayerWeb")
    t = threading.Thread(target=w.start)
    t.daemon = True
    t.start()

    LOG.info("Creating the player web")

def update_group(tag, group_id):
    player_web.update_group_id(tag, group_id)

def get_web(tag=None, db=None):
    LOG.info('dallas: about to get the web, and db is {}'.format(db))
    start = time.time()
    LOG.info('dallas: About to start calculating player data for {} at {}'.format(tag, start))
    if player_web == None:
        return '{}'

    # Make sure we have the most updated ranks
    init_ranks(db)

    if tag == None:
        web = player_web.get_json()
        end = time.time()
        LOG.info('dallas: Just finished calculating player web data at {}. Took {}'.format(end, end-start))
        return web
    else:
        # First, get the node for this player
        nid = player_web.get_id(tag, False)

        if nid:
            # Now, get all edges from this node
            edges = player_web.node_to_edges_map[nid]

            # Make a set of all other players this player has an edge to
            node_ids = set([edge['source'] for edge in edges])
            node_ids.update([edge['target'] for edge in edges])

            # Now that we have all node id, get a list of all nodes
            nodes = [player_web.nid_to_node_map[nid] for nid in node_ids]
            json = {'nodes': nodes, "edges": edges}
            end = time.time()
            LOG.info('dallas: Just finished calculating player web data at {}. Took {}'.format(end, end-start))
            return json

def init_ranks(db):
    global ranks
    global worst_rank
    ranks = {}

    if db == None:
        ranks = {}
        return

    sql = "SELECT count(rank) FROM ranks;"
    res = db.exec(sql)
    # Do we even have rank info yet?
    if res[0][0] == 0:
        return

    LOG.info('dallas: tyring to get the worse rank adn found {}'.format(res))
    worst_rank = res[0][0]

    sql = "SELECT * FROM ranks"
    res = db.exec(sql)

    for r in res:
        player = r[1]
        rank = int(r[2])
        LOG.info('dallas: setting the rank of {} to {}'.format(player, rank))
        ranks[player] = rank

class PlayerWeb(object):
    def __init__(self, *args):
        self.q = args[0]
        self.tag_nid_map = {}
        self.edge_id_map = {}
        self.eid_to_edge_map = {}
        self.nid_to_node_map = {}
        self.current_node_id = 0 
        self.current_edge_id = 0
        self.node_to_edges_map = {}
        self.nodes = []
        self.edges = []

    def run(self):
        while True:
            try:
                winner_loser_pairs = self.q.get(timeout=5)
            except queue.Empty:
                pass
            except Exception:
                LOG.info('The player web has hit an unexpected exception! Dying')

            for winner, loser in winner_loser_pairs:
                self.update(winner, loser)

    def update(self, winner, loser):
        wid = self.get_id(winner)
        lid = self.get_id(loser)

        eid = self.get_edge_id(wid, lid)

    def get_edge_id(self, wid, lid):
        # Do we already have an edge between these two players?
        if (wid,lid) in self.edge_id_map:
            return self.edge_id_map[(wid,lid)]
        elif (lid,wid) in self.edge_id_map:
            return self.edge_id_map[(lid,wid)]

        else:
            # We don't have an edge for these two. Make one
            self.edge_id_map[(wid,lid)] = self.current_edge_id
            self.create_edge(wid, lid, self.current_edge_id)
            self.current_edge_id = self.current_edge_id + 1
            return self.edge_id_map[(wid,lid)]


    def get_id(self, tag, create=True):
        # Do we already have an ID mapped to this player?
        if not tag in self.tag_nid_map and create:
            self.tag_nid_map[tag] = self.current_node_id
            # If we don't, we need to create an edge to this player also
            self.create_node(tag, self.current_node_id)
            self.current_node_id = self.current_node_id + 1
        elif not tag in self.tag_nid_map:
            return None
        return self.tag_nid_map[tag]

    def create_node(self, tag, id):
        node = {"id":id, "name":tag, "count":1, "linkCount":1, "label":tag, "shortName":tag, "userCount":True, "group":0, "url":"player/{}".format(id)}
        self.nodes.append(node)
        self.nid_to_node_map[id] = node
        LOG.info("Created a node for player {} with id {}".format(tag, id))


    def update_group_id(tag, group_id):
        # update this nodes group ID
        nid = self.tag_nid_map[tag]
        node = self.nodes[nid]
        # TODO remove
        LOG.info('dallas: about to see if this group ID has changed... It was {}'.format(node['group']))
        node['group'] = group_id
        # TODO remove
        LOG.info('dallas: and it is now {}'.format(group_id))

        # Save this node back to our maps
        self.nodes[nid] = node
        self.nid_to_node_map[nid] = node


    def create_edge(self, wid, lid, id):
        edge = {"source":wid, "target":lid, "depth":9, "linkName":"www.google.com", "count":1}
        self.edges.append(edge) 

        self.eid_to_edge_map[id] = edge
        LOG.info("Created an edge from node id {} to node id {}".format(wid, lid))
        self.update_node_to_edges(wid, lid, id)

    def get_json(self):
        LOG.info("About to return the json for the player web")
        LOG.info("There are {} nodes and {} edges".format(len(self.nodes), len(self.edges)))
        ranked_nodes = []
        for node in self.nodes:
            ranked_node = node
            tag = ranked_node['name']
            rank = worst_rank if not tag in ranks else ranks[tag]

            # calulate the size off of the rank
            min_size = 10
            max_size = 50
            size = min_size 
            if worst_rank > 1:
                rank = worst_rank - rank
                normalized_rank = (rank+0.0)*(max_size+0.0)/(worst_rank+0.0)
                # Filter out anything lower than min_size
                size = max(min_size, normalized_rank)
                # Filter out anything lager than max_size
                size = min(size, max_size)

            ranked_node['radius'] = size
            LOG.info('dallas; setting the radius of node {} to {}'.format(tag, size))
            ranked_nodes.append(ranked_node)
        data = {'nodes': ranked_nodes, "links": self.edges}

        json = {"d3":{"options":{"radius":2.5,"fontSize":9,"labelFontSize":9,"gravity":.05,"nodeFocusColor":"black","nodeFocusRadius":25,"nodeFocus":True,"linkDistance":150,"charge":-1000,"nodeResize":"count","nodeLabel":"label","linkName":"tag"}, 'data':data}}
        
        return dumps(json)

    def update_node_to_edges(self, wid, lid, eid):
        if wid not in self.node_to_edges_map:
            self.node_to_edges_map[wid] = []
        if lid not in self.node_to_edges_map:
            self.node_to_edges_map[lid] = []
        
        edge = self.eid_to_edge_map[eid]
        self.node_to_edges_map[wid].append(edge)
        self.node_to_edges_map[lid].append(edge)
