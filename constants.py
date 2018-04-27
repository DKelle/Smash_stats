DNS = 'ec2-18-216-108-45.us-east-2.compute.amazonaws.com'

TAGS_TO_COALESCE = [['christmasmike', 'thanksgiving mike', 'christmas mike', 'christmas mike xmas', 'christmas mike late', 'halloween mike'],
        ['im 12', 'im12'],
        ['circuits', 'circuits', 'jkelle'],
        ['hnic', 'hnic xmas'],
        ['1111', '11 11', 'vuibol'],
        ['qmantra', 'qmantra xmas'],
	['megafox', 'su | megafox'],
	['hakii', 'su l hakii', 'su | hakii', 'su redriot i hakii', 'hih | hakii', 'su | sleepyhakii', 'su|hakii', 'su | hakii $', 'su  redriot i hakii', 'hoh | hakii', 'su| hakii'],
	['lucy', 'ttn | lucy'],
	['sassy', 'atx | sassy'],
	['crump', 'donald crump', 'captain crump', 'abc | crump'],
	['dragonite', 'su dragonite', 'su | dragonite', 'tpwn | dragonite', 'tpwn | dragonite_pr', 'tpwn| dragonite (gnw)', 'atx hoh | dragonite', 'dragonite_pr', 'hoh | dragonite', 'mega dragonite', 'tpwn|dragonite', 'armada | dragonite', 'aes | dragonite'],
	['gallium', 's.e.s punk', 'ses punk'],
	['mt', 'mt_'],
	['wolf', ' wolf'],
	['fx | albert', 'albert'],
	['ul | jf', 'jf', 'ul| jf', 'ul i jf'],
	['take a seat', 'take a \_', 'take a \\_', 'takeaseat', 'take a seat xmas'],
	['bobby big ballz', 'bobby big balls'],
	['prof. cube', 'type r professor cube', 'prof cube', 'professor cube', 'profesor cube', 'cube', 'processorcube', 'prof cube $'],
	['cashoo', 'hoh | cashoo', 'hoh l cashoo'],
	['ul | chandy', 'ul| chandy', 'cnb | chandy', 'chandy'],
	['spankey', 'spanky'],
	['xlll', 'xiii'],
	['cheesedud6', '←/cheesedud6'],
	['kj', 'go! kj'],
	['jtag', 'tgl | jtag', 'sms | jtag', 'sms jtag', 'jtg'],
	['jka', 'tgl | jka'],
	['fcar', 'tgl | fcar'],
	['resident', 'tgl | resident'],
	['minty!', 'tgl | minty!', 'tgl | minty', 'minty'],
	['willow', 'willowette'],
	['messiah', 'maple'],
	['tenni', 'go! tenni'],
	['kj', 'go! | kj'],
	['cruzin', 'sa  cruzin'],
	['christmasmitch', 'mitchell', 'mitchell slan'],
        ['jibs', 'sfu jibs'],
        ['trane', 'irn trane'],
        ['ninjafish', 'sa  ninjafish'],
        ['mufin', 'sfu mufin'],
        ['jowii', 'jo wii'],
        ['gudlucifer', 'good lucifer', 'goodlucifer', 'gudlucifer wolf'],
        ['ehmon', 'tgl ehmon', 'tgl  ehmon', 'ah ehmon', 'sms ehmon', 'sms | ehmon', 'tgl | ehmon'],
        ['pollo loco', 'pollo'],
        ['doombase', 'retiredbase'],
        ['majinmike', 'majin mike'],
        ['karonite', 'red velvet', 'aos redvelvet', 'redvelvet']]

# TODO DO NOT ADD MORE BRACKETS WITHOUT ADDING A CORRESPONDING DISPLAY NAME!!
AUSTIN_URLS = ('austin', ['http://challonge.com/heatwave###', 'https://challonge.com/NP9ATX###', 'http://challonge.com/hw###', 'https://austinsmash4.challonge.com/atx###', 'https://challonge.com/alibaba###', 'https://austinsmash4.challonge.com/Mothership###', 'https://austinsmash4.challonge.com/atxfiles###', 'https://austinsmash4.challonge.com/ARFI###', 'https://austinsmash4.challonge.com/arcadian###', 'https://austinsmash4.challonge.com/ooples###', 'https://austinsmash4.challonge.com/mbh###', 'https://austinsmash4.challonge.com/sth###'])
SMASHBREWS_RULS = ('smashbrews', ['https://challonge.com/Smashbrews###', 'https://challonge.com/smashbrewsS3W###', 'https://challonge.com/smashbrewsS4W###', 'https://challonge.com/smashbrewsS5W###'])
COLORADO_SINGLES_URLS = ('colorado', ['http://smashco.challonge.com/CSUWW###WUS', 'http://smascho.challonge.com/FCWUA###', 'http://smascho.challonge.com/FCWUIB###'])
COLORADO_DOUBLES_URLS = ('colorado_doubles', ['http://smashco.challonge.com/CSUWW###WUD', 'http://smashco.challonge.com/FCWUDC###'])
COLORADO_URLS = ('colorado_both', COLORADO_SINGLES_URLS + COLORADO_DOUBLES_URLS)
SMS_URLS = ('sms', ['http://challonge.com/RAA_###'])

DISPLAY_MAP = {'heatwave': 'Heatwave',
        'NP9ATX': 'NP9',
        'challonge.com/hw': 'Heatwave',
        'challonge.com/atx': 'Smashpack',
        'alibaba': 'Alibaba',
        'Mothership': 'Mothership',
        'atxfiles': 'ATX Files',
        'ARFI': 'ARFI',
        'arcadian': 'Arcadian',
        'ooples': 'Ooples',
        'challonge.com/mbh': 'Michaels Big House',
        'challonge.com/sth': 'Smash The Halls',
        'smashbrewsS3': 'Smashbrews S3',
        'smashbrewsS4': 'Smashbrews S4',
        'smashbrewsS5': 'Smashbrews S5',
        'Smashbrews': 'Smashbrews',
        'smashco': 'CSU',
        'smascho': 'CSU',
        'RAA': 'Reading At Alkek'}

        
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
        'https://smash.gg/tournament/super-smash-con-2016/events/melee-singles',
        'https://smash.gg/tournament/the-mango/event/melee-singles',
        'https://smash.gg/tournament/genesis-4/event/melee-singles',
        'https://smash.gg/tournament/the-big-house-7/event/melee-singles',
        'https://smash.gg/tournament/esports-arizona-talking-stick-resort-2/event/super-smash-bros-melee-singles',
        'https://smash.gg/tournament/gametyrant-expo-2017/event/super-smash-bros-melee-singles',
        'https://smash.gg/tournament/genesis-5/event/melee-singles',
        'https://smash.gg/tournament/the-holiday-bash-smash-invitational/event/melee-singles',
        'https://smash.gg/tournament/poi-poundaz/event/melee-singles',
        'https://smash.gg/tournament/ugc-smash-open/event/melee-singles',
        'https://smash.gg/tournament/sweet-27-a-super-smash-bros-melee-event/event/melee-singles',
        'https://smash.gg/tournament/the-gang-hosts-a-melee-tournament/event/melee-singles',
        'https://smash.gg/tournament/mountain-of-dreams-2-5/event/melee-singles',
        'https://smash.gg/tournament/syndicate-2017/event/melee-singles-1',
        'https://smash.gg/tournament/tampa-never-sleeps-7/event/melee-singles',
        'https://smash.gg/tournament/chicago-gaming-coalition-no-1/event/melee-singles',
        'https://smash.gg/tournament/ozhadou-nationals-15/event/melee-singles',
        'https://smash.gg/tournament/smash-summit-spring-2017/event/melee-singles-1',
        'https://smash.gg/tournament/taw-tijuana-at-war/event/melee-singles',
        'https://smash.gg/tournament/smash-valley-v-featuring-lucky-abate-swedish-delight-wadi-more/event/melee-singles',
        'https://smash.gg/tournament/super-smash-sundays-55-1/event/melee-singles',
        'https://smash.gg/tournament/noods-noods-noods-oakland-edition-1/event/melee-singles',
        'https://smash.gg/tournament/noods-noods-noods-melee-edition/event/wii-u-singles',
        'https://smash.gg/tournament/tipped-off-12-presented-by-the-lab-gaming-center/event/melee-singles',
        'https://smash.gg/tournament/thunderstruck-v/event/melee-singles',
        'https://smash.gg/tournament/hope-r-300-pot-bonus-ft-seagull-joe-icymist-tension/event/melee-singles',
        'https://smash.gg/tournament/cen-cal-standoff/event/melee-singles',
        'https://smash.gg/tournament/no-fun-allowed/event/melee-singles',
        'https://smash.gg/tournament/respawn-6/event/melee-singles',
        'https://smash.gg/tournament/gatorlan-fall-2017/event/melee-singles',
        'https://smash.gg/tournament/noods-noods-noods-melee-edition/event/melee-singles',
        'https://smash.gg/tournament/full-bloom-4/event/melee-singles',
        'https://smash.gg/tournament/beast-7-1/event/melee-singles',
        'https://smash.gg/tournament/super-bit-wars-6/event/melee-singles',
        'https://smash.gg/tournament/xanadu-end-of-an-era/event/melee-singles',
        'https://smash.gg/tournament/dreamhack-winter-2017/event/melee-singles',
        'https://smash.gg/tournament/rumble-in-the-tundra-7/event/melee-singles',
        'https://smash.gg/tournament/canada-cup-2017/event/melee-singles',
        'https://smash.gg/tournament/overlords-of-orlando-a-florida-monthly-series/event/melee-singles',
        'https://smash.gg/tournament/the-scarlet-classic-iv/event/melee-singles',
        'https://smash.gg/tournament/cencal-standoff-2018-1/event/smash-bros-melee-singles']

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
        'https://smash.gg/tournament/super-smash-con-2016/events/wii-u-singles',
        'https://smash.gg/tournament/ozhadou-nationals-15/event/wii-u-singles',
        'https://smash.gg/tournament/super-bit-wars-6/event/wii-u-singles',
        'https://smash.gg/tournament/ugc-smash-open/event/wii-u-singles',
        'https://smash.gg/tournament/gatorlan-fall-2017/event/wii-u-singles',
        'https://smash.gg/tournament/genesis-4/event/wii-u-singles',
        'https://smash.gg/tournament/the-big-house-7/event/wii-u-singles',
        'https://smash.gg/tournament/beast-7-1/event/wii-u-singles',
        'https://smash.gg/tournament/final-round-20/event/wii-u-singles',
        'https://smash.gg/tournament/smash-valley-v-featuring-lucky-abate-swedish-delight-wadi-more/event/wii-u-singles',
        'https://smash.gg/tournament/no-fun-allowed/event/wii-u-singles',
        'https://smash.gg/tournament/respawn-6/event/wii-u-singles',
        'https://smash.gg/tournament/overlords-of-orlando-a-florida-monthly-series/event/wii-u-singles',
        'https://smash.gg/tournament/cen-cal-standoff/event/wii-u-singles',
        'https://smash.gg/tournament/thunderstruck-v/event/wii-u-singles',
        'https://smash.gg/tournament/noods-noods-noods-melee-edition/event/wii-u-singles',
        'https://smash.gg/tournament/poi-poundaz/event/wii-u-singles',
        'https://smash.gg/tournament/esports-arizona-talking-stick-resort-2/event/super-smash-bros-for-wii-u-singles',
        'https://smash.gg/tournament/kumite-in-tennessee-2018/event/wii-u-singles',
        'https://smash.gg/tournament/syndicate-2017/event/wii-u-singles-1',
        'https://smash.gg/tournament/full-bloom-4/event/wii-u-singles',
        'https://smash.gg/tournament/gametyrant-expo-2017/event/super-smash-bros-for-wii-u-singles',
        'https://smash.gg/tournament/hope-r-300-pot-bonus-ft-seagull-joe-icymist-tension/event/wii-u-singles',
        'https://smash.gg/tournament/canada-cup-2017/event/wiiu-singles',
        'https://smash.gg/tournament/cencal-standoff-2018-1/event/smash-bros-wii-u-singles',
        'https://smash.gg/tournament/taw-tijuana-at-war/event/wii-u-singles',
        'https://smash.gg/tournament/xanadu-end-of-an-era/event/wii-u-singles',
        'https://smash.gg/tournament/tipped-off-12-presented-by-the-lab-gaming-center/event/wii-u-singles',
        'https://smash.gg/tournament/tampa-never-sleeps-7/event/wii-u-singles',
        'https://smash.gg/tournament/noods-noods-noods-oakland-edition-1/event/wii-u-singles',
        'https://smash.gg/tournament/chicago-gaming-coalition-no-1/event/wii-u-singles',
        'https://smash.gg/tournament/genesis-5/event/smash-for-wii-u-singles']

SLEEP_TIME = 10 * 60 * 6 #1 hour
TOURNAMENTS_PER_RANK = 20


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
