from otree.api import *


author = 'Jon Atwell'
doc = """
Negotatiing New Recruit with a partner
"""


class C(BaseConstants):
    SALARY = {
        90000: (-6000, 0),
        88000: (-4500, -1500),
        86000: (-3000, -3000),
        84000: (-1500, -4500),
        82000: (0, -6000),
    }
    BONUS = {10: (0, 4000), 8: (400, 3000), 6: (800, 2000), 4: (1200, 1000), 2: (1600, 0)}
    VACATION_TIME = {
        25: (0, 1600),
        20: (1000, 1200),
        15: (2000, 800),
        10: (3000, 400),
        5: (4000, 0),
    }
    MOVING_EXPENSES = {
        100: (0, 3200),
        90: (200, 2400),
        80: (400, 1600),
        70: (600, 800),
        60: (800, 0),
    }
    LOCATION = {
        "San Francisco": (1200, 1200),
        "Atlanta": (900, 900),
        "Chicago": (600, 600),
        "Boston": (300, 300),
        "New York": (0, 0),
    }
    INSURANCE_COVERAGE = {
        "Plan A": (0, 800),
        "Plan B": (800, 600),
        "Plan C": (1600, 400),
        "Plan D": (2400, 200),
        "Plan E": (3200, 0),
    }
    STARTING_DATE = {
        "June 1": (0, 2400),
        "June 15": (600, 1800),
        "July 1": (1200, 1200),
        "July 15": (1800, 600),
        "August 1": (2400, 0),
    }
    JOB_ASSIGNMENT = {
        "Division A": (0, 0),
        "Division B": (-600, -600),
        "Division C": (-1200, -1200),
        "Division D": (-1800, -1800),
        "Division E": (-2400, -2400),
    }
    NAME_IN_URL = 'calculator'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    CALCULATOR_TIME = 5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    salary = models.IntegerField()
    bonus = models.IntegerField()
    moving_expenses = models.IntegerField()
    vacation_time = models.IntegerField()
    job_assignment = models.StringField()
    location = models.StringField()
    insurance_coverage = models.StringField()
    starting_date = models.StringField()
    salary_pareto = models.IntegerField()
    bonus_pareto = models.IntegerField()
    moving_expenses_pareto = models.IntegerField()
    vacation_time_pareto = models.IntegerField()
    job_assignment_pareto = models.StringField()
    location_pareto = models.StringField()
    insurance_coverage_pareto = models.StringField()
    starting_date_pareto = models.StringField()
    salary_pair = models.StringField()
    bonus_pair = models.StringField()
    moving_expenses_pair = models.StringField()
    vacation_time_pair = models.StringField()
    job_assignment_pair = models.StringField()
    location_pair = models.StringField()
    insurance_coverage_pair = models.StringField()
    starting_date_pair = models.StringField()
    optimal_points = models.IntegerField()


# FUNCTIONS
# PAGES
class Candidate_calculator(Page):
    form_model = "player"
    form_fields = [
        'bonus',
        'job_assignment',
        'location',
        'insurance_coverage',
        'vacation_time',
        'moving_expenses',
        "salary",
        'starting_date',
    ]
    timeout_seconds = C.CALCULATOR_TIME * 60
    timer_text = "Time left before you'll need to move to the next page: "


class Recruiter_calculator(Page):
    form_model = "player"
    form_fields = [
        'bonus',
        'job_assignment',
        'location',
        'insurance_coverage',
        'vacation_time',
        'moving_expenses',
        "salary",
        'starting_date',
    ]
    timeout_seconds = C.CALCULATOR_TIME * 60
    timer_text = "Time left before you'll need to move to the next page: "


class Explore_calc(Page):
    form_model = "player"




page_sequence = [Candidate_calculator, Recruiter_calculator, Explore_calc]
