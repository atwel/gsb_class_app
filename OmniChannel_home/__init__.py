import random

from otree.api import *


author = 'Jon Atwell'
doc = """
Negotating OmniChannel with two teams
"""

SUNet_to_name = {
}


class C(BaseConstants):
    NAME_IN_URL = 'OC'
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 1
    COORDINATING_TIME = 30
    NEGOTIATING_TIME = 75
    CLASSCODE = 190881
    PLANNING_ASSIGNMENT_CODE = 610671
    FEEDBACK_ASSIGNMENT_CODE = 610877

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    name = models.StringField()

def role(player: Player):
    try:
        player.name = SUNet_to_name[player.participant.label]
        # self.participant.label = SUNet_to_name[self.participant.label]
    except:
        pass
    if player.id_in_group == 1:
        return '3dtv'
    elif player.id_in_group == 2:
        return 'omni'
    elif player.id_in_group == 3:
        return '3dtv'
    elif player.id_in_group == 4:
        return 'omni'
    elif player.id_in_group == 5:
        return '3dtv'
    else:
        return 'omni'



class Introduction(Page):
    form_model = "player"

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        try:
            player.name = SUNet_to_name[player.participant.label]
        except:
            player.participant.vars["name"] = "(come see Dr. Atwell)"



class DTV(Page):
    form_model = "player"
    # timeout_seconds= C.READING_TIME * 60
    # timer_text = 'Time left for reading the materials'
    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "3dtv"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "OmniChannel/3DTV.pdf"}


class Omni(Page):
    form_model = "player"
    # timeout_seconds= C.READING_TIME * 60
    # timer_text = 'Time left for reading the materials'
    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "omni"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "OmniChannel/OmniChannel.pdf"}


class Planning_doc(Page):
    form_model = "player"
    # timeout_seconds= C.PLANNING_DOC_TIME * 60
    # timer_text = 'Time left to finish writing your planning document'

    @staticmethod
    def vars_for_template(player: Player):
        url  = "/{}/assignments/{}".format(C.CLASSCODE, C.PLANNING_ASSIGNMENT_CODE)
        if role(player) == "3dtv":
            return {
                "pdf_file": "OmniChannel/3DTV.pdf",
                "assignment_url": url,
                "submission_time": "two hours before class"
            }
        elif role(player) == "omni":
            return {
                "pdf_file": "OmniChannel/OmniChannel.pdf",
                "assignment_url": url,
                "submission_time": "two hours before class"
            }


class Outro(Page):
    form_model = "group"


page_sequence = [
    Introduction,
    DTV,
    Omni,
    Planning_doc,
    Outro
]
