import logger

LOG = logger.logger(__name__)

class Scene(object):
    def __init__(self, scene_name, base_urls):
        self.base_urls=base_urls
        self.scene_name = scene_name
        LOG.info('Creating a Scene with base urls: ' + str(base_urls))

    def get_base_urls(self):
        return self.base_urls

    def get_name(self):
        return self.scene_name
