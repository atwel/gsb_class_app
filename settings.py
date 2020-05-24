from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

"""
    dict(
            name='BioPharm_Seltek',
            display_name="BioPharm Seltek",
            num_demo_participants=2,
            app_sequence=['BiopharmSeltek']),
    dict(
        name='New_Recruit',
        display_name="New Recruit",
        num_demo_participants=2,
        app_sequence=['NewRecruit']),
    dict(
        name='Sugar_Bowl_Section1',
        display_name="Sugar Bowl Section 1",
        num_demo_participants=2,
        app_sequence=['SugarBowl_Section1']),
    dict(
        name='Sugar_Bowl_Section_2',
        display_name="Sugar Bowl Section 2",
        num_demo_participants=2,
        app_sequence=['SugarBowl_Section2']),
    dict(
        name='Federated_Science',
        display_name="Federated Science",
        num_demo_participants=3,
        app_sequence=['Federated']),
    dict(
        name='HarborCo_section1',
        display_name="Harbor Co section 1",
        num_demo_participants=6,
        app_sequence=['HarborCo_section1']),
    dict(
            name='HarborCo_section2',
            display_name="Harbor Co section 2",
            num_demo_participants=6,
            app_sequence=['HarborCo_section2']),
    dict(
        name='HarborCo_vote1',
        display_name="Section 1 voting",
        num_demo_participants=6,
        app_sequence=['HarborCo_vote1']),
        dict(
            name='HarborCo_vote2',
            display_name="Section 2 voting",
            num_demo_participants=6,
            app_sequence=['HarborCo_vote2'])
"""


SESSION_CONFIGS = [
    dict(
        name='OmniChannel',
        display_name="OmniChannel",
        num_demo_participants=2,
        app_sequence=['OmniChannel']),

]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

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


DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""
ADMIN_USERNAME = "atwell"
ADMIN_PASSWORD = "aaaa"
# don't share this with anybody.
SECRET_KEY = 'z$k1!j!#nzwc#1af2%x9$^vde#u*(mf$wbdrmsw4f=$u2@jo!e'

INSTALLED_APPS = ['otree']
