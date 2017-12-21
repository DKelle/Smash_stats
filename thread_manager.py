from validURLs import validURLs
from scene import Scene
import constants
import threading
import logger
import constants
import get_ranks
import interaction
import bracket_utils
import gen_html

LOG = logger.logger(__name__)

def run():

    # Construct all of our 'scenes'

    base_urls = bracket_utils.get_list_of_scenes()
    scenes = [Scene(x[0], x[1]) for x in base_urls]
    valids = validURLs(scenes)

    print('creating worker threads')
    LOG.info("Creating the following worker threads")
    # threading.Thread(target=valids.init).start()

    ## Create a list of worker threads
    #workers = [valids.init, data_processor.init, get_ranks.get_ranks, interaction.interact, gen_html.init]
    workers = [valids.init]

    for worker in workers:
        print(str(worker))
        LOG.info(str(worker))
        t = threading.Thread(target=worker)
        t.start()


def main():
    run()


if __name__ == "__main__":
    main()
