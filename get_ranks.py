from manual_get_results import get_win_loss_data
import numpy
import pickle
from bracket_utils import dump_pickle_data, load_pickle_data

debug = False

class PlayerNode(object):
    def __init__(self, tag):
        self.tag = tag

def zeros(n):
    z = [0 for i in range(n)]
    zs = []
    for i in range(n):
        zs.append(z)
    return zs

def get_tags_to_index(win_loss_data):
    tags_to_index = []
    for tag in win_loss_data.keys():
        tags_to_index.append(tag)
    return tags_to_index

def create_transition_mat(win_loss_data, tags_to_index):
    num_players = len(tags_to_index)

    # Start a transition matrix, and fill it with zeros
    transition_mat = zeros(num_players)
    for i in range(num_players):
        row_sum = 0
        for j in range(num_players):
            if i == j:
                continue
            player_1 = tags_to_index[i]
            player_2 = tags_to_index[j]
            win_loss = win_loss_data[player_1]
            # Have these two players played each other?
            if player_2 in win_loss.keys():
                wins = win_loss[player_2][0]
                losses = win_loss[player_2][1]
            else:
                # If these players haven't played, assume that they both
                # have a 50% chance of winning
                wins = 1
                losses = 1
            total_matches = wins + losses

            value = (wins/(total_matches))/(num_players-1)
            transition_mat[i][j] = value
            row_sum += value

            transition_mat[i][i] = 1 - row_sum
            if 'christmas' in player_1 and debug:
                print('mike vs ' + str(player_2))
                print('wins, losses', wins, losses)
                print(transition_mat[i])
    return transition_mat

def get_eigen_vector(transition_mat):
    # Get eigen values and vectors
    vals, vectors = numpy.linalg.eig(transition_mat)

    # Find the index of eigen value 1
    i = index_of(vals, 1)
    vector = vectors[i]
    return vector

def index_of(vals, find):
    # (may not be /exactly/ one. Could be 1.000001)
    for i in range(len(vals)):
        val = vals[i]
        diff = abs(find-val)
        if diff < .001:
            if debug: print('found the index of ' + str(vals[i]))
            return i
    if debug: print("Could not find an eigen vector!")

def print_results(ranks):
    players = len(ranks)
    for i, x in enumerate(ranks):
        print(str(i) + '/' + str(players) + ' - ' + str(x))

def main():
    URLS = ['http://challonge.com/RAA_###']
    win_loss_data = get_win_loss_data(URLS)
    #win_loss_data = load_pickle_data('temp')

    # Create a map of tags to an ID (index of the tag)
    tags_to_index = get_tags_to_index(win_loss_data)

    # Make a transition matrix that shows the probability
    # of each player beating any other given player
    transition_mat = create_transition_mat(win_loss_data, tags_to_index)

    # If we get the eigen vector, we can treat each players
    # value as a rank
    # eg, if Christmas Mike is index 5 in tags_to_index
    # Then eigen_vector[5] will be Christmas Mike's rank
    ranks = get_eigen_vector(transition_mat)

    ranks_and_tags = list(zip(ranks, tags_to_index))
    sorted_ranks = sorted(ranks_and_tags)
    print_results(sorted_ranks)


if __name__ == "__main__":
    main()
