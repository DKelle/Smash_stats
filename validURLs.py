import logger
import bracket_utils
import constants
import time

LOG = logger.logger(__name__)

class validURLs(object):
    def __init__(self, scenes):
        self.scenes = scenes

        # Create a processor to analyze new matches
        print("validURL being created")


    def init(self):
        print('valid urls has been started')

        # Now that we have all the scenes we want to analyze,
        # continuously check for new brackets
        while True:
            for scene in self.scenes:

                # This scene will have several base URLs
                base_urls = scene.get_base_urls()
                name = scene.get_name()
                for base_url in base_urls:
                    prior_entries = False

                    # We need to create first and last from scratch
                    first = bracket_utils.temp(base_url)
                    last = bracket_utils.temp2(base_url, first)

                    print(base_url)
                    print(first)
                    print(last)


            time.sleep(constants.SLEEP_TIME)
