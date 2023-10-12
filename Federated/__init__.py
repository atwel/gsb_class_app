import datetime
import itertools
import random

from otree.api import *


author = 'Jon Atwell'
doc = """
Negotiating Federated Sciences with two partners
"""


class C(BaseConstants):
    NAME_IN_URL = 'Federated_Sciences'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    READING_TIME = 10  # minutes
    MATERIAL_BUTTON_SHOW = 2  # minutes
    PLANNING_DOC_TIME = 10
    NEGOTIATING_TIME = 30  # minutes
    REFLECTION_TIME = 5  # minutes
    PLANNING_DOC_LENGTH = 100  # words


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    stockman = models.BooleanField()
    pairing = models.StringField()
    end_time = models.StringField()
    started = models.BooleanField(initial=False)


class Player(BasePlayer):
    name = models.StringField()
    # planning_text = models.LongStringField(label="Describe your plan for this negotiation. In particular, how do intend to approach dealing with coalitions?")
    united = models.IntegerField()
    turbo = models.IntegerField()
    stockman = models.IntegerField()
    first_meeting = models.StringField(
        label="Whom did Turbo start the negotiation with?",
        choices=["Stockman", "United", "Both"],
        widget=widgets.RadioSelectHorizontal,
    )
    # journaling_text = models.LongStringField(label="Please describe your experience of the negotiation.")


# FUNCTIONS
def creating_session(subsession: Subsession):
    stock = itertools.cycle([True, False])
    for g in subsession.get_groups():
        g.stockman = next(stock)


def vars_for_admin_report(subsession: Subsession):
    stockman = []
    united = []
    turbo = []
    for p in subsession.get_players():
        the_label = p.participant.vars["name"]
        if p.role() == "stockman":
            stockman.append(the_label)
        elif p.role() == "turbo":
            turbo.append(the_label)
        else:
            united.append(the_label)
    return {"Stockman": stockman, "Turbo": turbo, "United": united}


def set_end_time(group: Group):
    group.end_time = (
        datetime.datetime.now() + datetime.timedelta(minutes=C.NEGOTIATING_TIME + 1)
    ).strftime("%H:%M:%S")
    group.started = True


def set_first_meet(group: Group):
    for i, p in enumerate(group.get_players()):
        try:
            p.name = SUNet_to_name[p.participant.label]
        except:
            p.name = "Demo_{}".format(i)
    for p in group.get_players():
        if p.role() == "stockman":
            stockman = p.name
        elif p.role() == "turbo":
            turbo = p.name
        else:
            united = p.name
    if group.stockman:
        group.pairing = ",".join([united, stockman, turbo])
    else:
        group.pairing = ",".join([united, turbo, stockman])


def role(player: Player):
    if player.id_in_group == 1:
        return 'stockman'
    elif player.id_in_group == 2:
        return 'turbo'
    else:
        return 'united'


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


class IntroWaitPage(WaitPage):
    group_by_arrival_time = True

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": "Waiting for others",
            "body_text": "Please wait a moment while you're assigned to a group.\n\n",
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


class Stockman(Page):
    form_model = "player"
    # timeout_seconds = C.READING_TIME*60
    # timer_text = 'Time left for reading the materials'
    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "stockman"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Federated/Stockman.pdf", "End_time": "", "show_end_time": False}

    @staticmethod
    def js_vars(player: Player):
        return dict(button_show=C.MATERIAL_BUTTON_SHOW * 60000)


class Stockman_nt(Page):
    form_model = "player"
    template_name = "Federated/Stockman.html"

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "stockman"

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "pdf_file": "Federated/Stockman.pdf",
            "End_time": player.group.end_time,
            "show_end_time": False,
        }

    @staticmethod
    def js_vars(player: Player):
        return dict(button_show=C.MATERIAL_BUTTON_SHOW * 60000)


class Turbo(Page):
    form_model = "player"
    # timeout_seconds = C.READING_TIME*60
    # timer_text = 'Time left for reading the materials'
    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "turbo"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Federated/Turbo.pdf", "End_time": "", "show_end_time": False}

    @staticmethod
    def js_vars(player: Player):
        return dict(button_show=C.MATERIAL_BUTTON_SHOW * 60000)


class Turbo_nt(Page):
    form_model = "player"
    template_name = "Federated/Turbo.html"

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "turbo"

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "pdf_file": "Federated/Turbo.pdf",
            "End_time": player.group.end_time,
            "show_end_time": False,
        }

    @staticmethod
    def js_vars(player: Player):
        return dict(button_show=C.MATERIAL_BUTTON_SHOW * 60000)


class United(Page):
    form_model = "player"
    # timeout_seconds = C.READING_TIME*60
    # timer_text = 'Time left for reading the materials'
    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "united"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Federated/United.pdf", "End_time": "", "show_end_time": False}

    @staticmethod
    def js_vars(player: Player):
        return dict(button_show=C.MATERIAL_BUTTON_SHOW * 60000)


class United_nt(Page):
    form_model = "player"
    template_name = "Federated/United.html"

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "united"

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "pdf_file": "Federated/United.pdf",
            "End_time": player.group.end_time,
            "show_end_time": False,
        }

    @staticmethod
    def js_vars(player: Player):
        return dict(button_show=C.MATERIAL_BUTTON_SHOW * 60000)


class Planning_doc(Page):
    form_model = "player"
    # form_fields = ["planning_text"]
    # timeout_seconds = C.PLANNING_DOC_TIME *60
    # timer_text = "Time left to finish the planning document"
    @staticmethod
    def vars_for_template(player: Player):
        if role(player) == "stockman":
            return {"pdf_file": "Federated/Stockman.pdf", "assignment_url":"/173725/assignments/514461"}
        elif role(player) == "turbo":
            return {"pdf_file": "Federated/Turbo.pdf", "assignment_url":"/173725/assignments/514461"}
        elif role(player) == "united":
            return {"pdf_file": "Federated/United.pdf", "assignment_url":"/173725/assignments/514461"}


class Ready_for_class(Page):
    form_model = "player"


class Wait_to_negotiate(WaitPage):
    form_model = "group"

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": "Waiting for your counterparts to finish preparing",
            "body_text": "It shouldn't be too long now!\n\n",
        }


class Back_to_class(Page):
    form_model = "player"

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if not player.group.started:
            set_end_time(player.group)

    @staticmethod
    def vars_for_template(player: Player):
        partners = player.get_others_in_group()
        part_1 = partners[0].name
        part_2 = partners[1].name
        if player.group.stockman:
            if role(player) == "united":
                return {
                    "rep": "United",
                    "alter": "Stockman",
                    "in_first": True,
                    "partner_1": part_1,
                    "partner_2": part_2,
                }
            elif role(player) == "stockman":
                return {
                    "alter": "United",
                    "rep": "Stockman",
                    "in_first": True,
                    "partner_1": part_1,
                    "partner_2": part_2,
                }
            else:
                return {
                    "rep": "Turbo",
                    "alter": "NA",
                    "in_first": False,
                    "partner_1": part_1,
                    "partner_2": part_2,
                }
        else:
            if role(player) == "united":
                return {
                    "rep": "United",
                    "alter": "Turbo",
                    "in_first": True,
                    "partner_1": part_1,
                    "partner_2": part_2,
                }
            elif role(player) == "turbo":
                return {
                    "alter": "United",
                    "rep": "Turbo",
                    "in_first": True,
                    "partner_1": part_1,
                    "partner_2": part_2,
                }
            else:
                return {
                    "rep": "Stockman",
                    "alter": "NA",
                    "in_first": False,
                    "partner_1": part_1,
                    "partner_2": part_2,
                }


class Outcome(Page):
    form_model = "player"
    form_fields = ["united", "stockman", "turbo", "first_meeting"]


class Journaling_page(Page):
    form_model = "player"
    def vars_for_template(player: Player):
        return {"assignment_url": "/173725/assignments/514463"}


class Outro(Page):
    form_model = "group"


page_sequence = [
    Introduction,
    Stockman,
    Turbo,
    United,
    Planning_doc,
    Ready_for_class,
    Wait_to_negotiate,
    Back_to_class,
    Stockman_nt,
    Turbo_nt,
    United_nt,
    Outcome,
    Journaling_page,
    Outro,
]
