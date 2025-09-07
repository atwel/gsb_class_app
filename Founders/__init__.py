from otree.api import *


author = 'Jon and Seyeon'
doc = """
Founders penalty experiment
"""


class C(BaseConstants):

    NAME_IN_URL = 'Founders'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


class Resumes(Page):
    form_model = "player"
    form_fields = []

    @staticmethod
    def js_vars(player: Player):
        return {"first_summary": "Founders/Summary_WS.png",
                    "first_resume":"Founders/Resume_WS.pdf"}


page_sequence = [Resumes]
