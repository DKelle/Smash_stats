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
ranks = {}
worst_rank = 1 

def update_web(match_pairs, db):
    if player_web == None:
        init_player_web()

    player_web.update(match_pairs, db)

def init_player_web():
    global player_web
    player_web = PlayerWeb()

    # vip TODO. Init the web + data structures from sql

    LOG.info("Creating the player web")

def update_ranks(tag_rank_map):
    player_web.update_ranks(tag_rank_map)

def get_web(tag=None, db=None):
    LOG.info('About to get the web, and db is {}'.format(db))
    start = time.time()
    LOG.info('About to start calculating player data for {} at {}'.format(tag, start))
    if player_web == None:
        return '{}'

    if tag == None:
        web = player_web.get_json()
        end = time.time()
        LOG.info('Just finished calculating player web data at {}. Took {}'.format(end, end-start))
        return web
    else:
        # First, get the node for this player
        nid = player_web.get_node(tag)

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
            LOG.info('Just finished calculating player web data at {}. Took {}'.format(end, end-start))
            return json

class PlayerWeb(object):
    def __init__(self, *args):
        # All of our node related data structures
        self.tag_nid_map = {}
        self.nid_to_node_map = {}
        self.nodes = []
        self.current_node_id = 0 

        # All of our edge related data structures
        self.id_to_opponents = {}
        self.node_to_edges_map = {}
        self.edges = []

        # There's a bug where the first node sometimes doesn't have any links... So make a fake node anyway
        self.create_node('No results', 9)

    def update(self, match_pairs, db):
        for match in match_pairs:
            winner, w_gid = match[:2]
            loser, l_gid = match[2:]

            # Do we already have nodes for these players?
            winner_node = self.get_node(winner)
            loser_node = self.get_node(loser)

            if winner_node == None:
                # Create a node for the winner of this match
                winner_node = self.create_node(winner, w_gid)
            else:
                # A node for this player already exists. Has the group changed?
                old_group = winner_node['group']
                if not old_group == w_gid:
                    winner_node['group'] = w_gid

                    # Save this node back
                    self.nodes[winner_node['id']] = winner_node

            if loser_node == None:
                # Create a node for the loser of this match
                loser_node = self.create_node(loser, l_gid)
            else:
                # A node for this player already exists. Has the group changed?
                old_group = loser_node['group']
                if not old_group == l_gid:
                    loser_node['group'] = l_gid

                    # Save this node back
                    self.nodes[loser_node['id']] = loser_node


            # Now that we have nodes for these two players, create an edge
            w_id = winner_node['id']
            l_id = loser_node['id']

            self.create_edge(w_id, l_id)
            
        # Update sql to have these changes
        sql_nodes = dumps(self.nodes)
        sql_links = dumps(self.edges)

        LOG.info('dallas: the size of nodes is {}'.format(len(sql_nodes)))
        sql = "UPDATE web SET nodes='{}', links='{}';".format(sql_nodes, sql_links)
        # This is a huge list... don't print it to the log
        LOG.info('Updating player web in sql')
        db.exec(sql)

    def get_node(self, tag):
        if tag not in self.tag_nid_map:
            return None
        return self.nodes[self.tag_nid_map[tag]]


    def create_node(self, tag, group):
        node_id = self.current_node_id
        node = {"id":node_id, "name":tag, "radius":15, "count":1, "linkCount":1, "label":tag, "shortName":tag, "userCount":True, "group":group, "url":"player/{}".format(node_id)}
        self.tag_nid_map[tag] = node_id
        self.nodes.append(node)
        self.nid_to_node_map[node_id] = node
        LOG.info("Created a node for player {} with id {}".format(tag, node_id))
        self.current_node_id = self.current_node_id + 1
        return node


    def create_edge(self, wid, lid):
        # Do we already have an edge between these players?
        for id in [wid, lid]:
            if not id in self.id_to_opponents:
                self.id_to_opponents[id] = []

        if lid in self.id_to_opponents[wid]:
            return
        if wid in self.id_to_opponents[lid]:
            LOG.info('ERROR: lid has played wid, but wid has not played lid. wid: {}, lid: {}'.format(wid, lid))
            return

        # These two have not played each other. Create an edge
        edge = {"source":wid, "target":lid, "depth":9, "linkName":"www.google.com", "count":1}
        self.edges.append(edge) 

        self.update_node_to_edges(wid, lid, edge)
        return edge


    def update_node_to_edges(self, wid, lid, edge):
        if wid not in self.node_to_edges_map:
            self.node_to_edges_map[wid] = []
        if lid not in self.node_to_edges_map:
            self.node_to_edges_map[lid] = []
        
        self.node_to_edges_map[wid].append(edge)
        self.node_to_edges_map[lid].append(edge)

    
    def update_ranks(self, tag_rank_map):
        for tag in tag_rank_map:
            total_ranked = tag_rank_map[tag]['total_ranked']
            rank = tag_rank_map[tag]['rank']
            
            # calulate the size off of the rank
            power = 6.0
            min_size = pow(10, (1.0/power))
            max_size = pow(65, (1.0/power))
            size = min_size 
            if total_ranked > 1:
                inverted_rank = total_ranked - rank
                normalized_rank = (inverted_rank+0.0)*(max_size+0.0)/(total_ranked+0.0)
                # Filter out anything lower than min_size
                size = max(min_size, normalized_rank)
                # Filter out anything lager than max_size
                size = min(size, max_size)
            size = pow(size, power)

            # Get our node, and set its radius
            nid = self.tag_nid_map[tag]
            node = self.nodes[nid]

            node['radius'] = size
            node['rank'] = rank

            # Save our node back
            self.nodes[nid] = node


    def get_json(self):
        LOG.info("About to return the json for the player web")
        LOG.info("There are {} nodes and {} edges".format(len(self.nodes), len(self.edges)))
        
        #for node in self.nodes:
        #    ranked_node = node
        #    total_ranked = worst_rank
        #    tag = ranked_node['name']
        #    
        #    # default to a low rank
        #    rank, total_ranked = worst_rank, worst_rank
        #    if self.tag_rank_map and tag in self.tag_rank_map:
        #        rank, total_ranked = self.tag_rank_map[tag]['rank'], self.tag_rank_map[tag]['total_ranked']

        #    # calulate the size off of the rank
        #    power = 6.0
        #    min_size = pow(10, (1.0/power))
        #    max_size = pow(65, (1.0/power))
        #    size = min_size 
        #    if total_ranked > 1:
        #        inverted_rank = total_ranked - rank
        #        normalized_rank = (inverted_rank+0.0)*(max_size+0.0)/(total_ranked+0.0)
        #        # Filter out anything lower than min_size
        #        size = max(min_size, normalized_rank)
        #        # Filter out anything lager than max_size
        #        size = min(size, max_size)
        #    size = pow(size, power)

        #    ranked_node['radius'] = size
        #    ranked_node['rank'] = rank
        #    ranked_nodes.append(ranked_node)


        data = {'nodes': self.nodes, "links": self.edges}

        json = {"d3":{"options":{"radius":2.5,"fontSize":9,"labelFontSize":20,"gravity":.05,"nodeFocusColor":"black","nodeFocusRadius":25,"nodeFocus":True,"linkDistance":190,"charge":-3000,"nodeResize":"count","nodeLabel":"label","linkName":"tag"}, 'data':data}}
        
        return dumps(json)
