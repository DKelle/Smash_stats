DNS = 'ec2-18-216-108-45.us-east-2.compute.amazonaws.com'

TAGS_TO_COALESCE = [['christmasmike', 'thanksgiving mike', 'christmas mike'],
	['megafox', 'su | megafox'],
	['hakii', 'su l hakii', 'su | hakii', 'su redriot i hakii', 'hih | hakii', 'su | sleepyhakii', 'su|hakii', 'su | hakii $', 'su  redriot i hakii', 'hoh | hakii', 'su| hakii'],
	['lucy', 'ttn | lucy'],
	['sassy', 'atx | sassy'],
	['crump', 'donald crump', 'captain crump', 'abc | crump'],
	['dragonite', 'su dragonite', 'su | dragonite', 'tpwn | dragonite', 'tpwn | dragonite_pr', 'tpwn| dragonite (gnw)', 'atx hoh | dragonite', 'dragonite_pr', 'hoh | dragonite', 'mega dragonite', 'tpwn|dragonite', 'armada | dragonite', 'aes | dragonite'],
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
	['xlll', 'xiii'],
	['cheesedud6', '←/cheesedud6'],
	['kj', 'go! kj'],
	['jtag', 'tgl | jtag', 'sms | jtag', 'sms jtag'],
	['jka', 'tgl | jka'],
	['fcar', 'tgl | fcar'],
	['resident', 'tgl | resident'],
	['minty!', 'tgl | minty!', 'minty'],
	['willow', 'willowette'],
	['messiah', 'maple'],
	['tenni', 'go! tenni'],
	['kj', 'go! | kj'],
        ['red velvet', 'karonite', 'aos redvelvet']]

AUSTIN_URLS = ('austin', ['http://challonge.com/heatwave###', 'https://challonge.com/NP9ATX###', 'http://challonge.com/hw###', 'https://austinsmash4.challonge.com/atx###'])
SMASHBREWS_RULS = ('smashbrews', ['https://challonge.com/Smashbrews###'])
COLORADO_SINGLES_URLS = ('colorado', ['http://smashco.challonge.com/CSUWW###WUS', 'http://smascho.challonge.com/FCWUA###', 'http://smascho.challonge.com/FCWUIB###'])
COLORADO_DOUBLES_URLS = ('colorado_doubles', ['http://smashco.challonge.com/CSUWW###WUD', 'http://smashco.challonge.com/FCWUDC###'])
COLORADO_URLS = ('colorado_both', COLORADO_SINGLES_URLS + COLORADO_DOUBLES_URLS)
SMS_URLS = ('sms', ['http://challonge.com/RAA_###'])

PRO_MELEE = ['https://smash.gg/tournament/smash-summit/events/melee-singles/brackets',
        'https://smash.gg/tournament/super-smash-con-2017/events/melee-singles/brackets/144662',
        'https://smash.gg/tournament/get-on-my-level-2017/events/super-smash-bros-melee-singles',
        'https://smash.gg/tournament/dreamhack-atlanta-2017/events/super-smash-bros-melee',
        'https://smash.gg/tournament/evo-2017/events/super-smash-bros-melee/',
        'https://smash.gg/tournament/smash-n-splash-3/events/melee-singles',
        'https://smash.gg/tournament/royal-flush/events/melee-singles/',
        'https://smash.gg/tournament/dreamhack-austin-2017/events/super-smash-bros-melee',
        'https://smash.gg/tournament/ceo-dreamland/events/melee-singles/',
        'https://smash.gg/tournament/smash-rivalries-by-yahoo-esports/events/melee-singles',
        'https://smash.gg/tournament/full-bloom-3/events/melee-singles/',
        'https://smash.gg/tournament/smash-summit-spring-2017/events/melee-singles-1/',
        'https://smash.gg/tournament/beast-7-1/events/melee-singles',
        'https://smash.gg/tournament/genesis-4/events/melee-singles/',
        'https://smash.gg/tournament/don-t-park-on-the-grass/events/melee-singles/',
        'https://smash.gg/tournament/ugc-smash-open/events/melee-singles',
        'https://smash.gg/tournament/dreamhack-winter-2016/events/melee-singles',
        'https://smash.gg/tournament/smash-summit-3/events/melee-singles',
        'https://smash.gg/tournament/canada-cup-2016/events/melee-singles/brackets/',
        'https://smash.gg/tournament/eclipse-2/events/melee-singles/brackets',
        'https://smash.gg/tournament/the-big-house-6/events/melee-singles',
        'https://smash.gg/tournament/shine-2016-1/events/melee-singles/',
        'https://smash.gg/tournament/super-smash-con-2016/events/melee-singles']

PRO_WIIU = ['https://smash.gg/tournament/super-smash-con-2017/events/wii-u-singles/brackets/144668',
        'https://smash.gg/tournament/get-on-my-level-2017/events/super-smash-bros-for-wii-u-singles',
        'https://smash.gg/tournament/dreamhack-atlanta-2017/events/super-smash-bros-for-wii-u/',
        'https://smash.gg/tournament/evo-2017/events/super-smash-bros-for-wii-u/',
        'https://smash.gg/tournament/smash-n-splash-3/events/wii-u-singles/',
        'https://smash.gg/tournament/royal-flush/events/wii-u-singles',
        'https://smash.gg/tournament/dreamhack-austin-2017/events/super-smash-bros-for-wii-u',
        'https://smash.gg/tournament/ceo-dreamland/events/wii-u-singles',
        'https://smash.gg/tournament/full-bloom-3/events/wii-u-singles/',
        'https://smash.gg/tournament/beast-7-1/events/wii-u-singles/',
        'https://smash.gg/tournament/genesis-4/events/wii-u-singles',
        'https://smash.gg/tournament/don-t-park-on-the-grass/events/wii-u-singles',
        'https://smash.gg/tournament/ugc-smash-open/events/wii-u-singles/',
        'https://smash.gg/tournament/canada-cup-2016/events/wii-u-singles/',
        'https://smash.gg/tournament/eclipse-2/events/wii-u-singles/brackets',
        'https://smash.gg/tournament/the-big-house-6/events/wii-u-singles/',
        'https://smash.gg/tournament/shine-2016-1/events/wii-u-singles',
        'https://smash.gg/tournament/super-smash-con-2016/events/wii-u-singles']

SLEEP_TIME = 5 
TOURNAMENTS_PER_RANK = 75


TEST_URLS = [('test1', ['https://challonge.com/smash_web_test_###']),
        ('test2', ['https://challonge.com/smash_web_scene_two_###'])]

"""
Data structure we need -
dictionary where key is tag_1:
    value is dictionary:
        key for inner dictionary is tag_2, value is a list
        the list has (date_of_set, result)
        one (date, result) for every set they have played
"""
