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
Negotatiing BioPharm Seltek with a partner
"""


class Constants(BaseConstants):
    name_in_url = 'NoCode'
    players_per_group = 2
    num_rounds = 1
    reading_time = 15
    negotiation_time = 25
    planning_doc_length = 75
    planning_doc_time_minutes = 10
    negotiating_time = 25


class Subsession(BaseSubsession):
    pass
    """def group_by_arrival_time_method(self,waiting_players):

        if self.session.config["section_number"] == 1:
            locations = locations_1
        elif self.session.config["section_number"] == 2:
            locations = locations_2
        elif self.session.config["section_number"] == 3:
            locations = locations_3


        inperson_players = [p for p in waiting_players if p.participant.vars['inperson']]
        zoom_players = [p for p in waiting_players if not p.participant.vars['inperson']]

        if len(inperson_players) >= 2:
            print('about to create in person group')
            one = inperson_players.pop(0)
            two = inperson_players.pop(0)
            one.partner = two.participant.vars["name"]
            two.partner = one.participant.vars["name"]

            if locations != []:
                loc = locations.pop(0)
                one.meeting_inperson = True
                two.meeting_inperson = True
            else:
                loc = "Zoom breakout"
                one.zoom_group = "{} and {} ({}-{})".format(two.partner,one.partner,one.participant.label, two.participant.label)

            one.location = loc
            two.location = loc
            pair = [one, two]
            for p in pair:
                print(p.participant.vars["name"], p.participant.label, p.location, p.participant.vars["inperson"], p.partner)
            return pair

        elif len(zoom_players) >= 2:
            print('about to create Zoom group')
            one = zoom_players.pop(0)
            two = zoom_players.pop(0)
            loc = "Zoom breakout"
            one.location = loc
            two.location = loc
            one.partner = two.participant.vars["name"]
            two.partner = one.participant.vars["name"]
            one.zoom_group = "{} and {} ({}-{})".format(two.partner,one.partner,one.participant.label, two.participant.label)
            pair = [one, two]
            for p in pair:
                print(p.participant.vars["name"], p.participant.label, p.location, p.participant.vars["inperson"], p.partner)

            return pair

        else:
            still_waiting = []
            for player in waiting_players:
                if player.waiting_too_long():
                    still_waiting.append(player)
            if len(still_waiting) == 2:
                print('about to create Zoom group with waiting people')
                one = still_waiting.pop(0)
                two = still_waiting.pop(0)
                loc = "Zoom breakout"
                one.location = loc
                two.location = loc
                one.partner = two.participant.vars["name"]
                two.partner = one.participant.vars["name"]
                one.zoom_group = "{} and {} ({}-{})".format(two.partner,one.partner,one.participant.label, two.participant.label)
                pair = [one, two]
                for p in pair:
                    print(p.participant.vars["name"], p.participant.label, p.location, p.participant.vars["inperson"], p.partner)

                return pair
            elif len(still_waiting) == 1 and len(zoom_players) == 1:
                if still_waiting[0] != zoom_players[0]:
                    print('about to create Zoom group with waiting people')
                    one = still_waiting.pop(0)
                    two = zoom_players.pop(0)
                    loc = "Zoom breakout"
                    one.location = loc
                    two.location = loc
                    one.partner = two.participant.vars["name"]
                    two.partner = one.participant.vars["name"]
                    one.zoom_group = "{} and {} ({}-{})".format(two.partner,one.partner,one.participant.label, two.participant.label)
                    pair = [one, two]
                    for p in pair:
                        print(p.participant.vars["name"], p.participant.label, p.location, p.participant.vars["inperson"], p.partner)
                    return pair
            else:
                if still_waiting != []:
                    name = still_waiting[0].participant.vars["name"]
                    print("{} has been waiting for 2+ minutes".format(name))
                else:
                    print('not enough players yet to create a group')
    """
    """def vars_for_admin_report(self):
        zoomies = []
        for player in self.get_players():
            if player.zoom_group != None:
                zoomies.append(player.zoom_group)
        return dict(zoom_groups=",\n".join(zoomies))
    """



class Group(BaseGroup):
    deal = models.BooleanField(label="Did Stanfield and Sproles reach a deal?",widget=widgets.RadioSelectHorizontal)
    Salary = models.CurrencyField(label="What is the salary?")
    Bonus = models.CurrencyField(label="What is the bonus?")
    Equity = models.FloatField(label="What is the equity amount (%)?")
    Days = models.StringField(label="How many days a week can be remote?", choices=["Zero","One", "Two or Three"], widget=widgets.RadioSelectHorizontal)
    Start = models.IntegerField(label="When will Stanfield start?", choices=[[1,"Immediately"], [2,"Three Months"], [3,"Fifteen Months"], [4,"No Start"]], widget=widgets.RadioSelectHorizontal)

    last_Salary_Stanfield = models.CurrencyField(label="What was the last salary Stanfield asked for?")
    last_Bonus_Stanfield = models.CurrencyField(label="What was the last bonus Stanfield asked for?")
    last_Equity_Stanfield = models.FloatField(label="What was the last equity amount Stanfield asked for?")
    last_Days_Stanfield = models.StringField(label="How many remote days did Stanfield last ask for?", choices=["Zero","One", "Two or Three"], widget=widgets.RadioSelectHorizontal)
    last_Start_Stanfield = models.IntegerField(label="In what timeframe did Stanfield last ask to start?", choices=[[1,"Immediately"], [2,"Three Months"], [3,"Fifteen Months"], [4,"No Start"]], widget=widgets.RadioSelectHorizontal)

    last_Salary_Sproles = models.CurrencyField(label="What was the last salary Sproles proposed?")
    last_Bonus_Sproles = models.CurrencyField(label="What was the last bonus Sproles proposed?")
    last_Equity_Sproles = models.FloatField(label="What was the last equity amount Sproles proposed?")
    last_Days_Sproles = models.StringField(label="How many remote days did Sproles last propose?", choices=["Zero","One", "Two or Three"], widget=widgets.RadioSelectHorizontal)
    last_Start_Sproles = models.IntegerField(label="What timeframe for Stanfield's start did Sproles last propose?", choices=[[1,"Immediately"], [2,"Three Months"], [3,"Fifteen Months"], [4,"No Start"]], widget=widgets.RadioSelectHorizontal)

    def set_timer(self):
        start_time = time.time()
        for player in self.get_players():
            player.participant.vars["sim_timer"] = start_time + Constants.negotiating_time * 60 + 30

class Player(BasePlayer):
    planning_text = models.LongStringField(label="Describe your plan for this negotiation.")
    journaling_text = models.LongStringField(label="Please describe your experience of the negotiation.")
    target_points = models.IntegerField(label="What is your target amount of points going into this negotiation?")
    partner = models.StringField()
    name = models.StringField()
    grole = models.StringField()


    def waiting_too_long(self):
        return time.time() - self.participant.vars['arrival_time'] > 120
