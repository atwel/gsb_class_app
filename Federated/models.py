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
Negotatiing Federated Sciences with two partners
"""

SUNet_to_name = {'cumminsm':"Matt C","jomohu":"Joshua H","extra_01":"Unknown","extra_02":"Unknown","extra_03":"Unknown","extra_04":"Unknown","extra_05":"Unknown","extra_06":"Unknown",'andreaar': 'Andrea A. R.','kha915': 'Khaled A','rbadlani': 'Rohan B','nellb': 'Nell B','cryer': 'Andrew C','brian644': 'Brian E','jfagan2': 'John F','mkgold': 'Melanie G','mwhabib': 'Marc H','alfredoh': 'Alfredo H','jenn7790': 'Jenn K','casimira': 'Casi K','lkyaw3': 'Lin K','jlopata2': 'Jen L','smacq': 'Spencer M','hmaha': 'Harry M','ymeier': 'Yannick M','jmorcos': 'Joseph M','bhn': 'Bader N','stoneng': 'Stone N','judypark': 'Judy P','apinelli': 'Andrew P','prash20': 'Prashanth P','broch': 'Brett R','dsabada': 'Deepak S','pstiefel': 'Philip S','cszmutko': 'Carl S','dvas': 'David V','joewalt': 'Joseph W','linghanz': 'Michael Z','mxzoller': 'Maximilian Z','dejiabe': 'Deji A','zaxayon7': 'Ankit B','demeng': 'Demeng C','kc7': 'Kyle C','yuriydov': 'Yuriy D','mariaeg': 'Maria E','mgants': 'Michael G','tgerhart': 'Toby G','steveng3': 'Steven G','lawanson': 'Ruth L','zuber': 'Zuber M','jmilch': 'Julia M','ninimoor': 'Nini M','ianp12': 'Ian P','mgreeves': 'Mary-Grace R','lrengifo': 'Luis R','sagastuy': 'Maitane S','asayall': 'Alysha S','susa': 'Susannah S','yanivs': 'Yaniv S','csmurro': 'Clio S','rossv': 'Ross V','tinayyu': 'Tina Y','azehfuss': 'Anja Z',"atwell":"Tommy A","ermeehan":"Erica M","rossv":"Ross V","kaoutar": "Kaoutar Y"}


class Constants(BaseConstants):
    name_in_url = 'Federated_Sciences'
    players_per_group = 3
    num_rounds = 1

    reading_time = 5 #minutes
    material_button_show= 2 #minutes
    planning_doc_time = 8 # minutes
    negotiating_time = 30 # minutes
    reflection_time  = 5 # minutes

    planning_doc_length = 150 #words


class Subsession(BaseSubsession):

    def creating_session(self):
        import itertools
        stock = itertools.cycle([True, False])
        for g in self.get_groups():
            g.stockman = next(stock)




class Group(BaseGroup):
    stockman = models.BooleanField()
    pairing = models.StringField()
    start_time = models.StringField()

    def set_start_time(self):
        import datetime
        self.start_time = datetime.datetime.now().strftime("%H:%M:%S")

    def set_first_meet(self):
        for i, p in enumerate(self.get_players()):
            try:
                p.name = SUNet_to_name[p.participant_label]
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

    planning_text = models.LongStringField(label="Describe your plan for this negotiation. In particular, how do intend to approach dealing with coalitions?")

    united = models.IntegerField()
    turbo = models.IntegerField()
    stockman= models.IntegerField()

    journaling_text = models.LongStringField(label="Please describe your experience of the negotiation.")


    def role(self):
        if self.id_in_group == 1:
            return 'stockman'
        elif self.id_in_group == 2:
            return 'turbo'
        else:
            return 'united'
