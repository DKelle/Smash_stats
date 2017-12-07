from manual_get_results import get_dated_data
from constants import AUSTIN_URLS, SMASHBREWS_RULS, COLORADO_SINGLES_URLS, COLORADO_DOUBLES_URLS, SMS_URLS

SQL_HEADER = """
DROP DATABASE IF EXISTS smash;
CREATE DATABASE smash;

USE smash;

DROP TABLES IF EXISTS players;
DROP TABLES IF EXISTS matches;

CREATE TABLE players(
	id INT,
	tag VARCHAR(100),
	PRIMARY KEY (id)
);

CREATE TABLE matches(
	player1 INT,
	player2 INT,
	tag1 VARCHAR(100),
	tag2 VARCHAR(100),
	date VARCHAR(100),
	win INT,
        FOREIGN KEY (player1) REFERENCES players(id),
        FOREIGN KEY (player2) REFERENCES players(id)
);

"""

def get_tag_id_map(data):
    tags = {}
    for i, tag in enumerate(data):
        tag = sanitize(tag)
        if not tag in tags:
            tags[tag] = i

    return tags

def create_insert_player_sql(tags):
    insert = "INSERT INTO players(tag, id) VALUES (###1, ###2);"
    inserts = []
    for tag in tags:
        id = tags[tag]
        tag_insert = insert.replace('###1', '\''+str(tag)+'\'').replace('###2', str(id))
        inserts.append(tag_insert)

    return inserts

def sanitize(tag):
    if '\'' in tag and not '\\\'' in tag:
        return tag.replace('\'', '\\\'')
    return tag

def create_insert_matches_sql(data, tags):
    insert = "INSERT INTO matches(player1, player2, tag1, tag2, date, win) VALUES(###1, ###2, ###3, ###4, ###5, ###6);"
    inserts = []
    for tag in data:
        for opponent in data[tag]:
            for match in data[tag][opponent]:
                s_tag = sanitize(tag)
                s_opponent = sanitize(opponent)
                p1_id = tags[s_tag]
                p2_id = tags[s_opponent]
                date = match[0]
                win = match[1]
                match_insert = insert.replace('###1', str(p1_id)).replace('###2', str(p2_id)).replace('###3', '\''+str(s_tag)+'\'')
                match_insert = match_insert.replace('###4', '\''+str(s_opponent)+'\'').replace('###5', '\''+str(date)+'\'').replace('###6', str(win))
                inserts.append(match_insert)

    return inserts
                

if __name__ == "__main__":
    base_urls = AUSTIN_URLS + SMASHBREWS_RULS + COLORADO_SINGLES_URLS + COLORADO_DOUBLES_URLS + SMS_URLS
    data = get_dated_data(base_urls)

    tags = get_tag_id_map(data)

    player_inserts = create_insert_player_sql(tags)
    matches_inserts = create_insert_matches_sql(data, tags)

    for p in player_inserts:
        SQL_HEADER += p + '\n'
    for m in matches_inserts:
        SQL_HEADER += m + '\n'


    with open('init_sql.txt', 'w') as f:
        for line in SQL_HEADER:
            f.write(line)

    print(matches_inserts)
