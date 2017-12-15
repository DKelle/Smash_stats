import bracket_utils
import sys
import time
import constants

def get_header():
    header = "<!DOCTYPE html>\n<html>\n\t<body>\n"
    header = header + '\t<link rel="stylesheet" type="text/css" href="smashco.css">\n'

    return header

def get_table(data, singles = False):

    btn = '\t\t<div id="left">\n'
    players = list(data.keys())
    sorted_data = sorted(players)

    singles_data = [x for x in sorted_data if '+' not in x]
    doubles_data = [x for x in sorted_data if '+' in x]

    cur_data = singles_data if singles else doubles_data
    legend = 'Singles' if singles else 'Doubles'

    #Add a button as a legen so the user knows what the data means
    btn += '\t\t\t<button class="legend">'+str(legend)+'<br>Tag W - L</button>\n'
    for i, key in enumerate(cur_data):

        if i == len(cur_data)//2:
            btn += '\t\t</div>\n'
            btn += '\t\t<div id="right">\n'

        wins, losses = get_wins_losses(key, data)
        btn += '\t\t\t<button class="accordion">'+ str(key) + ' ' + str(wins) + '-' + str(losses) +'</button>\n'
        btn += '\t\t\t<div class="panel">\n'

        btn += '\t\t\t\t<table>\n'
        btn += '\t\t\t\t\t<tr>\n'
        btn += '\t\t\t\t\t\t<th>Opponent</th>\n'
        btn += '\t\t\t\t\t\t<th>Wins</th>\n'
        btn += '\t\t\t\t\t\t<th>Losses</th>\n'
        btn += '\t\t\t\t\t</tr>\n'

        match_data = data[key]

        for opponent, results in match_data.items():
            btn += '\t\t\t\t\t<tr>\n'
            btn += '\t\t\t\t\t\t<td>'+ str(opponent) +'</td>\n'
            btn += '\t\t\t\t\t\t<td>'+ str(results[0]) +'</td>\n'
            btn += '\t\t\t\t\t\t<td>'+ str(results[-1]) +'</td>\n'
            btn += '\t\t\t\t\t</tr>\n'


        btn += '\t\t\t\t</table>\n'
        btn += '\t\t\t</div>\n'


    btn += '\t\t</div>\n'

    return btn

def get_footer():
    footer = '\t<script src="smashco.js"></script>\n'
    footer = footer + "\t</body>\n</html>\n"
    return footer

def get_wins_losses(player, data):
    wins = 0
    losses = 0
    opponents = data[player]
    for opp, result in opponents.items():
        wins += result[0]
        losses += result[-1]

    return wins, losses

def init():
    scenes = bracket_utils.get_list_of_named_scenes()

    #get the actual data about these URLs
    scene_data = shared_data.get_win_loss_data()
    print('starting html thread')

    while True:
        for scene in scenes:
            name = scene[0]
            base_urls = scene[1]

            if name in scene_data:
                data = scene_data[name]

                #Now turn all this data into HTML that can be displayed in browser
                html_header = get_header()
                html_table_singles = get_table(data, True)
                html_table_doubles = get_table(data, False)
                html_footer = get_footer()

                #Combine all the aspects of the page to create a final HTML file
                html = html_header + html_table_singles + html_table_doubles + html_footer

                # Create the actual HTML page
                fname = 'lib/' + str(scene[0]) + '.html'
                with open(fname, 'w+') as f:
                    f.write(html)

                shared_data.set_html(name, html)

        time.sleep(constants.SLEEP_TIME)
