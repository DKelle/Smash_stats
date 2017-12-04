TAGS_TO_COALESCE = [['christmas mike', 'thanksgiving mike'],
	['megafox', 'su | megafox'],
	['hakii', 'su l hakii', 'su | hakii', 'su redriot i hakii', 'hih | hakii', 'su | sleepyhakii', 'su|hakii', 'su | hakii $', 'su  redriot i hakii', 'hoh | hakii', 'su| hakii'],
	['lucy', 'ttn | lucy'],
	['sassy', 'atx | sassy'],
	['crump', 'donald crump', 'captain crump', 'abc | crump'],
	['dragonite', 'su dragonite', 'su | dragonite', 'tpwn | dragonite', 'tpwn | dragonite_pr', 'tpwn| dragonite (gnw)', 'atx hoh | dragonite', 'dragonite_pr', 'hoh | dragonite', 'mega dragonite', 'tpwn|dragonite'],
	['gallium', 's.e.s punk'],
	['mt', 'mt_'],
	['fx | albert', 'albert'],
	['ul | jf', 'jf', 'ul| jf', 'ul i jf'],
	['take a \_', 'take a seat', 'take a \\_'],
	['bobby big ballz', 'bobby big balls'],
	['prof. cube', 'prof cube', 'professor cube', 'profesor cube', 'cube', 'processorcube', 'prof cube $'],
	['cashoo', 'hoh | cashoo', 'hoh l cashoo'],
	['ul | chandy', 'ul| chandy', 'cnb | chandy', 'chandy'],
	['spankey', 'spanky'],
	['xlll', 'xiii']]


AUSTIN_URLS = ['https://challonge.com/NP9ATX###', 'https://austinsmash4.challonge.com/atx###', 'http://challonge.com/heatwave###']
AUSTIN_MELEE_URLS = ['http://challonge.com/tipperoni###am', 'http://challonge.com/tipperoni###', 'http://challonge.com/longhornweekly###', 'http://challonge.com/apollosingles###', 'http://challonge.com/smashedhalffull###', 'http://gamerzgalaxy.challonge.com/TTT###', 'http://challonge.com/Magesmf###', 'http://challonge.com/varsity###am', 'http://challonge.com/varsity###']
SMASHBREWS_RULS = ['https://challonge.com/Smashbrews###']
COLORADO_SINGLES_URLS = ['http://smashco.challonge.com/CSUWW###WUS', 'http://smascho.challonge.com/FCWUA###', 'http://smascho.challonge.com/FCWUIB###']
COLORADO_DOUBLES_URLS = ['http://smashco.challonge.com/CSUWW###WUD', 'http://smashco.challonge.com/FCWUDC###']
COLORADO_URLS = COLORADO_SINGLES_URLS + COLORADO_DOUBLES_URLS
SMS_URLS = ['http://challonge.com/RAA_###']

"""
Data structure we need -
dictionary where key is tag_1:
    value is dictionary:
        key for inner dictionary is tag_2, value is a list
        the list has (date_of_set, result)
        one (date, result) for every set they have played
"""
