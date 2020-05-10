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

with open("_rooms/Sp20_1.txt", "r") as f:
    raw_string = f.read()
    names_section1 = raw_string.replace("\n", ",")

with open("_rooms/Sp20_2.txt", "r") as f:
    raw_string = f.read()
    names_section2 = raw_string.replace("\n", ",")

SUNet_to_name = {'cumminsm':"Matt C","jomohu":"Joshua H","extra_01":"Unknown","extra_02":"Unknown","extra_03":"Unknown","extra_04":"Unknown","extra_05":"Unknown","extra_06":"Unknown",'andreaar': 'Andrea A. R.','kha915': 'Khaled A','rbadlani': 'Rohan B','nellb': 'Nell B','cryer': 'Andrew C','brian644': 'Brian E','jfagan2': 'John F','mkgold': 'Melanie G','mwhabib': 'Marc H','alfredoh': 'Alfredo H','jenn7790': 'Jenn K','casimira': 'Casi K','lkyaw3': 'Lin K','jlopata2': 'Jen L','smacq': 'Spencer M','hmaha': 'Harry M','ymeier': 'Yannick M','jmorcos': 'Joseph M','bhn': 'Bader N','stoneng': 'Stone N','judypark': 'Judy P','apinelli': 'Andrew P','prash20': 'Prashanth P','broch': 'Brett R','dsabada': 'Deepak S','pstiefel': 'Philip S','cszmutko': 'Carl S','dvas': 'David V','joewalt': 'Joseph W','linghanz': 'Michael Z','mxzoller': 'Maximilian Z','dejiabe': 'Deji A','zaxayon7': 'Ankit B','demeng': 'Demeng C','kc7': 'Kyle C','yuriydov': 'Yuriy D','mariaeg': 'Maria E','mgants': 'Michael G','tgerhart': 'Toby G','steveng3': 'Steven G','lawanson': 'Ruth L','zuber': 'Zuber M','jmilch': 'Julia M','ninimoor': 'Nini M','ianp12': 'Ian P','mgreeves': 'Mary-Grace R','lrengifo': 'Luis R','sagastuy': 'Maitane S','asayall': 'Alysha S','susa': 'Susannah S','yanivs': 'Yaniv S','csmurro': 'Clio S','rossv': 'Ross V','tinayyu': 'Tina Y','azehfuss': 'Anja Z',"atwell":"Tommy A","ermeehan":"Erica M","rossv":"Ross V","kaoutar": "Kaoutar Y"}


class Constants(BaseConstants):
    name_in_url = 'New_Recruit'
    players_per_group = 2
    num_rounds = 1

    reading_time = 5 #minutes
    material_button_show= .02 #minutes
    material_button_show_no_timer= .02 #minutes
    calculator_time = 5 #minutes
    planning_doc_time= 5 # minutes
    negotiating_time = 25 # minutes

    planning_doc_length = 150 #words

    link_581_1 = "https://stanford.zoom.us/j/98453129717"
    link_581_2 = "https://stanford.zoom.us/j/93410198117"
    section_1_participants = names_section1
    section_2_participants = names_section2
    SUNet_to_name = SUNet_to_name

    salary = { 90000:(-6000,0), 88000:(-4500,-1500), 86000:(-3000,-3000), 84000:(-1500,-4500), 82000:(0,-6000)}
    bonus = { 10:(0,4000), 8:(400,3000), 6:(800,2000), 4:(1200,1000), 2:(1600,0)}
    vacation_time = { 25:(0,1600), 20:(1000,1200), 15:(2000,800), 10:(3000,400), 5:(4000,0)}
    moving_expenses = {100:(0,3200), 90:(200,2400), 80:(400,1600), 70:(600,800), 60:(800,0)}
    location = {"San Francisco":(1200,1200), "Atlanta":(900,900), "Chicago":(600,600),"Boston":(300,300),  "New York":(0,0)}
    insurance_coverage = {"Plan A":(0,800), "Plan B":(800,600), "Plan C":(1600,400), "Plan D":(2400,200), "Plan E":(3200,0)}
    starting_date = {"June 1":(0,2400), "June 15":(600,1800),"July 1":(1200,1200), "July 15":(1800,600), "August 1":(2400,0)}
    job_assignment = {"Division A":(0,0), "Division B":(-600,-600), "Division C":(-1200,-1200), "Division D":(-1800,-1800), "Division E":(-2400,-2400)}


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    salary = models.IntegerField()
    bonus = models.IntegerField()
    moving_expenses = models.IntegerField()
    vacation_time = models.IntegerField()
    job_assignment = models.StringField()
    location = models.StringField()
    insurance_coverage = models.StringField()
    starting_date = models.StringField()

    salary_fract = models.FloatField()
    bonus_fract = models.FloatField()
    job_assignment_fract = models.FloatField()
    location_fract =models.FloatField()
    insurance_coverage_fract = models.FloatField()
    vacation_time_fract = models.FloatField()
    starting_date_fract = models.FloatField()
    moving_expenses_fract = models.FloatField()


class Player(BasePlayer):
    salary = models.IntegerField()
    bonus = models.IntegerField()
    moving_expenses = models.IntegerField()
    vacation_time = models.IntegerField()
    job_assignment = models.StringField()
    location = models.StringField()
    insurance_coverage = models.StringField()
    starting_date = models.StringField()

    planning_text = models.LongStringField(label="Describe your plan for this negotiation")
    journaling_text = models.LongStringField(label="Please describe your experience of the negotiation.")
    initial_offer_points = models.IntegerField()
    final_points = models.IntegerField()



    def role(self):
        if self.id_in_group == 1:
            return 'candidate'
        else:
            return 'recruiter'
