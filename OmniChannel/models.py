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
    name_in_url = 'OmniChannel'
    players_per_group = 2
    num_rounds = 1
    reflection_time  = 5 # minutes
    coordinating_time = 20

    planning_doc_length = 150 #words


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass



class Player(BasePlayer):
    name = models.StringField()

    agreement = models.StringField(label="Did the parties reach an agreement on all 9 issues? If not, you'll skip inputting the agreement.",choices=["Yes","No"])

    data = models.StringField(label="Use of Manipulated Data", choices=["3DTV has a perpetual license to use the data for internal research.","3DTV has a license to use that for internal research during the agreement term.","3DTV cannot use manipulated data for internal research."])
    license_restrictions = models.StringField(label="Data License Restriction",choices=["3DTV can offer the content to their subscribers in 2D or 3D format.","3DTV can offer the content to their subscribers in 3D format only."])
    premium_count = models.IntegerField(label="# of Premium channels licensed",choices=[0,5,10,15,20])
    premium_fees = models.IntegerField(label="Fees for PremiumTV ($/month)", choices=[11000,12000,13000,14000,15000])
    regular_count = models.IntegerField(label="# of OC channels licensed",choices=[60,70,80,90,100])
    regular_fees = models.IntegerField(label="Fees for OC channels ($/month)", choices=[600,700,800,900,1000])
    data_center_fees = models.IntegerField(label="Fees for using 3DTV's data centers ($/month)", choices=[30000,25000,20000,15000,10000])
    length = models.IntegerField(label="Length of Agreement", choices=[8,7,6,5,4])
    termination = models.IntegerField(label="Termination Options (months notice required)", choices=[12,9,6,3,1])

    planning_text = models.LongStringField(label="Describe your plan for this negotiation. In particular, how do intend to approach dealing with team members")

    journaling_text = models.LongStringField(label="Please describe your experience of the negotiation.")


    def role(self):
        try:
            self.name = SUNet_to_name[self.participant.label]
            #self.participant.label = SUNet_to_name[self.participant.label]
        except:
            pass
        if self.id_in_group == 1:
            return '3dtv'
        elif self.id_in_group == 2:
            return 'omni'
        elif self.id_in_group == 3:
            return '3dtv'
        elif self.id_in_group == 4:
            return 'omni'
        elif self.id_in_group == 5:
            return '3dtv'
        else:
            return 'omni'
