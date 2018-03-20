import bracket_utils
import pymysql.cursors
import sys
import re

# Which util do we want to use?
util = sys.argv[1]

if util == "watch":
    table = sys.argv[2]
    base_urls = bracket_utils.get_list_of_scenes()
    con = pymysql.connect(host='localhost', user='root', password='password', db='smash')

    for b in base_urls:
        urls = b[-1]
        for u in urls:
            atr = "url" if table == "matches" else "url" if table == "placings" else "base_url"
            if table == "analyzed" or table == "matches" or table == "placings":
                u = u.replace("###", "1")
            stmnt = "select * from " + str(table) + " where " + str(atr) + " = '"+str(u)+"';";
            print('stmnt: '+ str(stmnt))
            with con.cursor() as cur:
                cur.execute(stmnt)

            result = cur.fetchall()
            print('reslts are ' + str(result))

    con.commit()
    con.close()

if util == "clear":
    if len(sys.argv) > 2:
        tables = [sys.argv[2]]
    else:
        #TODO should make this automated - don't want a hardcoded list of tables
        tables = ['players', 'valids', 'matches', 'analyzed', 'placings', 'ranks']

    for table in tables:
        con = pymysql.connect(host='localhost', user='root', password='password', db='smash')
        stmnt = "TRUNCATE TABLE "+str(table)+";";
        with con.cursor() as cur:
            cur.execute(stmnt)

        con.commit()
        con.close()

if util == "init":
    sql= """
    drop table matches;
    drop table valids;
    drop table analyzed;
    drop table players;
    drop table placings;
    drop table ranks;
    CREATE TABLE players (
        id int NOT NULL AUTO_INCREMENT,
        tag varchar(255) NOT NULL,
        PRIMARY KEY (id)
    );

    CREATE TABLE matches (
        player1 varchar(255) NOT NULL,
        player2 varchar(255) NOT NULL,
        winner varchar(255) NOT NULL,
        date varchar(255) NOT NULL,
        scene varchar(255) NOT NULL,
        url varchar(255) not null
    );

    CREATE TABLE valids (
        base_url varchar(255) NOT NULL,
        first int NOT NULL,
        last int NOT NULL,
        scene varchar(255)
    );

    CREATE TABLE analyzed (
        base_url varchar(255) not null
    );

    CREATE TABLE placings (
        url varchar(255) NOT NULL,
        player varchar(255) NOT NULL,
        place varchar(256) NOT NULL
    );

    CREATE TABLE ranks (
        scene varchar(255) NOT NULL,
        player varchar(255) NOT NULL,
        rank varchar(256) NOT NULL,
        points varchar(256) NOT NULL
    );

    """
    #FOREIGN KEY (player1) REFERENCES players(id)
    con = pymysql.connect(host='localhost', user='root', password='password', db='smash')
    with con.cursor() as cur:
        cur.execute(sql)

    con.commit()
    con.close()

if util == "help":
    options = ['init', 'clear', 'watch']
    print('Options are \n' + str(options))
