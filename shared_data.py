import threading
import copy

lock = threading.Lock()

url_range = {}
win_loss_data = {}
dated_win_loss = {}
rank_data = {}
html_data = {}

def set_url_range_data(base_url, first, last):
    global url_range

    # Lock the shared data, and update it
    with lock:
        print('shared is being updated with : ' + str(base_url) + ' ' + str(first) + ' ' + str(last))
        url_range[base_url] = (first, last)

def get_valid_range():
    with lock:
        return copy.deepcopy(url_range)


def set_dated_data(name, dated_data):
    global dated_win_loss
    with lock:
        dated_win_loss[name] = dated_data
        print('shared data is get new dated data for scene  ' + str(name))

def get_dated_data():
    with lock:
        return copy.deepcopy(dated_win_loss)

def set_win_loss_data(name, data):
    global win_loss_data
    with lock:
        win_loss_data[name] = data
        print('shared data is getting new win loss data ' + str(name))

def get_win_loss_data():
    with lock:
        return win_loss_data

def set_rank_data(name, ranks):
    global rank_data
    with lock:
        print('shared data is getting new rank data ' + str(name))
        rank_data[name] = ranks

def get_rank_data():
    with lock:
        return rank_data

def set_html(name, html):
    global html_data
    with lock:
        print('shared data is getting new html data for ' + str(name))
        html_data[name] = html

def get_html():
    with lock:
        return html_data
