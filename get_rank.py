from manual_get_results import get_win_loss_data
from pprint import pprint
import numpy

def pad_data(win_loss_data):
    #For each player A that did not play player B, add an entry to both, where the total score is (0,0)

    #First get a list of all players
    all_players = list(win_loss_data.keys())

    #Sort the list. This will be the order of our 2d matrix
    sorted_players = sorted(all_players)

    #Go through our data, and create all the new entries
    for player, results in win_loss_data.items():
        didnt_play = [p for p in all_players if p not in results]

        #Add everyone that player didnt_play to players results
        for p in didnt_play:
            win_loss_data[player][p] = (0,0)

    weights = []
    #Create a 2d matrix of weights
    for i, p1 in enumerate(sorted_players):
        weights.append([])
        for j, p2 in enumerate(sorted_players):
            weights[i].append(win_loss_data[p1][p2][0])

    #Now that we have an array of weights, normalize it
    normal_weights = normalize(weights)
    print(normal_weights)


def normalize(weights):
    #Iterate through each col

    col_total = 0
    normal = []

    for i,x in enumerate(weights):
        row_total = sum(weights[i])
        new_row = [(x+0.0)/(row_total+0.0) if row_total > 0 else 0 for x in weights[i] ]
        print('changing ' + str(weights[i]) + ' to ' + str(new_row))
        weights[i] = new_row

if __name__ == "__main__":
    #get the win loss data
    win_loss_data = get_win_loss_data(pages=1)

    #Pad the data so we have a square matrix
    win_loss_data = pad_data(win_loss_data)

