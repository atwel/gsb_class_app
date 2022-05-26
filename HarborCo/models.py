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
Negotating HarborCo
"""




class Constants(BaseConstants):
    name_in_url = 'HarborCo'
    players_per_group = 6
    num_rounds = 1
    reading_time = 400
    negotiating_time = 100 # minutes
    reflection_time  = 5 # minutes

    planning_doc_length = 100 #words
    planning_doc_time = 40


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    name = models.StringField()
    planning_text = models.LongStringField(label="Describe your plan for this negotiation. In particular, how do intend to approach dealing with coalitions?")
    journaling_text = models.LongStringField(label="Please describe your experience of the negotiation.")


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
            return 'gov'
        else:
            return 'harborco'
