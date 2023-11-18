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
        name='219472',
        display_name='Section 1',
        participant_label_file = "_rooms/FALL23_01.txt",
    ),
    dict(
        name='219477',
        display_name='Section 2',
        participant_label_file = "_rooms/FALL23_02.txt",
    ),
    dict(
            name='APX',
            display_name='FL_APX',
            participant_label_file = "_rooms/Fillmore_Lawns_apx.txt",
        ),
    dict(
                name='DIL',
                display_name='FL_DIL',
                participant_label_file = "_rooms/Fillmore_Lawns_dil.txt",
            ),
    dict(
                name='FMO',
                display_name='FL_FMO',
                participant_label_file = "_rooms/Fillmore_Lawns_fmo.txt",
            ),
    dict(
                name='GUP',
                display_name='FL_GUP',
                participant_label_file = "_rooms/Fillmore_Lawns_gup.txt",
            ),
    dict(
                name='KAS',
                display_name='FL_KAS',
                participant_label_file = "_rooms/Fillmore_Lawns_kas.txt",
            ),
    dict(
                name='PEX',
                display_name='FL_PEX',
                participant_label_file = "_rooms/Fillmore_Lawns_pex.txt",
            ),
    dict(
                name='QTI',
                display_name='FL_QTI',
                participant_label_file = "_rooms/Fillmore_Lawns_qti.txt",
            ),
    dict(
                name='RAV',
                display_name='FL_RAV',
                participant_label_file = "_rooms/Fillmore_Lawns_rav.txt",
            ),
    dict(
                name='TUK',
                display_name='FL_TUK',
                participant_label_file = "_rooms/Fillmore_Lawns_tuk.txt",
            ),
    dict(   name="OB581", display_name="spare"),
    dict(
            name='219472219477',
            display_name='OB581_error',
            participant_label_file = "_rooms/FALL23_01.txt",
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
