from validURLs import validURLs
from process_data import processData
import constants
import threading
import logger
import shared_data
import constants
import get_ranks
import interaction
import bracket_utils
import gen_html

LOG = logger.logger(__name__)

def main():

    base_urls = bracket_utils.get_list_of_scenes()
    valids = validURLs(base_urls)
    data_processor = processData()

    print('creating worker threads')
    LOG.info("Creating the following worker threads")
    # threading.Thread(target=valids.init).start()

    ## Create a list of worker threads
    workers = [valids.init, data_processor.init, get_ranks.get_ranks, interaction.interact, gen_html.init]

    for worker in workers:
        print(str(worker))
        LOG.info(str(worker))
        t = threading.Thread(target=worker)
        t.start()


if __name__ == "__main__":
    main()


