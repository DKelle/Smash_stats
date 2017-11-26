from manual_get_results import get_win_loss_data, get_dated_data
import numpy
import pickle
import constants
import pprint
import datetime
from bracket_utils import dump_pickle_data, load_pickle_data, get_urls_with_players

debug = False

TEST_DATA = {
    "A": {
        "B": (1, 0),
        "C": (1, 0),
        "D": (1, 0),
    },
    "B": {
        "A": (0, 1),
        "C": (1, 0),
        "D": (1, 0),
    },
    "C": {
        "A": (0, 1),
        "B": (0, 1),
        "D": (1, 0),
    },
    "D": {
        "A": (0, 1),
        "B": (0, 1),
        "C": (0, 1),
    },
}

epsilon = 1

# The greater this number, the more significant recent matches will be
exponent = 1.3

class PlayerNode(object):
    def __init__(self, tag):
        self.tag = tag

def zeros(n):
    z = [0 for i in range(n)]
    zs = []
    for i in range(n):
        zs.append(z[:])
    return zs[:]

def get_tags_to_index(win_loss_data):
    tags_to_index = []
    for tag in win_loss_data.keys():
        tags_to_index.append(tag)
    return tags_to_index

def get_win_loss_score(win_loss, tag, tag2):
    # Get a list of the matches these twp have played against each other
    matches = win_loss[tag]
    win_total = 0
    loss_total = 0

    for match in matches:
        print('match is ' + str(match))
        win = (not match[1])
        date = match[0]
        score = date_to_points(date)
        if win:
            win_total += score
        else:
            loss_total += score


    return win_total, loss_total

def date_to_points(date):
    today = datetime.datetime.today()
    current_date = datetime.datetime(today.year, today.month, today.day)
    date = datetime.datetime.strptime(date,'%Y-%m-%d')
    delta = float((today - date).days)
    delta = max(200, delta)
    delta = 200 - delta
    score = delta ** exponent
    return score


def create_transition_mat(win_loss_data, tags_to_index):
    num_players = len(tags_to_index)
    total_matches_played = get_total_matches_played(win_loss_data)
    print('win loss data is ' + str(win_loss_data))

    # Start a transition matrix, and fill it with zeros
    transition_mat = zeros(num_players)
    if debug:
        print("this should be zeros")
        pprint.pprint(transition_mat)

    for i in range(num_players):
        row_sum = 0
        player_1 = tags_to_index[i]
        for j in range(num_players):
            if i == j:
                continue
            player_2 = tags_to_index[j]
            win_loss = win_loss_data[player_1]
            # Have these two players played each other?
            if player_2 in win_loss.keys():
                #wins = win_loss[player_2][0]
                #losses = win_loss[player_2][1]
                wins, losses = get_win_loss_score(win_loss, player_2, player_1)
            else:
                # If these players haven't played, assume that their chance
                # of winning is thier own win/loss ratio
                wins = get_win_loss_ratio(player_1, win_loss_data)
                losses = get_win_loss_ratio(player_2, win_loss_data)

            total_matches = wins + losses
            total_matches_p2 = get_total_played(player_2, win_loss_data)
            chance_of_playing = total_matches_p2/(total_matches_played)
            if debug:
                print('the total chance of these two playing is ', player_1, player_2, str(chance_of_playing))
            #win_loss_ratio = ((losses+epsilon)/(total_matches+epsilon))/(num_players-1)
            win_loss_ratio = ((losses+epsilon)/(total_matches+epsilon))*(chance_of_playing)
            value = win_loss_ratio

            if debug:
                print('analyze ' + player_1 + ' against ' + player_2)
                print('wins is X, losses is X, value is X', wins, losses, value)
            transition_mat[i][j] = value
            row_sum += value

        transition_mat[i][i] = 1 - row_sum
        if 'christmas' in player_1 and debug:
            print('mike vs ' + str(player_2))
            print('wins, losses', wins, losses)
            print(transition_mat[i])
    return transition_mat

def get_total_played(tag, win_loss_data):
    total = 0
    if tag in win_loss_data:
        win_loss = win_loss_data[tag]
        for opponent in win_loss.keys():
            # Add the wins and losses against each opponent
            # to get a total number of matches played by 'tag'
            total += len(win_loss[opponent])

    if debug:
        print('the total number of matches played by ' + str(tag) + ' is ' + str(total))
    return total

def get_win_loss_ratio(player, win_loss_dict):
    data = win_loss_dict[player]
    wins = get_wins(player, win_loss_dict)
    losses = get_losses(player, win_loss_dict)
    return (wins+epsilon)/(losses+epsilon)

def get_wins(player, win_loss_dict):
    data = win_loss_dict[player]
    wins = 0
    for key in data.keys():
        for match in data[key]:
            if match[1]:
                wins += 1
    return wins

def get_losses(player, win_loss_dict):
    data = win_loss_dict[player]
    losses = 0
    for key in data.keys():
        for match in data[key]:
            if not match[1]:
                losses += 1
    return losses

def get_eigen_vector(transition_mat):
    # Get eigen values and vectors
    num_players = len(transition_mat[0])
    vals, vectors = numpy.linalg.eig(transition_mat)

    if debug:
        print('Eigen values are ')
        pprint.pprint(vals)
        print('Eigen vectors are ')
        pprint.pprint(vectors)

    # Find the index of eigen value 1
    i = index_of(vals, 1)
    vector = vectors[i]

    s = [0] * num_players
    s[0] = 1
    s = numpy.array(s)
    mat = numpy.array(transition_mat)
    for i in range(1000):
        s = s.dot(mat)
        if debug:
            print("found eigen vector manually")
            pprint.pprint(s)

    return s

def l2(vec1, vec2):
    return sum(x**2 for x in vec1 - vec2)

def random_walk(trans_mat, threshold=0.0000000000000001):
    num_players = trans_mat.shape[0]
    cur_state = numpy.array([1./num_players] * num_players)
    prev_state = numpy.array([0] * num_players)
    diff = l2(cur_state, prev_state)
    while diff > threshold:
        prev_state = cur_state
        cur_state = cur_state.dot(trans_mat)
        diff = l2(cur_state, prev_state)
        if debug: print(diff)
    return cur_state

def index_of(vals, find):
    # (may not be /exactly/ one. Could be 1.000001)
    for i in range(len(vals)):
        val = vals[i]
        diff = abs(find-val)
        if diff < .001:
            if debug: print('found the index of ' + str(vals[i]) + ' and the index is ' + str(i))
            return i
    if debug: print("Could not find an eigen vector!")

def print_results(ranks, player_urls=None):
    basic = False
    players = len(ranks)
    PR_map = {}

    if player_urls:
        # Create a map of tags to PR, if any
        PR = 1
        best_players = reversed([x[-1] for i, x in enumerate(ranks)])
        print(best_players)
        for tag in best_players:
            if tag in player_urls and len(player_urls[tag]) > 2:
              PR_map[tag] = PR
              print('adding ' + str(tag) + ' to the PR at ' + str(PR))
              PR = PR + 1

    # Before we print rankgs, calculate PRs
    # PR is like a rank, but you only qualify to be
    # PRd if you have played at least 3 tournaments
    for i, x in enumerate(ranks):
        # this is going to be slow
        tag = x[1]
        if basic:
            print(str(players-i) + '/' + str(players) + ' - ' + str(x[-1]))
        elif tag in PR_map:
            PR = PR_map[tag]
            print(str(players-i) + '/' + str(players) + ' - ' + str(x) + ' - PR ' + str(PR))
        else:
            print(str(players-i) + '/' + str(players) + ' - ' + str(x))

def get_total_matches_played(win_loss_data):
    total = 0
    for key in win_loss_data.keys():
        data = win_loss_data[key]
        for k in data.keys():
            for match in data[k]:
                if match[1]:
                    total += 1

    if debug:
        print('total matches played is ' + str(total))
    return total

def main():
    URLS = constants.SMS_URLS
    #URLS = constants.AUSTIN_URLS
    #URLS = constants.COLORADO_SINGLES_URLS
    #URLS = constants.AUSTIN_MELEE_URLS
    #URLS = constants.SMASHBREWS_RULS
    #win_loss_data, player_urls = get_win_loss_data(URLS, True)
    win_loss_data, player_urls = get_dated_data(URLS, True)
    #win_loss_data = load_pickle_data('practice')
    #win_loss_data = TEST_DATA
    if debug:
        print('win loss data looks like: ')
        pprint.pprint(win_loss_data)

    # Create a map of tags to an ID (index of the tag)
    tags_to_index = get_tags_to_index(win_loss_data)
    if debug:
        print('tags to index looks like')
        pprint.pprint(tags_to_index)

    # Make a transition matrix that shows the probability
    # of each player beating any other given player
    transition_mat = create_transition_mat(win_loss_data, tags_to_index)
    if debug:
        print('transition mat looks like')
        pprint.pprint(transition_mat)


    # If we get the eigen vector, we can treat each players
    # value as a rank
    # eg, if Christmas Mike is index 5 in tags_to_index
    # Then eigen_vector[5] will be Christmas Mike's rank
    ranks = random_walk(numpy.array(transition_mat))
    if debug:
        print('ranking values are ')
        pprint.pprint(ranks)

    if debug:
        print('ranks times transition mat is')
        a = numpy.array(transition_mat)
        b = numpy.array(ranks)
        pprint.pprint(a.dot(b))
    ranks_and_tags = list(zip(ranks, tags_to_index))
    sorted_ranks = sorted(ranks_and_tags)
    if debug:
        print_results(sorted_ranks)
    else:
        print_results(sorted_ranks, player_urls)


if __name__ == "__main__":
    main()
