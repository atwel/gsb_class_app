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


with open("_rooms/Sp21_01.txt", "r") as f:
    raw_string = f.read()
    names_section1 = raw_string.split("\n")

with open("_rooms/Sp21_02.txt", "r") as f:
    raw_string = f.read()
    names_section2 = raw_string.replace("\n", ",")

with open("_rooms/Sp21_03.txt", "r") as f:
    raw_string = f.read()
    names_section3 = raw_string.replace("\n", ",")


class Constants(BaseConstants):
    name_in_url = 'Check_in'
    players_per_group = None
    num_rounds = 1

    link_581_1 = "https://stanford.zoom.us/j/96497241579?pwd=ZzgxeFFDOWQ3ODZxTnZ0OERVK0RMQT09"
    link_581_2 = "https://stanford.zoom.us/j/93359073372?pwd=TjZMTno1MUZUS1d3TUNkUHNERmJvZz09"
    link_581_3 = "https://stanford.zoom.us/j/96451384953?pwd=ZkZmeUllalhQM3JFMzBUNitFaDJoQT09"
    names_section1 = names_section1
    names_section2 = names_section2
    names_section3 = names_section3

class Subsession(BaseSubsession):

    def before_session_starts(self):
        if self.session.config["section_number"] == 1:
            section_participants = names_section1
            zoom_link = Constants.link_581_1
        elif self.session.config["section_number"] == 2:
            section_participants = names_section2
            zoom_link = Constants.link_581_2
        else:
            section_participants = names_section3
            zoom_link = Constants.link_581_3

        for player, label in zip(self.get_players(), section_participants):
            player.participant.label = label
            player.participant.vars["zoom_link"] = zoom_link
            player.participant.vars["section"] = self.session.config["section_number"]

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    healthcheck= models.BooleanField(label="Are you in compliance with GSB COVID on-campus policies? (i.e. Healthcheck submitted and OK'ed)",widget=widgets.RadioSelectHorizontal)
    inperson = models.BooleanField(label="Do you want to negotiate in person today?",widget=widgets.RadioSelectHorizontal)
    zoom_link = models.StringField()
    section = models.IntegerField()
