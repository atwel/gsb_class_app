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
import random


author = 'Jon Atwell'

doc = """
Voting platform for HarborCo
"""

SUNet_to_name = {'cumminsm':"Matt C","jomohu":"Joshua H","extra_01":"Unknown","extra_02":"Unknown","extra_03":"Unknown","extra_04":"Unknown","extra_05":"Unknown","extra_06":"Unknown",'andreaar': 'Andrea A. R.','kha915': 'Khaled A','rbadlani': 'Rohan B','nellb': 'Nell B','cryer': 'Andrew C','brian644': 'Brian E','jfagan2': 'John F','mkgold': 'Melanie G','mwhabib': 'Marc H','alfredoh': 'Alfredo H','jenn7790': 'Jenn K','casimira': 'Casi K','lkyaw3': 'Lin K','jlopata2': 'Jen L','smacq': 'Spencer M','hmaha': 'Harry M','ymeier': 'Yannick M','jmorcos': 'Joseph M','bhn': 'Bader N','stoneng': 'Stone N','judypark': 'Judy P','apinelli': 'Andrew P','prash20': 'Prashanth P','broch': 'Brett R','dsabada': 'Deepak S','pstiefel': 'Philip S','cszmutko': 'Carl S','dvas': 'David V','joewalt': 'Joseph W','linghanz': 'Michael Z','mxzoller': 'Maximilian Z','dejiabe': 'Deji A','zaxayon7': 'Ankit B','demeng': 'Demeng C','kc7': 'Kyle C','yuriydov': 'Yuriy D','mariaeg': 'Maria E','mgants': 'Michael G','tgerhart': 'Toby G','steveng3': 'Steven G','lawanson': 'Ruth L','zuber': 'Zuber M','jmilch': 'Julia M','ninimoor': 'Nini M','ianp12': 'Ian P','mgreeves': 'Mary-Grace R','lrengifo': 'Luis R','sagastuy': 'Maitane S','asayall': 'Alysha S','susa': 'Susannah S','yanivs': 'Yaniv S','csmurro': 'Clio S','rossv': 'Ross V','tinayyu': 'Tina Y','azehfuss': 'Anja Z',"atwell":"Tommy A","ermeehan":"Erica M","rossv":"Ross V","kaoutar": "Kaoutar Y"}

with open("_rooms/Sp20_2.txt", "r") as f:
    raw_string = f.read()
    names_section2 = raw_string.replace("\n", ",")

class Constants(BaseConstants):
    name_in_url = 'Voting_section2'
    players_per_group = 6
    num_rounds = 10

    section_2_participants = names_section2.split(",")
    SUNet_to_name = SUNet_to_name



class Subsession(BaseSubsession):
    def creating_session(self):
        names = Constants.section_2_participants.copy()
        for p in self.get_players():
            p.participant.label = names.pop(0)


class Group(BaseGroup):
    mix = models.StringField(label="Industry Mix", choices=["Primarily dirty","Clean & dirty","All clean"],initial="Primarily dirty")
    eco = models.StringField(label="Ecological Impact",choices=["Some harm","Maintain & repair","Improve"], initial="Some harm")
    union = models.StringField(label="Employment Rules",choices=["Unlimited union preference","Union quota 2:1","Union quota 1:1","No union preference"], initial="No union preference")
    loan = models.StringField(label="Federal Loan", choices=["$3 Billion","$2 Billion","$1 Billion","No federal loan"],initial="$3 Billion")
    comp = models.StringField( label = "Compensation to other ports", choices=["HarborCo pays $600 million","HarborCo pays $450 million","HarborCo pays $300 million","HarborCo pays $150 million","HarborCo pays nothing"],initial="HarborCo pays nothing")

    passed = models.BooleanField()
    high_passed = models.BooleanField()
    vetoed = models.BooleanField()
    no_pass = models.BooleanField()
    pairing = models.StringField()

    def set_first_meet(self):
        for i, p in enumerate(self.get_players()):
            try:
                p.name = SUNet_to_name[p.participant.label]
            except:
                p.name = "Demo_{}".format(i)

        for p in self.get_players():
            if p.role() == "stockman":
                stockman = p.name
            elif p.role() == "turbo":
                turbo = p.name
            else:
                united = p.name

        if self.stockman:
            self.pairing = ",".join([united, stockman, turbo])
        else:
            self.pairing = ",".join([united, turbo, stockman])


class Player(BasePlayer):

    name = models.StringField()
    vote = models.StringField(choices=["Yes","No"], label="Would you like to vote in favor of this proposal?", initial="No")

    def role(self):
        if self.id_in_group == 1:
            return 'union'
        elif self.id_in_group == 2:
            return 'enviro'
        elif self.id_in_group == 3:
            return 'ports'
        elif self.id_in_group == 4:
            return 'dcr'
        elif self.id_in_group == 5:
            return 'harborco'
        else:
            return 'gov'
