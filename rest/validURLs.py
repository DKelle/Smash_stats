from scene import Scene
import logger
import bracket_utils
import shared_data

LOG = logger.logger(__name__)

class validURLs(object):
    def __init__(self, base_urls_list):
        self.base_urls_list = base_urls_list
        LOG.info("validURL being created")


    def init(self):
        print('valid urls has been started')
        scenes = []
        for base_url in self.base_urls_list:
            scenes.append(Scene(base_url))

        # Now that we have all the scenes we want to analyze,
        # continuously check for new brackets
        while True:
            new_range = {}
            for scene in scenes:

                # This scene will have several base URLs
                base_urls = scene.get_base_urls()
                for base_url in base_urls:
                    # get the first
                    first_url = bracket_utils._get_first_valid_url(base_url)
                    last_url = bracket_utils._get_last_valid_url(base_url, first_url)
                    print('Scanner base _urls ' + str(base_url))
                    print('First is ' + str(first_url))
                    print('last is ' + str(last_url))
                    LOG.info('Scanner base _urls ' + str(base_url))
                    LOG.info('First is ' + str(first_url))
                    LOG.info('last is ' + str(last_url))

                    # Create a map of base_url to the first and last valid urls
                    # eg. http://smashco.challonge.com/CSUWW###WUS : (32, 74)
                    new_range[base_url] = (first_url, last_url)

            # After we have calculated all valid url ranges,
            # Send this data to shared_data to keep
            shared_data.set_url_range_data(new_range)

