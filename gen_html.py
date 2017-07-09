from manual_get_results import get_win_loss_data

def get_header():
    header = "<!DOCTYPE html>\n<html>\n\t<body>\n"
    header = header + '\t<link rel="stylesheet" href="https://unpkg.com/purecss@1.0.0/build/pure-min.css" integrity="sha384-nn4HPE8lTHyVtfCBi5yW9d20FjT8BJwUXyWZT9InLYax14RDjBj46LmSztkmNP9w" crossorigin="anonymous">\n'
    return header

def get_table(data):
    table = ''
    #Start generating the table HTML
    table = table + '\t<table class="pure-table" style="width:30%" align="center">\n'


    for key in data:
        wins, losses = get_wins_losses(key, data)
        table = table + '\t\t<thead>\n'
        table = table + '\t\t\t<tr>\n'
        table = table + '\t\t\t\t<th>' + str(key) + ' ' + str(wins) + '-' + str(losses) + '</th>\n'
        table = table + '\t\t\t</tr>\n'
        table = table + '\t\t</thead>\n'

        match_data = data[key]
        for opponent, results in match_data.items():
            table = table + '\t\t<tbody>\n'
            table = table + '\t\t\t<tr>\n'
            table = table + '\t\t\t\t<td>' + str(opponent) + '\t' +  str(results) + '</td>\n'
            table = table + '\t\t\t</tr>\n'
            table = table + '\t\t</tbody>\n'

    table = table + '\t</table>\n'

    return table

def get_footer():
    footer = "\t</body>\n</html>\n"
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
