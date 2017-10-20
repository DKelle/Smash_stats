from bracket_utils import get_urls_with_player, get_tournament_placings
import sys

def main(tag):
    # Get all the urls that this player has participated in
    player_urls = get_urls_with_player(tag)
    player_placings = []

    # Get the html from the 'standings' of this tournament
    for url in player_urls:
        tournament_placings = get_tournament_placings(url)
        player_placing = tournament_placings[tag.lower()] if tag.lower() in tournament_placings else None
        if player_placing:
            player_placings.append((url, player_placing))

    for url, placing in sorted(player_placings, key=lambda x : x[-1]):
        print(url, placing)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        tag = sys.argv[1]
    else:
        tag = 'Christmas Mike'
    main(tag)
