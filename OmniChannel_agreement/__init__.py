import random

from otree.api import *


author = 'Jon Atwell'
doc = """
Reporting OmniChannel outcome
"""


class C(BaseConstants):
    NAME_IN_URL = 'OmniChannel_report'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    name = models.StringField()
    agreement = models.StringField(
        label="Did the parties reach an agreement on all 9 issues? If not, you'll skip inputting the agreement.",
        choices=["Yes", "No"],
    )
    data = models.StringField(
        label="Use of Manipulated Data",
        choices=[
            "3DTV has a perpetual license to use the data for internal research.",
            "3DTV has a license to use that for internal research during the agreement term.",
            "3DTV cannot use manipulated data for internal research.",
        ],
    )
    license_restrictions = models.StringField(
        label="Data License Restriction",
        choices=[
            "3DTV can offer the content to their subscribers in 2D or 3D format.",
            "3DTV can offer the content to their subscribers in 3D format only.",
        ],
    )
    premium_count = models.IntegerField(
        label="# of Premium channels licensed", choices=[0, 5, 10, 15, 20]
    )
    premium_fees = models.IntegerField(
        label="Fees for PremiumTV ($/month)", choices=[11000, 12000, 13000, 14000, 15000]
    )
    regular_count = models.IntegerField(
        label="# of OC channels licensed", choices=[60, 70, 80, 90, 100]
    )
    regular_fees = models.IntegerField(
        label="Fees for OC channels ($/month)", choices=[600, 700, 800, 900, 1000]
    )
    data_center_fees = models.IntegerField(
        label="Fees for using 3DTV's data centers ($/month)",
        choices=[30000, 25000, 20000, 15000, 10000],
    )
    length = models.IntegerField(label="Length of Agreement (years)", choices=[8, 7, 6, 5, 4])
    termination = models.IntegerField(
        label="Termination Options (months notice required)", choices=[12, 9, 6, 3, 1]
    )


def role(player: Player):

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


class Agreement(Page):
    form_model = "player"
    form_fields = ["agreement"]


class Outcome(Page):
    form_model = "player"
    form_fields = [
        "data",
        "license_restrictions",
        "premium_count",
        "premium_fees",
        "regular_count",
        "regular_fees",
        "data_center_fees",
        "length",
        "termination",
    ]

    @staticmethod
    def is_displayed(player: Player):
        if player.agreement == "Yes":
            return True
        else:
            return False



class Outro(Page):
    form_model = "group"


page_sequence = [
    Agreement,
    Outcome,
    Outro,
]
