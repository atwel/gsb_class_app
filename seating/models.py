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


class Constants(BaseConstants):
    name_in_url = 'seating'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    claim_it = models.BooleanField(label="You got a seat!")
    waiting = models.BooleanField(label="Would you like to add yourself to the waitlist?")
    declined  = models.BooleanField(default=False)
