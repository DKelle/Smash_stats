from validURLs import validURLs
import constants
import threading
import logger
import shared_data

LOG = logger.logger(__name__)

def main():
    austin = constants.AUSTIN_URLS
    smashbrews = constants.SMASHBREWS_RULS
    colorado_singles = constants.COLORADO_SINGLES_URLS
    colorado_doubles= constants.COLORADO_DOUBLES_URLS
    colorado = constants.COLORADO_URLS = constants.COLORADO_SINGLES_URLS + constants.COLORADO_DOUBLES_URLS
    sms = constants.SMS_URLS

    base_urls = [austin, smashbrews, colorado_singles, colorado_doubles, colorado, sms]
    valids = validURLs(base_urls)
    print('creating worker threads')
    LOG.info("Creating the following worker threads")
    # threading.Thread(target=valids.init).start()

    ## Create a list of worker threads
    workers = [valids.init]

    for worker in workers:
        print(str(worker))
        LOG.info(str(worker))
        t = threading.Thread(target=worker)
        t.start()


if __name__ == "__main__":
    main()


