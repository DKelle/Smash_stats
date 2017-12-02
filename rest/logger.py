import logging

class logger(object):
    def __init__(self, name):

        logging.basicConfig(filename='smash.log',
            filemode='a',
            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG)

    def info(self, message):
        logging.info(message)
