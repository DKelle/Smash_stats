from validURLs import validURLs
from constants import TEST_URLS
from scene import Scene
from database_writer import DatabaseWriter
from testing.testing_data import all_match_data
from player_web import get_web
from json import loads

def main():
    # actually analyze all of the test data
    analyze_test_data()

    # start running the tests
    db = DatabaseWriter(db='smash_test')
    run_tests(db)

def analyze_test_data():
    # Get the test bracket urls
    scenes = [Scene(TEST_URLS[0], TEST_URLS[1])]

    # Now start analyzing the URLs
    valids = validURLs(scenes, testing=True)
    valids.init()

def run_tests(db):
    test_web(db)
    test_all_players_exist(db)
    test_all_matches_exist(db)
    test_placings(db)
    test_valids(db)
    test_analyzed(db)
    test_endpoints(db)
    pass

def test_web(db):
    print('About to run web tests...')
    web = get_web()
    web = loads(get_web())
    data = web['d3']['data']
    nodes = data['nodes']
    links = data['links']

    existing_links = [[False] * len(nodes)] * len(nodes)
    tags_to_node_index = {}
    # Make sure that every link has a corresponding match
    for link in links:
        n1 = nodes[link['source']]
        n2 = nodes[link['target']]
        t1 = n1['name']
        t2 = n2['name']
        tags_to_node_index[t1] = link['source']
        tags_to_node_index[t2] = link['target']
        sql = "SELECT * FROM matches WHERE (player1='{}' AND player2='{}') OR (player1='{}' AND player2='{}');".format(t1,t2,t2,t1)
        db.exec(sql, testing=True)

        # Mark this link as existing
        existing_links[link['source']][link['target']] = True
        existing_links[link['target']][link['source']] = True

    # Make sure that every match has a corresponding link
    sql = "SELECT * FROM matches;"
    res = db.exec(sql)
    for match in res:
        t1 = match[0]
        t2 = match[1]
        i1 = tags_to_node_index[t1]
        i2 = tags_to_node_index[t2]

        print('Testing there is a link between {} and {}'.format(t1, t2))
        # Make sure there is a link between these two players
        assert existing_links[i1][i2]
        assert existing_links[i2][i1]

    print('Web tests have passed')
    

def test_all_players_exist(db):
    print('About to test_all_players_exist...')
    # The players in these brackets are named a - z
    # Make sure we have all of them
    sql = "SELECT * FROM players;"
    results = db.exec(sql)
    assert len(results) == 26

    # Now check the player names individually
    for i in range(26):
        tag = chr(ord('a') + i)
        sql = "SELECT * FROM players WHERE tag='{}';".format(tag)
        result = db.exec(sql, testing=True)
        assert len(result) == 1

        sql = "DELETE FROM players WHERE tag='{}' LIMIT 1;".format(tag)
        db.exec(sql)

    # We should have deleted every player. Make sure the table is empty
    sql = "SELECT * FROM players;"
    res = db.exec(sql, testing=True)
    assert len(res) == 0

    print('player tests have passed')

def test_all_matches_exist(db):
    print('About to test_all_matches_exist...')
    for match_data in all_match_data:
        matches = match_data['matches']
        for tag in matches:
            wins = matches[tag]
            for op in wins:
                # Make sure that 'tag' has a recorded win agasint 'op'
                sql = "SELECT * FROM matches WHERE (player1='{}' OR player2='{}') AND winner='{}';".format(op,op,tag)
                res = db.exec(sql, testing=True)
                assert len(res) > 0

                sql = "DELETE FROM matches WHERE (player1='{}' OR player2='{}') AND winner='{}' LIMIT 1;".format(op,op,tag)
                db.exec(sql)

    # Now that we have finished with this, we should have an empty database
    sql = "SELECT * FROM matches;"
    res = db.exec(sql, testing=True)
    assert len(res) == 0

    print('match tests have passed')

def test_placings(db):
    print('About to test_placings...')
    for match_data in all_match_data:
        url = match_data['url']
        placings = match_data['placings']
        for tag in placings:
            place = placings[tag]
            # Make sure we have data about this players final placement in this bracket
            sql = "SELECT * FROM placings WHERE url='{}' AND player='{}' AND place={}".format(url, tag, place)
            res = db.exec(sql, testing=True)
            assert len(res) == 1
            sql = "DELETE FROM placings WHERE url='{}' AND player='{}' AND place={} LIMIT 1".format(url, tag, place)
            res = db.exec(sql)

    sql = "SELECT * FROM placings;"
    res = db.exec(sql, testing=True)
    assert len(res) == 0

    print('placing tests have passed')

def test_valids(db):
    print('About to test valids...')
    # The valid tournaments are 2-7
    sql = "SELECT first, last FROM valids";
    res = db.exec(sql, testing=True)
    first = res[0][0]
    last = res[0][1]
    assert first == 2
    assert last == 7
    print('Valids tests have passed')

def test_analyzed(db):
    print('About to test analyzed')
    for match_data in all_match_data:
        url = match_data['url']
        sql = "SELECT * FROM analyzed WHERE base_url='{}';".format(url)
        res = db.exec(sql, testing=True)
        assert len(res) == 1

        sql = "DELETE FROM analyzed WHERE base_url='{}' LIMIT 1;".format(url)
        db.exec(sql)

    sql = "SELECT * FROM analyzed;"
    res = db.exec(sql, testing=True)

    assert len(res) == 0
    print('analyzed tests passed')

def test_endpoints(db):
    pass

if __name__ == "__main__":
    main()
