import logging
import os
import subprocess
from datetime import datetime

max_size = 1 * 1000000
fname = 'smash.log'
logging.basicConfig(filename=fname,level=logging.INFO)


class logger():
    def __init__(self, name):
        self.name = name

    def info(self, msg):
        s = self.check_file_size()
        date = datetime.now()
        logging.info("[{}:{}]: {} - {}b".format(self.name, date, msg, s))

    def exc(self, msg):
        s = self.check_file_size()
        date = datetime.now()
        msg = "[{}:{}]: {} - {}b".format(self.name, date, msg, s)
        logging.exception(msg)
        # Print this so it also goes to the screen, and is more easily noticiable
        print(msg)


    def check_file_size(self):
        size = os.stat(fname).st_size

        # Is this log getting to big? Clear it
        # if size > max_size:
        #     # Truncate this file, it's too big
        #     print('dallas: DELETING FILE')
        #     cmd = "truncate {} --size 0".format(fname)
        #     subprocess.check_output(cmd.split())

        return size
