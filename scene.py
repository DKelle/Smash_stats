import logger

LOG = logger.logger(__name__)

class Scene(object):
    def __init__(self, scene_name, url_info):
        self.base_urls = [] if 'enumerated' not in url_info else url_info['enumerated']
        self.users = [] if 'users' not in url_info else url_info['users']
        self.scene_name = scene_name
        LOG.info('Creating a Scene with base urls: ' + str(self.base_urls))

    def get_base_urls(self):
        return self.base_urls

    def get_users(self):
        return self.users

    def get_name(self):
        return self.scene_name
