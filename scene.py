import logger

LOG = logger.logger(__name__)

class Scene(object):
    def __init__(self, base_urls):
        self.base_urls=base_urls
        LOG.info('Creating a Scene with base urls: ' + str(base_urls))

    def get_base_urls(self):
        return self.base_urls


