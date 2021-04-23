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

locations_1 = ["Campus Dr Grove 1","Campus Dr Grove 2","Campus Dr Grove 3","Campus Dr Lawn 1","Campus Dr Lawn 2","Campus Dr Lawn 3","Community Court 1","Community Court 2","Community Court 3","Community Court 4","Community Court 5","GSB Bowl 1","GSB Bowl 2","GSB Bowl 3","Knight Way 1"]
locations_2 = ["Campus Dr Lawn 1","Campus Dr Lawn 2","Campus Dr Lawn 3","Community Court 1","Community Court 2","Community Court 3","Community Court 4","Community Court 5","GSB Bowl 1","GSB Bowl 2","GSB Bowl 3","Knight Way 1","Knight Way 2","Knight Way 3","Knight Way 4","Town Square 3","Town Square 4"]
locations_3 = ["Campus Dr Grove 1 ","Campus Dr Grove 2","Campus Dr Grove 3","Campus Dr Lawn 1","Campus Dr Lawn 2","Campus Dr Lawn 3","Community Court 1","Community Court 2","Community Court 3","Community Court 4","Community Court 5","Knight Way 1","Knight Way 2","Knight Way 3","Knight Way 4","Town Square 1","Town Square 3","Town Square 4","Town Square 5","Town Square 6"]


class Constants(BaseConstants):
    name_in_url = 'BiopharmSeltek'
    players_per_group = 2
    num_rounds = 1
    reading_time = 10
    planning_doc_length = 100
    planning_doc_time_minutes = 5
    negotiating_time = 25


class Subsession(BaseSubsession):
    def group_by_arrival_time_method(self,waiting_players):

        print('in group_by_arrival_time_method')
        inperson_players = [p for p in waiting_players if p.participant.vars['inperson']]
        zoom_players = [p for p in waiting_players if not p.participant.vars['inperson']]

        if len(inperson_players) >= 2:
            print('about to create in person group')
            one = inperson_players.pop(0)
            two = inperson_players.pop(0)
            one.partner = two.participant.vars["name"]
            two.partner = one.participant.vars["name"]
            if one.participant.vars["section"] == 1:
                if locations_1 != []:
                    loc = locations_1.pop(0)
                    one.meeting_inperson = True
                    two.meeting_inperson = True
                else:
                    loc = "Zoom breakout"
                    one.zoom_group = "{} and {} ({}-{})".format(two.partner,one.partner,one.participant.label, two.participant.label)
            elif one.participant.vars["section"] == 2:
                if locations_2 != []:
                    loc = locations_2.pop(0)
                    one.meeting_inperson = True
                    two.meeting_inperson = True
                else:
                    loc = "Zoom breakout"
                    one.zoom_group = "{} and {} ({}-{})".format(two.partner,one.partner,one.participant.label, two.participant.label)
            else:
                if locations_3 != []:
                    loc = locations_3.pop(0)
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



class Group(BaseGroup):
    link = models.StringField(label="Stanford Zoom URL")
    link_to_recording = models.StringField(label="Please provide the link to your recording.")
    initial_price = models.CurrencyField(label="What was the price of the first offer in millions of USD (e.g. XX.xx )?")
    made_initial = models.StringField(choices=["BioPharm","Seltek"], widget=widgets.RadioSelectHorizontal, label="Which company made the first offer?")
    deal = models.BooleanField(label="Did the companies reach a deal?",widget=widgets.RadioSelectHorizontal)
    last_Biopharm = models.CurrencyField(label="What was the last offer made by BioPharm in millions of USD (e.g. XX.x)?")
    last_Seltek = models.CurrencyField(label="What was the last offer made by Seltek in millions of USD (e.g. XX.xx)?")
    final_sale_price = models.CurrencyField(label="What was the Final Sale Price in millions of USD (e.g. XX.xx)?")
    batna_BF = models.CurrencyField(label="At what price in millions of USD should you walk away without a deal?")
    target_BF = models.CurrencyField(label="What is your ideal purchase price for the Seltek plant in millions of USD (e.g. XX.xx)?")
    batna_ST = models.CurrencyField(label="At what price in millions of USD should you walk away without a deal?")
    target_ST = models.CurrencyField(label="What is your ideal sale price for your plant in millions of USD (e.g. XX.x)?")
    nego_time = models.IntegerField()

    def set_timer(self):
        start_time = time.time()
        for player in self.get_players():
            player.participant.vars["sim_timer"] = start_time + Constants.negotiating_time * 60 + 30

class Player(BasePlayer):
    planning_text = models.LongStringField(label="Describe your plan for this negotiation")
    journaling_text = models.LongStringField(label="Please describe your experience of the negotiation.")
    location = models.StringField(label="Negotiation location")
    meeting_inperson = models.BooleanField(default=False)
    partner = models.StringField()
    zoom_group = models.StringField()

    def waiting_too_long(self):
        return time.time() - self.participant.vars['arrival_time'] > 120
