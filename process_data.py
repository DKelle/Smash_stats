import logger
import constants
import get_results
import time
import copy
import bracket_utils
from database_writer import DatabaseWriter

LOG = logger.logger(__name__)

class processData(object):
    def __init__(self):
        print('loading constants for process')
        self.dated_base_scene = bracket_utils.get_list_of_named_scenes()
        self.list_of_scene = bracket_utils.get_list_of_scenes()
        self.db = DatabaseWriter()

    def process(self, bracket, scene):
        # Send this bracket to get_results
        get_results.process(bracket, scene, self.db)
