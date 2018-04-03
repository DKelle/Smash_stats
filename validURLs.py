from database_writer import DatabaseWriter
from process_data import processData
from threading import Thread
import logger
import bracket_utils
import constants
import time
from tweet import tweet

# TODO this is temporary test code
loaded_smashgg = False

LOG = logger.logger(__name__)

class validURLs(object):
    def __init__(self, scenes, testing=False):
        self.testing = testing
        self.scenes = scenes
        db_name = 'smash_test' if testing else 'smash'
        self.db = DatabaseWriter(db=db_name)

        # Create a processor to analyze new matches
        self.data_processor = processData(self.db) 
        LOG.info("validURL being created")


    def init(self):
        if not self.testing:
            while True:
                LOG.info('dallas: about to create analyziz threads')
                self.create_analysis_threads()
                LOG.info('dallas: just finished with analysis threads')
                time.sleep(constants.SLEEP_TIME)
                LOG.info('dallas: Just finished sleeping')

        # If we are testing, we only want to run once, and then check our state
        else:
            self.create_analysis_threads()

    def create_analysis_threads(self):
        global loaded_smashgg
        # Create one thread to analyze each scene
        threads = []

        #for scene in self.scenes:

        #    t = Thread(target=self.analyze_scene, args=(scene,))
        #    LOG.info('dallas: Trying to start the analysis thread for {}'.format(scene.get_name()))
        #    t.start()
        #    threads.append(t)

        # First, start the pros
        if not loaded_smashgg and not self.testing:
            # Start 1 thread for melee and 1 thread for wiiu
            LOG.info('dallas: about to start pros')
            urls = constants.PRO_MELEE
            LOG.info('dallas: about to start pros with these urls {}'.format(urls))
            t = Thread(target=self.analyze_smashgg, args=(urls, 'pro',))
            t.daemon = True
            t.start()
            threads.append(t)

            # Now wiiu
            urls = constants.PRO_WIIU
            LOG.info('dallas: about to start pros with these urls {}'.format(urls))
            t = Thread(target=self.analyze_smashgg, args=(urls, 'pro_wiiu',))
            t.daemon = True
            t.start()
            threads.append(t)

        else:
            LOG.info('dallas: skipping pros because it has been done')

        for t in threads:
            #LOG.info('dallas: abouto call join for the analysis thread  {}'.format(scene.get_name()))
            t.join()
            #LOG.info('dallas: joining for the analysis thread  {}'.format(scene.get_name()))
        
        # If this was the first time we ran, mark pro brackets as complete
        if not loaded_smashgg and not self.testing:
            # After all the matches from this scene have been processed, calculate ranks
            #self.data_processor.process_ranks('pro')
            loaded_smashgg = True
            self.data_processor.process_ranks(name)

    def analyze_smashgg(self, urls, name):
        for url in urls:
            # Before we process this URL, check to see if we already have
            sql = "SELECT * FROM analyzed where base_url='{}'".format(url)
            res = self.db.exec(sql)
            if len(res) == 0:
                LOG.info('dallas: About to process pro bracket {}'.format(url))
                self.data_processor.process(url, name)
            else:
                LOG.info("Skpping pro bracket because it has already been analyzed: {}".format(url))
        

    def analyze_scene(self, scene):
        # This scene will have several base URLs
        base_urls = scene.get_base_urls()
        name = scene.get_name()
        for base_url in base_urls:
            
            # attempt to load this data from the database
            LOG.info('dallas about to start this analysis thread for scene {}'.format(scene.get_name()))
            sql = "SELECT first,last FROM valids WHERE base_url = '" + str(base_url) + "';"
            result = self.db.exec(sql)
            has_results = len(result) > 0 

            # Did we find a match in the database?
            if has_results:
                LOG.info("validURLs found values in the database" + str(result))
                first = result[0][0]
                last = result[0][1]

                # Check for a new valid URL
                new_last = bracket_utils._get_last_valid_url(base_url, last-1)

                if not new_last == last:
                    if new_last - last > 5:
                        with open("DEBUGOUTPUT.txt", 'a') as f:
                            f.write("[validURLs.py:55]: found a SHIT TON of new tournaments for bracket: {}".format(base_url))

                    else:
                        bracket = base_url.replace('###', str(new_last))
                        msg = "Found new bracket: {}".format(bracket)
                        tweet(msg)

                    # If there's been a new last, update the database
                    sql = "UPDATE valids SET last=" + str(new_last) + " where base_url = '"+str(base_url)+"';"
                    self.db.exec(sql)


                    # Analyze each of these new brackets
                    for i in range(last+1, new_last+1):
                        # Since this URL is new, we have to process the data
                        bracket = base_url.replace('###', str(i))
                        self.data_processor.process(bracket, name)

                    self.data_processor.process_ranks(name)

            else:
                # We need to create first and last from scratch
                first = bracket_utils._get_first_valid_url(base_url)
                last = bracket_utils._get_last_valid_url(base_url, first)

                # This is new data, we need to put it into the db
                sql = "INSERT INTO valids (base_url, first, last, scene) VALUES ("
                sql += "'"+str(base_url)+"', "+str(first)+ ", "+str(last)+", '"+str(name)+"');"
                self.db.exec(sql)

                for i in range(first, last+1):
                    bracket = base_url.replace('###', str(i))
                    self.data_processor.process(bracket, name)

                self.data_processor.process_ranks(name)
                

    # TODO remove this whole function
    #def run_loop(self):
    #    global loaded_smashgg

    #    # TODO temporary - have we loaded smashgg brackets?
    #    name = "pro"
    #    if not loaded_smashgg and not self.testing:
    #        for b in constants.PRO_URLS:
    #            # Before we process this URL, check to see if we already have
    #            sql = "SELECT * FROM analyzed where base_url='{}'".format(b)
    #            res = self.db.exec(sql)
    #            if len(res) == 0:
    #                self.data_processor.process(b, name)
    #            else:
    #                LOG.info("Skpping pro bracket because it has already been analyzed: {}".format(b))
    #        
    #        # After all the matches from this scene have been processed, calculate ranks
    #        #self.data_processor.process_ranks('pro')
    #        loaded_smashgg = True

    #        self.data_processor.process_ranks(name)

    #    # Now that we have all the scenes we want to analyze,
    #    # continuously check for new brackets
    #    for scene in self.scenes:

    #        # This scene will have several base URLs
    #        base_urls = scene.get_base_urls()
    #        name = scene.get_name()
    #        for base_url in base_urls:
    #            
    #            # attempt to load this data from the database
    #            sql = "SELECT first,last FROM valids WHERE base_url = '" + str(base_url) + "';"
    #            result = self.db.exec(sql)
    #            has_results = len(result) > 0 

    #            # Did we find a match in the database?
    #            if has_results:
    #                LOG.info("validURLs found values in the database" + str(result))
    #                first = result[0][0]
    #                last = result[0][1]

    #                # Check for a new valid URL
    #                new_last = bracket_utils._get_last_valid_url(base_url, last-1)

    #                if not new_last == last:
    #                    if new_last - last > 5:
    #                        with open("DEBUGOUTPUT.txt", 'a') as f:
    #                            f.write("[validURLs.py:55]: found a SHIT TON of new tournaments for bracket: {}".format(base_url))

    #                    else:
    #                        bracket = base_url.replace('###', str(new_last))
    #                        msg = "Found new bracket: {}".format(bracket)
    #                        tweet(msg)

    #                    # If there's been a new last, update the database
    #                    sql = "UPDATE valids SET last=" + str(new_last) + " where base_url = '"+str(base_url)+"';"
    #                    self.db.exec(sql)


    #                    # Analyze each of these new brackets
    #                    for i in range(last+1, new_last+1):
    #                        # Since this URL is new, we have to process the data
    #                        bracket = base_url.replace('###', str(i))
    #                        self.data_processor.process(bracket, name)

    #                    self.data_processor.process_ranks(name)

    #            else:
    #                # We need to create first and last from scratch
    #                first = bracket_utils._get_first_valid_url(base_url)
    #                last = bracket_utils._get_last_valid_url(base_url, first)

    #                # This is new data, we need to put it into the db
    #                sql = "INSERT INTO valids (base_url, first, last, scene) VALUES ("
    #                sql += "'"+str(base_url)+"', "+str(first)+ ", "+str(last)+", '"+str(name)+"');"
    #                self.db.exec(sql)

    #                for i in range(first, last+1):
    #                    bracket = base_url.replace('###', str(i))
    #                    self.data_processor.process(bracket, name)

    #                self.data_processor.process_ranks(name)
    #                
