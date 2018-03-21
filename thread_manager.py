from validURLs import validURLs
from process_data import processData
from scene import Scene
import constants
import threading
import logger
import constants
import get_ranks
import bracket_utils
from worker import Worker

LOG = logger.logger(__name__)

def run():

    # Construct all of our 'scenes'

    base_urls = bracket_utils.get_list_of_scenes()
    scenes = [Scene(x[0], x[1]) for x in base_urls]
    valids = validURLs(scenes)
    data_processor = processData()

    LOG.info("Creating the following worker threads")
    # threading.Thread(target=valids.init).start()

    ## Create a list of worker threads
    #workers = [valids.init, data_processor.init, get_ranks.get_ranks, interaction.interact, gen_html.init]
    threads = [valids.init]

    for thread in threads:
        LOG.info("Starting thread {}".format(str(thread)))
        w = Worker(target=thread, name="validURLs")
        t = threading.Thread(target=w.start)
        t.daemon = True
        t.start()

def main():
    run()

if __name__ == "__main__":
    main()
