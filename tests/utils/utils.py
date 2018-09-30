def setup_db(db):
    db.create_db()
    tables  = ["""
    CREATE TABLE players (
        id int NOT NULL AUTO_INCREMENT,
        tag varchar(255) NOT NULL,
        matches_per_scene varchar(255) NOT NULL,
        scene varchar(255) NOT NULL,
        PRIMARY KEY (id)
    );""",

    """CREATE TABLE matches (
        player1 varchar(255) NOT NULL,
        player2 varchar(255) NOT NULL,
        winner varchar(255) NOT NULL,
        date varchar(255) NOT NULL,
        scene varchar(255) NOT NULL,
        url varchar(255) not null,
        display_name varchar(255) not null,
        score varchar(255) not null
    );""",

    """CREATE TABLE valids (
        base_url varchar(255) NOT NULL,
        first int NOT NULL,
        last int NOT NULL,
        scene varchar(255)
    );""",

    """CREATE TABLE analyzed (
        base_url varchar(255) not null
    );""",

    """CREATE TABLE user_analyzed (
        url varchar(255) not null,
        user varchar(255) not null,
        scene varchar(255) not null
    );""",

    """CREATE TABLE placings (
        url varchar(255) NOT NULL,
        player varchar(255) NOT NULL,
        place varchar(256) NOT NULL
    );""",

    """CREATE TABLE ranks (
        scene varchar(255) NOT NULL,
        player varchar(255) NOT NULL,
        rank int NOT NULL,
        points varchar(256) NOT NULL,
        date varchar(256) NOT NULL
    );"""]

    for table in tables:
        db.exec(table)

def teardown_db(db):
    drop = "DROP DATABASE {}".format(db.db)
    db.exec(drop)
