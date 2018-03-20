import logger
import time
import requests
import constants
import json
LOG = logger.logger(__name__)

player_web = None
def update_web(winner, loser):
    global player_web
    if player_web == None:
        player_web = PlayerWeb()
        LOG.info("Creating the player web")
    player_web.update(winner, loser)

def get_hyper(tag):
    start = time.time()
    LOG.info('dallas: About to start calculating player data for {} at {}'.format(tag, start))
    if player_web == None:
        return {}
    # First, get the node for this player
    nid = player_web.get_id(tag, False)
    if nid:
        # Now, get all edges from this node
        edges = player_web.node_to_edges_map[nid]

        # Make a set of all other players this player has an edge to
        node_ids = set([edge['source'] for edge in edges])
        node_ids.update([edge['target'] for edge in edges])
        LOG.info("dallas: {} has played against these opponent IDs: {}".format(tag, node_ids))

        # Now that we have all node id, get a list of all nodes
        nodes = [player_web.nid_to_node_map[nid] for nid in node_ids]
        player_node = player_web.nid_to_node_map[nid]
        nodes.remove(player_node)

        child_list = {}
        child_list['id'] = player_node['id']
        child_list['name'] = player_node['label']
        child_list['children'] = []

        tag1 = player_node['label']
        for n in nodes:
            tag2 = n['label']
            LOG.info('dallas: about to send reqeust for {}'.format(tag2))
            #r = requests.get('https://{}:5000/h2h'.format(constants.DNS))
            LOG.info('dallas: just got back reqeust for {}'.format(tag2))
            #tournaments = json.loads(r.text)
            child_list['children'].append({'id':n['id'],
                                            'name':n['label'],
                                            'data':'{}-{}'.format(tag1,tag2)})
        end = time.time()
        LOG.info('dallas: Just finished calculating player web data at {}. Took {}'.format(end, end-start))
        return child_list


def get_web(tag=None):

    start = time.time()
    LOG.info('dallas: About to start calculating player data for {} at {}'.format(tag, start))
    if player_web == None:
        return {}
    if tag == None:
        web = player_web.get_json()
        LOG.info("dallas: tag is None, returning entire web")
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
            LOG.info("dallas: {} has played against these opponent IDs: {}".format(tag, node_ids))

            # Now that we have all node id, get a list of all nodes
            nodes = [player_web.nid_to_node_map[nid] for nid in node_ids]
            json = {'nodes': nodes, "edges": edges}
            end = time.time()
            LOG.info('dallas: Just finished calculating player web data at {}. Took {}'.format(end, end-start))
            return json

class PlayerWeb(object):
    def __init__(self):
        self.tag_nid_map = {}
        self.edge_id_map = {}
        self.eid_to_edge_map = {}
        self.nid_to_node_map = {}
        self.current_node_id = 1
        self.current_edge_id = 1
        self.node_to_edges_map = {}
        self.nodes = []
        self.edges = []

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
        # TODO fix up this link count
        node = {"name":tag, "count":1, "linkCount":1, "label":tag, "shortName":tag, "userCount":True, "group":"fake", "url":"www.google.com"}
        self.nodes.append(node)
        self.nid_to_node_map[id] = node
        LOG.info("Created a node for player {} with id {}".format(tag, id))

    def create_edge(self, wid, lid, id):
        edge = {"source":wid, "target":lid, "depth":9, "linkName":"www.google.com", "count":1}
        self.edges.append(edge) 
        self.eid_to_edge_map[id] = edge
        LOG.info("Created an edge from node id {} to node id {}".format(wid, lid))
        self.update_node_to_edges(wid, lid, id)

    def get_json(self):
        LOG.info("About to return the json for the player web")
        LOG.info("There are {} nodes and {} edges".format(len(self.nodes), len(self.edges)))
        data = {'nodes': self.nodes, "links": self.edges}

        json = {"d3":{"options":{"radius":2.5,"fontSize":9,"labelFontSize":9,"gravity":0.1,"height":800,"nodeFocusColor":"black","nodeFocusRadius":25,"nodeFocus":True,"linkDistance":150,"charge":-220,"nodeResize":"count","nodeLabel":"label","linkName":"tag"}, 'data':data}}
        
        return json

    def update_node_to_edges(self, wid, lid, eid):
        if wid not in self.node_to_edges_map:
            self.node_to_edges_map[wid] = []
        if lid not in self.node_to_edges_map:
            self.node_to_edges_map[lid] = []
        
        edge = self.eid_to_edge_map[eid]
        self.node_to_edges_map[wid].append(edge)
        self.node_to_edges_map[lid].append(edge)
