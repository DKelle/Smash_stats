from bracket_utils import get_urls_with_players, get_tournament_placings
import sys

def main(tags):
    # Get all the urls that this player has participated in
    player_urls = get_urls_with_players(tags)
    player_placings = []

    # Get the html from the 'standings' of this tournament
    for url in player_urls:
        tournament_placings = get_tournament_placings(url)

        found_placing = False
        for tag in tags:
            player_placing = tournament_placings[tag.lower()] if tag.lower() in tournament_placings else None
            if player_placing:
                found_placing = True
                player_placings.append((url, player_placing))
        if not found_placing:
            print('cant determine placing in bracket ' + url)

    for url, placing in sorted(player_placings, key=lambda x : x[-1]):
        print(url, placing)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        tags = sys.argv[1:]
    else:
        tags = ['Christmas Mike']
    main(tags)
