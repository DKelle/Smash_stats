from manual_get_results import get_win_loss_data

def get_header():
    header = "<!DOCTYPE html>\n<html>\n\t<body>\n"
    header = header + '\t<link rel="stylesheet" type="text/css" href="smashco.css">\n'
    header = header + '\t\t<div id="left"></div>\n'
    header = header + '\t\t<div id="center">\n'


    return header

def get_table(data):

    btn = ''
    players = list(data.keys())
    sorted_data = sorted(players)
    sorted_data

    #Add a button as a legen so the user knows what the data means
    btn += '\t\t\t<button class="legend">tag W - L</button>\n'
    for key in sorted_data:
        wins, losses = get_wins_losses(key, data)
        btn += '\t\t\t<button class="accordion">'+ str(key) + ' ' + str(wins) + '-' + str(losses) +'</button>\n'
        btn += '\t\t\t<div class="panel">\n'

        match_data = data[key]
        btn += '\t\t\t\t<p class="legend">Opponent (W-L)</p>\n'
        for opponent, results in match_data.items():
            btn += '\t\t\t\t<p text-align="center">'+ str(opponent) + '\t' +  str(results) +'</p>\n'

        btn += '\t\t\t</div>\n'

    btn += '\t\t</div>\n'
    return btn

def get_footer():
    footer = '\t\t<div id="right"></div>\n'
    footer = footer + '\t<script src="smashco.js"></script>\n'
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

if __name__ == "__main__":
    data = get_win_loss_data(pages=25)

    html_header = get_header()

    html_table = get_table(data)

    html_footer = get_footer()

    html = html_header + html_table + html_footer

    print(html)
