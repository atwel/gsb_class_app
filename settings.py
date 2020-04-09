from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)


SESSION_CONFIGS = [
    dict(
        name='New_Recruit',
        display_name="New Recruit",
        num_demo_participants=2,
        app_sequence=['NewRecruit'],
    )]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='OB581_1',
        display_name='OB581.1, Sp20 ',
        participant_label_file = "_rooms/Sp20_1.txt",
    ),
    dict(
        name='OB581_2',
        display_name='OB581.2, Sp20 ',
        participant_label_file = "_rooms/Sp20_2.txt",
    )
]
OTREE_AUTH_LEVEL = "STUDY"
ADMIN_USERNAME = 'atwell'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = "aaaa"#environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""

# don't share this with anybody.
SECRET_KEY = 'z$k1!j!#nzwc#1af2%x9$^vde#u*(mf$wbdrmsw4f=$u2@jo!e'

INSTALLED_APPS = ['otree']
