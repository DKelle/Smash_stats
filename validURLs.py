from database_writer import DatabaseWriter
from process_data import processData
import logger
import bracket_utils
import constants
import time

LOG = logger.logger(__name__)

class validURLs(object):
    def __init__(self, scenes):
        self.scenes = scenes
        self.db = DatabaseWriter()

        # Create a processor to analyze new matches
        self.data_processor = processData() 
        print("validURL being created")


    def init(self):
        print('valid urls has been started')

        # Now that we have all the scenes we want to analyze,
        # continuously check for new brackets
        while True:
            for scene in self.scenes:

                # This scene will have several base URLs
                base_urls = scene.get_base_urls()
                name = scene.get_name()
                for base_url in base_urls:
                    prior_entries = False
                    
                    # attempt to load this data from the database
                    sql = "SELECT first,last FROM valids WHERE base_url = '" + str(base_url) + "';"
                    result = self.db.exec(sql)
                    has_results = len(result) > 0 
                    print("HAS RESULTS? " + str(has_results))

                    # Did we find a match in the database?
                    if has_results:
                        print("validURLs found values in the database" + str(result))
                        first = result[0][0]
                        last = result[0][1]

                        # Check for a new valid URL
                        new_last = bracket_utils._get_last_valid_url(base_url, last)

                        if not new_last == last:
                            # If there's been a new last, update the database
                            sql = "UPDATE valids SET last=" + str(new_last) + " where base_url = '"+str(base_url)+"';"
                            self.db.exec(sql)

                            # Since this URL is new, we have to process the data
                            bracket = base_url.replace('###', str(last))
                            self.data_processor.process(bracket)


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
                            self.data_processor.process(bracket)
                        

            time.sleep(constants.SLEEP_TIME)
