from requests import get
import time
from tweet import tweet

limited = False
while True:
    msg = ''
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = get('https://challonge.com/1g06dgsf', headers=headers)
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

    print(msg)

    # Check every 1.5 hours
    TIMEOUT = 60 * 90
    time.sleep(TIMEOUT)
