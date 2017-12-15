from scene import Scene
import pymysql.cursors
import logger
import bracket_utils
import shared_data
import constants
import time

LOG = logger.logger(__name__)

class DatabaseWriter(object):
    def __init__(self, db='smash'):
        print('trying to make db writer')

        # Connect to our database
        con = pymysql.connect(host='localhost', user='root', password='password', db=db)
        self.con = con
        print('done making db writer')

    def exec(self, stmnt):
        print('trying to exec ' + stmnt)
        try:
            with self.con.cursor() as cur:
                cur.execute(stmnt)

            self.con.commit()
            
            results = cur.fetchall()
            return results
        finally:
            print('database writer is done execing')
