from requests import get
import time
from tweet import tweet

limited = False
while True:
    msg = ''
    r = get('https://challonge.com/1g06dgsf')
    if r.status_code > 300:
        if 'too many' in r.reason.lower():
            msg = "Yep, you're being rate limited"

            # We we go from !limited -> limited? text
            if not limited:
                tweet(msg)
            limited = True
        else:
            msg = "No, but are getting back a {} because {}".format(r.status_code, r.reason)
    else:
        msg = "We are back up. Getting a  {}".format(r.status_code)

        # We we go from limited -> !limited? text
        if not limited:
            tweet(msg)

    # Check every 1.5 hours
    TIMEOUT = 60 * 90
    time.sleep(TIMEOUT)
