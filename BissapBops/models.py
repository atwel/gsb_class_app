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

import time

author = 'Jon Atwell'

doc = """
Negotatiing BissapBops with a partner
"""


class Constants(BaseConstants):
    name_in_url = 'BissapBops'
    players_per_group = 2
    num_rounds = 1
    reading_time = 20
    negotiating_time = 30
    planning_doc_length = 75
    planning_doc_time_minutes = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    deal = models.BooleanField(label="Did Osi and Ann-Marie reach a deal?",widget=widgets.RadioSelectHorizontal)
    split = models.BooleanField(label="Did the agreement split product lines across markets? (If this question is confusing, your answer is probably no)",widget=widgets.RadioSelectHorizontal)

    sla = models.IntegerField(label="What is the service level agreement (SLA)?", choices=[[99,"99%"],[95,"95%"], [90,"90%"],[0,"None"]], widget=widgets.RadioSelectHorizontal)
    warehouse = models.BooleanField(label="Will USA-Mart lease a warehouse to NJ LLC?",widget=widgets.RadioSelectHorizontal)
    contract = models.IntegerField(label="What is the exclusivity length of the contract?", choices=[[5,"5 years"], [3,"3 years"], [1,"1 year"], [0,"No exclusivity period"]], widget=widgets.RadioSelectHorizontal)
    location = models.IntegerField(label="What USA-Mart markets will stock NJ products?", choices=[[1,"Northeast cities"], [2,"NE cities and cities with large African and Carribean pops."], [3,"All USA-Mart locations"]], widget=widgets.RadioSelect)

    juice_lines_no_split = models.IntegerField(label="How many juices will USA-Mart carry?", choices=[[3,"3 in int'l aisle"], [6,"6, all int'l aisle"], [7,"6, split across standard and int'l aisles"], [9, "9 juices, across aisles"], [12,"All 12 juice SKUs"]], widget=widgets.RadioSelect)
    spice_no_split = models.IntegerField(label="How many spice and dried fruit SKUs will USA-Mart carry?",choices=[0,1,2,3,4,5,6])
    juice_split1 = models.IntegerField(label="How many juices will USA-Mart carry in the first market segment?", choices=[[3,"3 in int'l aisle"], [6,"6, all int'l aisle"], [7,"6, split across standard and int'l aisles"], [9, "9 juices, across aisles"], [12,"All 12 juice SKUs"]], widget=widgets.RadioSelect)
    spice_split1 = models.IntegerField(label="How many spice and dried fruit SKUs will USA-Mart carry in the first market segment?",choices=[0,1,2,3,4,5,6])
    juice_split2 = models.IntegerField(label="How many juices will USA-Mart carry in the second market segment?", choices=[[3,"3 in int'l aisle"], [6,"6, all int'l aisle"], [7,"6, split across standard and int'l aisles"], [9, "9 juices, across aisles"], [12,"All 12 juice SKUs"]], widget=widgets.RadioSelect)
    spice_split2 = models.IntegerField(label="How many spice and dried fruit SKUs will USA-Mart carry in the second market segment?",choices=[0,1,2,3,4,5,6])

    def set_timer(self):
        start_time = time.time()
        for player in self.get_players():
            player.participant.vars["sim_timer"] = start_time + Constants.negotiating_time * 60 + 30

class Player(BasePlayer):
    planning_text = models.LongStringField(label="Describe your plan for this negotiation.")
    journaling_text = models.LongStringField(label="Please describe your experience of the negotiation.")
    partner = models.StringField()
    name = models.StringField()
    grole = models.StringField()

    def waiting_too_long(self):
        return time.time() - self.participant.vars['arrival_time'] > 120
