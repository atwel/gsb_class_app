from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

"""dict(name="Seating",
        display_name="Seating allocation",
        num_demo_participants=1,
        app_sequence=["seating"],
        section_number=1,
        section_seats = 23,
        start_index=0),"""

SESSION_CONFIGS = [


dict(
        name='BioPharm_Seltek',
        display_name="BioPharm Seltek",
        num_demo_participants=2,
        section_number=1,
        app_sequence=['BiopharmSeltek']),
dict(
        name='Recruit_calc',
        display_name="New Recruit calculator",
        num_demo_participants=1,
        section_number=1,
        app_sequence=["calculator"]),
dict(
        name='newRecruit',
        display_name="New Recruit",
        num_demo_participants=2,
        section_number=1,
        app_sequence=["NewRecruit"]),
dict(
        name='NoCode',
        display_name="NoCode, Inc",
        num_demo_participants=2,
        section_number=1,
        app_sequence=['NoCode']),
dict(
        name='Federated_Science',
        display_name="Federated Science",
        num_demo_participants=3,
        section_number=1,
        app_sequence=['Federated']),
dict(
        name='Bissap_Bops',
        display_name="Bissap Bops",
        num_demo_participants=2,
        section_number=1,
        app_sequence=['BissapBops']),
dict(
        name='OmniChannel',
        display_name="OmniChannel",
        num_demo_participants=6,
        section_number=1,
        app_sequence=['OmniChannel']),
dict(
        name='HarborCo',
        display_name="Harbor Co",
        num_demo_participants=6,
        section_number=1,
        app_sequence=['HarborCo']),
dict(
        name='HarborCo_vote',
        display_name="HarborCo voting",
        num_demo_participants=6,
        section_number=1,
        app_sequence=['HarborCo_vote',"just_journal"])
]


LANGUAGE_CODE = 'en'

REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ROOMS = [
    dict(
        name='OB581_01',
        display_name='OB581.01, Sp23',
        participant_label_file = "_rooms/Sp23_01.txt",
    ),
    dict(
        name='OB581_02',
        display_name='OB581.02, Sp23',
        participant_label_file = "_rooms/Sp23_02.txt",
    ),
    dict(
        name='OB581_03',
        display_name='OB581.03, Sp23',
        participant_label_file = "_rooms/Sp23_03.txt",
    ),
        dict(
            name='OB581_01_alt',
            display_name='OB581.01alt, Sp23',
            participant_label_file = "_rooms/Sp23_03.txt",
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
