from logger import logger
import requests

LOG = logger(name='tweet')
def tweet(msg='temp'):

    try:
        r = requests.post("http://localhost:6969", data={'msg': msg}, timeout=30)
    except Exception:
        LOG.exc('Hit exception while trying to tweet message {}'.format(msg))
