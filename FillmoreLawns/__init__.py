import random

from otree.api import *


author = 'Jon Atwell'.
doc = """
Negotating Fillmore Lawns
"""


class C(BaseConstants):
    NAME_IN_URL = 'HarborCo'
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    name = models.StringField()


# FUNCTIONS
def role(player: Player):
    if player.id_in_group == 1:
        return 'Stellar_Cove'
    elif player.id_in_group == 2:
        return 'Green_Living'
    elif player.id_in_group == 3:
        return 'Illium'
    elif player.id_in_group == 4:
        return 'Mayor_Gabriel'
    elif player.id_in_group == 5:
        return 'Our_Backyards'
    else:
        return 'Planning_Commission'


# PAGES
class Introduction(Page):
    form_model = "player"



class Harborco(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "Stellar_Cove"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "HarborCo/Harborco.pdf"}


class Union(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "union"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "HarborCo/Union.pdf"}


class Enviro(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "enviro"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "HarborCo/EnvironmentalLeague.pdf"}


class Governor(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "gov"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "HarborCo/Governor.pdf"}


class Ports(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "ports"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "HarborCo/OtherPorts.pdf"}


class Dcr(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "dcr"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "HarborCo/FederalDCR.pdf"}


class Planning_doc(Page):
    form_model = "player"
    # form_fields = ["planning_text"]
    @staticmethod
    def vars_for_template(player: Player):
        if role(player) == "dcr":
            return {
                "pdf_file": "HarborCo/FederalDCR.pdf",
                "assignment_url": "/173725/assignments/514484",
            }
        elif role(player) == "harborco":
            return {
                "pdf_file": "HarborCo/Harborco.pdf",
                "assignment_url": "/173725/assignments/514484",
            }
        elif role(player) == "ports":
            return {
                "pdf_file": "HarborCo/OtherPorts.pdf",
                "assignment_url": "/173725/assignments/514484",
            }
        elif role(player) == "union":
            return {
                "pdf_file": "HarborCo/Union.pdf",
                "assignment_url": "/173725/assignments/514484",
            }
        elif role(player) == "gov":
            return {
                "pdf_file": "HarborCo/Governor.pdf",
                "assignment_url": "/173725/assignments/514484",
            }
        elif role(player) == "enviro":
            return {
                "pdf_file": "HarborCo/EnvironmentalLeague.pdf",
                "assignment_url": "/173725/assignments/514484",
            }
        else:
            return {
                "pdf_file": "HarborCo/Governor.pdf",
                "assignment_url": "/173725/assignments/514484",
            }


class Back_to_class(Page):
    form_model = "player"


page_sequence = [
    Introduction,
    Union,
    Ports,
    Dcr,
    Harborco,
    Enviro,
    Governor,
    Planning_doc,
    Back_to_class,
    Union,
    Ports,
    Dcr,
    Harborco,
    Enviro,
    Governor,
]
