import random

from otree.api import *


author = 'Jon Atwell'
doc = """
Negotating OmniChannel with two teams
"""


class C(BaseConstants):
    NAME_IN_URL = 'OmniChannel'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    READING_TIME = 10
    PLANNING_DOC_TIME = 10  # minutes
    COORDINATING_TIME = 20
    NEGOTIATING_TIME = 60
    PLANNING_DOC_LENGTH = 100  # words


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
    planning_text = models.LongStringField(
        label="Describe your plan for this negotiation. In particular, how do intend to approach dealing with team members"
    )
    journaling_text = models.LongStringField(
        label="Please describe your experience of the negotiation."
    )


# FUNCTIONS
def vars_for_admin_report(subsession: Subsession):
    omni = []
    DTV = []
    for p in subsession.get_players():
        if p.role() == "3dtv":
            DTV.append(p.name)
        else:
            omni.append(p.name)
    return {"DTV_ip": DTV, "Omni_ip": omni}


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


# PAGES
SUNet_to_name = {
    "extra1": "Unnamed #1",
    "extra2": "Unnamed #2",
    "extra3": "Unnamed #3",
    "extra4": "Unnamed #4",
    "extra5": "Unnamed #5",
    "extra6": "Unnamed #6",
    "extra7": "Unnamed #7",
    "extra8": "Unnamed #8",
    "extra9": "Unnamed #9",
    "extra10": "Unnamed #10",
}


class Introduction(Page):
    form_model = "player"

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        try:
            player.participant.vars["SUNet"] = player.participant.label
            player.participant.vars["name"] = SUNet_to_name[player.participant.label]
        except:
            player.participant.vars["SUNet"] = "none"
            player.participant.vars["name"] = "(come see Dr. Atwell)"
        player.name = player.participant.vars["name"]


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


class Message_DTV(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "3dtv"


class Message_OC(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "omni"


class Planning_doc(Page):
    form_model = "player"
    # timeout_seconds= C.PLANNING_DOC_TIME * 60
    # timer_text = 'Time left to finish writing your planning document'
    @staticmethod
    def vars_for_template(player: Player):
        if role(player) == "3dtv":
            return {
                "pdf_file": "OmniChannel/3DTV.pdf",
                "assignment_url": "/173725/assignments/514474",
            }
        elif role(player) == "omni":
            return {
                "pdf_file": "OmniChannel/OmniChannel.pdf",
                "assignment_url": "/173725/assignments/514474",
            }


class Wait_until_open(Page):
    form_model = "player"
    # remove  next line when not demo-ing
    # timeout_seconds = 10


class Agreement(Page):
    form_model = "player"
    form_fields = ["agreement"]

    @staticmethod
    def is_displayed(player: Player):
        if role(player) == "3dtv":
            return True
        else:
            return False


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
        if role(player) == "3dtv" and player.agreement == "Yes":
            return True
        else:
            return False


class Journaling_page(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player: Player):
        return {"assignment_url": "/173725/assignments/514475"}


class Outro(Page):
    form_model = "group"


page_sequence = [
    Introduction,
    DTV,
    Omni,
    Message_DTV,
    Message_OC,
    Planning_doc,
    Wait_until_open,
    DTV,
    Omni,
    Agreement,
    Outcome,
    Journaling_page,
    Outro,
]
