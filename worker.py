import threading 
from logger import logger
import time

ALIVE = 0
KILLED = 1
RUNNING = 2

LOG = logger(__name__)
class Worker():

    def __init__(self, target=None, name=None):
        self.status = ALIVE
        self.target = target
        self.name = name

    def start(self):
        # Run the thread forever
        while True:
            LOG.info('About to start worker {}'.format(self.name))
            self.status = RUNNING
            self.run_target()

            # Keep checking on this threads status
            while self.status == RUNNING:
                # Check every 30 seconds
                time.sleep(30)
                pass

    def run_target(self):
        try:
            self.target()
        except Exception as e:
            LOG.exc("Setting status to killed for worker {}".format(self.name))
            self.status = KILLED
            LOG.info(e)

    def get_status(self):
        status_map = {ALIVE: 'ALIVE', KILLED: 'KILLED', RUNNING: 'RUNNING'}
        return status_map[self.status]
