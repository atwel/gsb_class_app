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
import datetime
import itertools

author = 'Jon Atwell'

doc = """
Negotiating Federated Sciences with two partners
"""


class Constants(BaseConstants):
    name_in_url = 'Federated_Sciences'
    players_per_group = 3
    num_rounds = 1

    reading_time = 10 #minutes
    material_button_show= 2 #minutes
    planning_doc_time = 10
    negotiating_time = 30 # minutes
    reflection_time  = 5 # minutes

    planning_doc_length = 100 #words


class Subsession(BaseSubsession):

    def creating_session(self):
        stock = itertools.cycle([True, False])
        for g in self.get_groups():
            g.stockman = next(stock)

    def vars_for_admin_report(self):
        stockman = []
        united = []
        turbo = []

        for p in self.get_players():
            the_label = p.participant.vars["name"]
            if p.role() == "stockman":
                stockman.append(the_label)
            elif p.role() == "turbo":
                turbo.append(the_label)
            else:
                united.append(the_label)


        return {"Stockman":stockman,"Turbo":turbo,"United":united}

class Group(BaseGroup):
    stockman = models.BooleanField()
    pairing = models.StringField()
    end_time = models.StringField()
    started = models.BooleanField(initial=False)

    def set_end_time(self):
        self.end_time = (datetime.datetime.now() + datetime.timedelta(minutes=Constants.negotiating_time + 1)).strftime("%H:%M:%S")
        self.started = True

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

    #planning_text = models.LongStringField(label="Describe your plan for this negotiation. In particular, how do intend to approach dealing with coalitions?")

    united = models.IntegerField()
    turbo = models.IntegerField()
    stockman= models.IntegerField()
    first_meeting = models.StringField(label="Whom did Turbo start the negotiation with?",choices=["Stockman","United","Both"], widget=widgets.RadioSelectHorizontal)

    #journaling_text = models.LongStringField(label="Please describe your experience of the negotiation.")


    def role(self):
        if self.id_in_group == 1:
            return 'stockman'
        elif self.id_in_group == 2:
            return 'turbo'
        else:
            return 'united'
