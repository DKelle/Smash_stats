import logger
import shared_data
import constants
import get_results
import time
import copy
import bracket_utils

LOG = logger.logger(__name__)

class processData(object):
    def __init__(self):
        print('loading constants for process')
        self.dated_base_scene = bracket_utils.get_list_of_named_scenes()
        self.list_of_scene = bracket_utils.get_list_of_scenes()

    def init(self):
        print('starting process data thread')

        while True:
            # iterate through all  scenes
            # eg, sms, smashbrews, etc
            for scene_list in self.dated_base_scene:

                # Start creating the dated data for this scene
                name = scene_list[0]
                base_urls = scene_list[1]
                win_loss_data = copy.deepcopy(get_results.get_data(base_urls))
                dated_win_loss_data = copy.deepcopy(get_results.get_dated_data(base_urls))
                if dated_win_loss_data:
                    # Now that we have the data for this scene, update shared data
                    shared_data.set_dated_data(name, dated_win_loss_data)

                if win_loss_data:
                   # Now that we have the win loss data for this scene, update shared data
                   shared_data.set_win_loss_data(name, win_loss_data)

            time.sleep(constants.SLEEP_TIME)
