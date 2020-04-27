from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)



author = 'Jon Atwell'

doc = """
Negotatiing New Recruit with a partner
"""


class Constants(BaseConstants):
    name_in_url = 'New_Recruit_bots'
    players_per_group = 2
    num_rounds = 1
    salary = {86000:(-3000,-3000), 82000:(0,-6000), 88000:(-4500,-1500), 90000:(-6000,0), 84000:(-1500,-4500)}
    location = {"New York":(0,0), "Atlanta":(900,900), "Chicago":(600,600),"Boston":(300,300),  "San Francisco":(1200,1200)}
    insurance_coverage = {"Plan A":(0,800), "Plan B":(800,600), "Plan C":(1600,400), "Plan D":(2400,200), "Plan E":(3200,0)}
    moving_expenses = {"100%":(0,3200),"70%":(600,800), "90%":(200,2400),"80%":(400,1600),"60%":(800,0)}
    starting_date = {"June 1":(0,2400), "June 15":(600,1800),"July 1":(1200,1200), "July 15":(1800,600), "August 1":(2400,0)}
    vacation_time = {10:(3000,400), 5:(4000,0), 20:(1000,1200), 15:(2000,800),  25:(0,1600)}
    job_assignment = {"Division A":(0,0), "Division B":(-600,-600), "Division C":(-1200,-1200), "Division D":(-1800,-1800), "Division E":(-2400,-2400)}
    bonus = { "2%":(1600,0), "8%":(400,3000), "4%":(1200,1000), "10%":(0,4000),  "6%":(800,2000)}
    reading_time = 6
    planning_doc_length = 150


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    link = models.StringField(initial="https://stanford.zoom.us/j/4340648848",label="Stanford Zoom URL")
    salary = models.CurrencyField(choices=list(Constants.salary.keys()),widget=widgets.RadioSelectHorizontal, label="Salary in USD")
    bonus = models.StringField(choices=list(Constants.bonus.keys()), widget=widgets.RadioSelectHorizontal, label="Annual Bonus as percentage of salary")
    job_assignment = models.StringField(choices=list(Constants.job_assignment.keys()),widget=widgets.RadioSelectHorizontal, label="Job is within:")
    location = models.StringField(choices=list(Constants.location.keys()), widget=widgets.RadioSelectHorizontal)
    insurance_coverage = models.StringField(choices=list(Constants.insurance_coverage.keys()),widget=widgets.RadioSelectHorizontal)
    vacation_time = models.IntegerField(choices=list(Constants.vacation_time.keys()),widget=widgets.RadioSelectHorizontal, label="Vacation time in days")
    starting_date = models.StringField(choices=list(Constants.starting_date.keys()),widget=widgets.RadioSelectHorizontal)
    moving_expenses = models.StringField(choices=list(Constants.moving_expenses.keys()),widget=widgets.RadioSelectHorizontal, label="Percentage of moving expenses covered")

    salary_fract = models.FloatField()
    bonus_fract = models.FloatField()
    job_assignment_fract = models.FloatField()
    location_fract =models.FloatField()
    insurance_coverage_fract = models.FloatField()
    vacation_time_fract = models.FloatField()
    starting_date_fract = models.FloatField()
    moving_expenses_fract = models.FloatField()


class Player(BasePlayer):
    salary = models.CurrencyField(choices=list(Constants.salary.keys()),widget=widgets.RadioSelectHorizontal, label="Salary in USD")
    bonus = models.StringField(choices=list(Constants.bonus.keys()), widget=widgets.RadioSelectHorizontal, label="Annual Bonus as percentage of salary")
    job_assignment = models.StringField(choices=list(Constants.job_assignment.keys()),widget=widgets.RadioSelectHorizontal, label="Job is within:")
    location = models.StringField(choices=list(Constants.location.keys()), widget=widgets.RadioSelectHorizontal)
    insurance_coverage = models.StringField(choices=list(Constants.insurance_coverage.keys()),widget=widgets.RadioSelectHorizontal)
    vacation_time = models.IntegerField(choices=list(Constants.vacation_time.keys()),widget=widgets.RadioSelectHorizontal, label="Vacation time in days")
    starting_date = models.StringField(choices=list(Constants.starting_date.keys()),widget=widgets.RadioSelectHorizontal)
    moving_expenses = models.StringField(choices=list(Constants.moving_expenses.keys()),widget=widgets.RadioSelectHorizontal, label="Percentage of moving expenses covered")
    planning_text = models.LongStringField(label="Describe your plan for this negotiation")
    total_points = models.IntegerField(initial=100)
    low_score = models.BooleanField(initial=False)
