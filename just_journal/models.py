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
Figuring out who the participant is and if they can negotiate in person
"""

class Constants(BaseConstants):
    name_in_url = 'just_journal'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    journaling_text = models.LongStringField(label="Please describe your experience of the negotiation.")
