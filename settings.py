from os import environ
import random
SESSION_CONFIGS = [
    dict(
        name='introquest', 
        app_sequence=['introquest'], 
        num_demo_participants=1, 
    ),
    dict(
        name='jeudede', 
        app_sequence=['jeudede'], 
        num_demo_participants=1, 
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']
bot_labels=[]
for i in range(24): bot_labels.append("bot%d"%(i+1))

# bot_labels=["AMS", "ATH", "BER", "BRU", "BUD", "DUB", "HEL", "LIS", "LON", "MAD", "MOS", "OSL", "PRA", "RIG", "ROM", "SOF", "VAR", "VIE", "VIL", "ZUR", "LAB", "BOX1", "BOX2", "BOX3", "BOX4", "BOX5", "BOX6", "BOX7", "BOX8"]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1, participation_fee=3.00, doc="", test_mode=False, bot_labels=bot_labels #+["LIS","BUD","VAR","MAD","BRU","BOX1","BOX3","BOX7"]
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'fr'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True

ROOMS = [
    {
        'name': 'LEEP',
        'display_name': 'Laboratoire d’Economie Expérimentale de Paris',
        'participant_label_file': '_rooms/LEEP.txt',
    },
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]
ADMIN_USERNAME = 'experimentateur'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5354502079362'
