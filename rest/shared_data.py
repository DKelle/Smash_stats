import threading

lock = threading.Lock()

url_range = {}
win_loss_data = {}
dated_win_loss = {}

def set_url_range_data(new_range):
    global url_range

    # Lock the shared data, and update it
    with lock:
        print('shared data has updated range: ' + str(new_range))
        url_range = new_range
