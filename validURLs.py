from database_writer import get_db
from process_data import processData
from threading import Thread
import logger
import bracket_utils
import constants
import time
from tweet import tweet

analyzed_scenes = False

LOG = logger.logger(__name__)

class validURLs(object):
    def __init__(self, scenes, testing=False):
        self.testing = testing
        self.scenes = scenes
        db_name = 'smash_test' if testing else 'smash'
        self.db = get_db(db=db_name)

        # Create a processor to analyze new matches
        self.data_processor = processData(self.db) 
        LOG.info("validURL being created")


    def init(self):
        if not self.testing:
            while True:
                LOG.info('About to create analyziz threads')
                self.create_analysis_threads()
                LOG.info('just finished with analysis threads')
                time.sleep(constants.SLEEP_TIME)
                LOG.info('Just finished sleeping')

        # If we are testing, we only want to run once, and then check our state
        else:
            self.create_analysis_threads()

    def create_analysis_threads(self):
        global analyzed_scenes
        # Create one thread to analyze each scene
        threads = []

        num_threads = 3
        length = len(self.scenes)
        for i in range(num_threads):
            i1 = int((length/num_threads)*i)
            i2 = int((length/num_threads)*(i+1))
            chunk = self.scenes[i1:i2]
            name = [scene.get_name() for scene in chunk]
            t = Thread(target=self.analyze_scenes, name=str(name), args=(chunk,))
            LOG.info('Trying to start the analysis thread for scenes {}'.format(t.name))
            t.start()
            threads.append(t)

        # Start the pros
        # Have we analyzed them before?
        sql = "SELECT * FROM players WHERE scene='pro';"
        res = self.db.exec(sql)
        if len(res) == 0 and not self.testing:
            # Start 1 thread for melee and 1 thread for wiiu
            LOG.info('about to start pros')
            urls = constants.PRO_MELEE
            t = Thread(target=self.analyze_smashgg, name='pro', args=(urls, 'pro',))
            t.daemon = True
            t.start()
            threads.append(t)

            # Now wiiu
            urls = constants.PRO_WIIU
            t = Thread(target=self.analyze_smashgg, name='pro_wiiu', args=(urls, 'pro_wiiu',))
            t.daemon = True
            t.start()
            threads.append(t)

        else:
            LOG.info('Skipping pros because it has been done')

        for t in threads:
            LOG.info('abouto call join for the analysis thread  {}'.format(t.name))
            t.join()
            LOG.info('joining for the analysis thread  {}'.format(t.name))

        # If this is the first time that we have gone through all the scenes, tweet me
        if not analyzed_scenes:
            analyzed_scenes = True
            LOG.info('Just finished analyzing scenes for the first time. About to tweet')
            tweet('Done loading scene data')
        
        # If this was the first time we ran, mark pro brackets as complete
        # TODO temporarily dont calculate pro ranks... to memory intensive. Fix this
        sql = "SELECT * FROM ranks WHERE scene='pro';"
        res = self.db.exec(sql)
        if len(res) == 0 and not self.testing and False:
            LOG.info('dallas: make pro ranks')
            # After all the matches from this scene have been processed, calculate ranks
            self.data_processor.process_ranks('pro')
            self.data_processor.process_ranks('pro_wiiu')

    def analyze_smashgg(self, urls, name):
        for url in urls:
            # Before we process this URL, check to see if we already have
            sql = "SELECT * FROM analyzed where base_url='{}'".format(url)
            res = self.db.exec(sql)
            if len(res) == 0:

                display_name = bracket_utils.get_display_base(url)
                LOG.info('About to process pro bracket {}'.format(url))
                self.data_processor.process(url, name, display_name)
            else:
                LOG.info("Skpping pro bracket because it has already been analyzed: {}".format(url))
        
    def analyze_scenes(self, chunk):
        # We've been given a chunk of scenes to analyze
        # So do

        for scene in chunk:
            self.analyze_scene(scene)

    def analyze_scene(self, scene):
        # This scene will have several base URLs
        base_urls = scene.get_base_urls()
        name = scene.get_name()
        for base_url in base_urls:
            
            # attempt to load this data from the database
            LOG.info('About to start this analysis thread for scene {}'.format(scene.get_name()))
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
                        LOG.info('Found new bracket: {}'.format(bracket))
                        msg = "Found new bracket: {}".format(bracket)
                        tweet(msg)

                    # If there's been a new last, update the database
                    sql = "UPDATE valids SET last=" + str(new_last) + " where base_url = '"+str(base_url)+"';"
                    self.db.exec(sql)


                    # Analyze each of these new brackets
                    for i in range(last+1, new_last+1):
                        # Since this URL is new, we have to process the data
                        bracket = base_url.replace('###', str(i))
                        # Create the display name for this bracket
                        # Eg challonge.com/NP9ATX54 -> NP9 54
                        display_base = bracket_utils.get_display_base(bracket)
                        display_name = '{} {}'.format(display_base, i)
                        self.data_processor.process(bracket, name, display_name)

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
                    # Create the display name for this bracket
                    # Eg challonge.com/NP9ATX54 -> NP9 54
                    display_base = bracket_utils.get_display_base(bracket)
                    display_name = '{} {}'.format(display_base, i)
                    self.data_processor.process(bracket, name, display_name)

                self.data_processor.process_ranks(name)
