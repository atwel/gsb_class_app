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
Negotating OmniChannel with two teams
"""


class Constants(BaseConstants):
    name_in_url = 'OmniChannel'
    players_per_group = 2
    num_rounds = 1
    reading_time = 10
    planning_doc_time  = 10 # minutes
    coordinating_time = 20
    negotiating_time = 60
    planning_doc_length = 100 #words


class Subsession(BaseSubsession):

    def vars_for_admin_report(self):
        omni = []
        DTV = []

        for p in self.get_players():
            if p.role() == "3dtv":
                DTV.append(p.name)
            else:
                omni.append(p.name)

        return {"DTV_ip":DTV, "Omni_ip":omni}

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
    length = models.IntegerField(label="Length of Agreement (years)", choices=[8,7,6,5,4])
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
