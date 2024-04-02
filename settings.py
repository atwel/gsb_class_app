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
        name='OmniChannel',
        display_name="OmniChannel",
        num_demo_participants=6,
        section_number=1,
        app_sequence=['OmniChannel']),
dict(
        name='OmniChannel_outcome',
        display_name="OmniChannel_outcome",
        num_demo_participants=6,
        section_number=1,
        app_sequence=['OmniChannel_agreement']),
dict(
        name='OmniChannel_homeprep',
        display_name="OmniChannel prep",
        num_demo_participants=6,
        section_number=1,
        app_sequence=['OmniChannel_home'])
]

LANGUAGE_CODE = 'en'

REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ROOMS = [
    dict(
        name='233147',
        display_name='Section 1',
        participant_label_file = "_rooms/SP24_01.txt",
    ),
    dict(
        name='233151',
        display_name='Section 2',
        participant_label_file = "_rooms/SP24_02.txt",
    ),
    dict(
            name='233156',
            display_name='Section 3',
            participant_label_file = "_rooms/SP24_03.txt",
        ),
    dict(
            name="OB581",
            display_name="spare"),
    dict(
            name='219472219477',
            display_name='OB581_error',
            participant_label_file = "_rooms/SP24_01.txt",
    )
]


DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""
ADMIN_USERNAME = environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = environ.get('ADMIN_PASSWORD')

# don't share this with anybody.
SECRET_KEY = environ.get('SECRET_KEY')


INSTALLED_APPS = ['otree']
