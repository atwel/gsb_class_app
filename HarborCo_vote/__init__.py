import random
import time

from otree.api import *


author = 'Jon Atwell'
doc = """
Voting platform for HarborCo
"""
with open("_rooms/FALL23_01.txt", "r") as f:
    raw_string = f.read()
    names_section1 = raw_string.split("\n")
    # names_section1.pop()
with open("_rooms/FALL23_02.txt", "r") as f:
    raw_string = f.read()
    names_section2 = raw_string.split("\n")
    # names_section2.pop()
with open("_rooms/Sp23_03.txt", "r") as f:
    raw_string = f.read()
    names_section3 = raw_string.split("\n")
    # names_section3.pop()
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


class C(BaseConstants):
    NAME_IN_URL = 'Voting'
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 10
    SUNET_TO_NAME = SUNet_to_name
    NAMES_SECTION1 = names_section1
    NAMES_SECTION2 = names_section2
    NAMES_SECTION3 = names_section3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    mix = models.StringField(
        label="Industry Mix",
        choices=["Primarily dirty", "Clean & dirty", "All clean"],
        initial="Primarily dirty",
    )
    eco = models.StringField(
        label="Ecological Impact",
        choices=["Some harm", "Maintain & repair", "Improve"],
        initial="Some harm",
    )
    union = models.StringField(
        label="Employment Rules",
        choices=[
            "Unlimited union preference",
            "Union quota 2:1",
            "Union quota 1:1",
            "No union preference",
        ],
        initial="No union preference",
    )
    loan = models.StringField(
        label="Federal Loan",
        choices=["$3 Billion", "$2 Billion", "$1 Billion", "No federal loan"],
        initial="$3 Billion",
    )
    comp = models.StringField(
        label="Compensation to other ports",
        choices=[
            "HarborCo pays $600 million",
            "HarborCo pays $450 million",
            "HarborCo pays $300 million",
            "HarborCo pays $150 million",
            "HarborCo pays nothing",
        ],
        initial="HarborCo pays nothing",
    )
    passed = models.BooleanField(default=False)
    high_passed = models.BooleanField(default=False)
    vetoed = models.BooleanField(default=False)
    did_not_pass = models.BooleanField(default=True)
    timed_out = models.BooleanField(default=False)
    pass_displayed = models.BooleanField(default=False)
    start_time = models.FloatField()


class Player(BasePlayer):
    name = models.StringField()
    vote = models.StringField(
        choices=["Yes", "No"],
        label="Would you like to vote in favor of this proposal?",
        initial="No",
    )


# FUNCTIONS
def creating_session(subsession: Subsession):
    if subsession.session.config["section_number"] == 1:
        section_labels = C.NAMES_SECTION1.copy()
    elif subsession.session.config["section_number"] == 2:
        section_labels = C.NAMES_SECTION2.copy()
    elif subsession.session.config["section_number"] == 3:
        section_labels = C.NAMES_SECTION3.copy()
    print(section_labels)
    print(len(subsession.get_players()), len(section_labels))
    for p in subsession.get_players():
        p.participant.label = section_labels.pop(0)


def role(player: Player):
    if player.id_in_group == 1:
        return 'union'
    elif player.id_in_group == 2:
        return 'enviro'
    elif player.id_in_group == 3:
        return 'ports'
    elif player.id_in_group == 4:
        return 'dcr'
    elif player.id_in_group == 5:
        return 'gov'
    else:
        return 'harborco'


# PAGES
class New_round(Page):
    form_model = "group"
    timeout_seconds = 120

    @staticmethod
    def is_displayed(player: Player):
        if player.subsession.round_number == 1:
            return True
        else:
            if (
                not all([g.did_not_pass for g in player.group.in_previous_rounds()])
                or player.group.in_round(player.group.round_number - 1).timed_out
            ):
                player.group.did_not_pass = False
                player.group.timed_out = True
                player.group.pass_displayed = True
            return False

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if role(player) == "harborco":
            if player.subsession.round_number == 1:
                player.group.start_time = time.time()


class Proposal(Page):
    form_model = "group"
    form_fields = ["mix", "eco", "union", "loan", "comp"]

    @staticmethod
    def is_displayed(player: Player):
        return player.group.did_not_pass and role(player) == "harborco"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "HarborCo/Harborco.pdf"}


class Proposal_wait(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.group.did_not_pass and not player.group.pass_displayed

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": "Negotiations and Proposal Crafting",
            "body_text": "You are currently in negotiations and will remain so until a scheduled vote is called or HarborCo puts a proposal up for a vote.",
        }


class Vote(Page):
    form_model = "player"
    form_fields = ["vote"]
    timeout_seconds = 90

    @staticmethod
    def is_displayed(player: Player):
        return player.group.did_not_pass and role(player) != "harborco"

    @staticmethod
    def vars_for_template(player: Player):
        if role(player) == "union":
            pdf_file = "HarborCo/Union.pdf"
        if role(player) == "enviro":
            pdf_file = "HarborCo/EnvironmentalLeague.pdf"
        if role(player) == "gov":
            pdf_file = "HarborCo/Governor.pdf"
        if role(player) == "ports":
            pdf_file = "HarborCo/OtherPorts.pdf"
        if role(player) == "dcr":
            pdf_file = "HarborCo/FederalDCR.pdf"
        eco_if = player.group.eco == "Some harm"
        loan_if = player.group.loan != "No federal loan"
        return {
            "eco_if": eco_if,
            "pdf_file": pdf_file,
            "loan_if": loan_if,
            "eco": player.group.eco.lower(),
            "mix": player.group.mix.lower(),
            "loan": player.group.loan.lower(),
            "union": player.group.union.lower(),
            "comp": player.group.comp,
        }


class Tally(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.group.did_not_pass

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": "Waiting for all votes to be cast.",
            "body_text": "Other parties are still voting. Once votes are in and tallied, the results will be shown.",
        }

    @staticmethod
    def after_all_players_arrive(group: Group):
        if group.did_not_pass:
            count = 0
            veto = False
            for p in group.get_players():
                if p.vote == "Yes":
                    count += 1
                if p.role() == "dcr":
                    if p.vote == "No" and group.loan != "No federal loan":
                        veto = True
            if veto:
                group.high_passed = False
                group.passed = False
                group.vetoed = True
                group.did_not_pass = True
            else:
                group.vetoed = False
                if count == 5:
                    group.high_passed = True
                    group.passed = False
                    group.did_not_pass = False
                elif count == 4:
                    group.high_passed = False
                    group.passed = True
                    group.did_not_pass = False
                elif count <= 3:
                    group.high_passed = False
                    group.passed = False
                    group.did_not_pass = True
        # print(time.time(), self.group.in_round(1).start_time)
        # print("time passed", (time.time() - self.group.in_round(1).start_time)/60)
        # if (time.time() - self.group.in_round(1).start_time) / 60 > 75:
        #    if not any([self.group.passed, self.group.high_passed]):
        #        self.group.timed_out = True


class Results_high_pass(Page):
    form_model = "group"
    timeout_seconds = 60

    @staticmethod
    def is_displayed(player: Player):
        value = player.group.high_passed and not player.group.pass_displayed
        return value

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.group.pass_displayed = True

    @staticmethod
    def vars_for_template(player: Player):
        for p in player.group.get_players():
            if p.role() == "union":
                if p.vote == "Yes":
                    union = "For"
                else:
                    union = "Against"
            if p.role() == "gov":
                if p.vote == "Yes":
                    gov = "For"
                else:
                    gov = "Against"
            if p.role() == "dcr":
                if p.vote == "Yes":
                    dcr = "For"
                else:
                    dcr = "Against"
            if p.role() == "enviro":
                if p.vote == "Yes":
                    enviro = "For"
                else:
                    enviro = "Against"
            if p.role() == "ports":
                if p.vote == "Yes":
                    ports = "For"
                else:
                    ports = "Against"
        return {"union": union, "gov": gov, "ports": ports, "enviro": enviro, "dcr": dcr}


class Results_pass(Page):
    form_model = "group"
    timeout_seconds = 60

    @staticmethod
    def is_displayed(player: Player):
        value = player.group.passed and not player.group.pass_displayed
        return value

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.group.pass_displayed = True

    @staticmethod
    def vars_for_template(player: Player):
        for p in player.group.get_players():
            if p.role() == "union":
                if p.vote == "Yes":
                    union = "For"
                else:
                    union = "Against"
            if p.role() == "gov":
                if p.vote == "Yes":
                    gov = "For"
                else:
                    gov = "Against"
            if p.role() == "dcr":
                if p.vote == "Yes":
                    dcr = "For"
                else:
                    dcr = "Against"
            if p.role() == "enviro":
                if p.vote == "Yes":
                    enviro = "For"
                else:
                    enviro = "Against"
            if p.role() == "ports":
                if p.vote == "Yes":
                    ports = "For"
                else:
                    ports = "Against"
        return {"union": union, "gov": gov, "ports": ports, "enviro": enviro, "dcr": dcr}


class Results_not_passed(Page):
    form_model = "group"
    timeout_seconds = 60

    @staticmethod
    def is_displayed(player: Player):
        value = player.group.did_not_pass and not player.group.vetoed
        return value

    @staticmethod
    def vars_for_template(player: Player):
        for p in player.group.get_players():
            if p.role() == "union":
                if p.vote == "Yes":
                    union = "For"
                else:
                    union = "Against"
            if p.role() == "gov":
                if p.vote == "Yes":
                    gov = "For"
                else:
                    gov = "Against"
            if p.role() == "dcr":
                if p.vote == "Yes":
                    dcr = "For"
                else:
                    dcr = "Against"
            if p.role() == "enviro":
                if p.vote == "Yes":
                    enviro = "For"
                else:
                    enviro = "Against"
            if p.role() == "ports":
                if p.vote == "Yes":
                    ports = "For"
                else:
                    ports = "Against"
        return {"union": union, "gov": gov, "ports": ports, "enviro": enviro, "dcr": dcr}


class Results_veto(Page):
    form_model = "group"
    timeout_seconds = 60

    @staticmethod
    def is_displayed(player: Player):
        return player.group.vetoed

    @staticmethod
    def vars_for_template(player: Player):
        for p in player.group.get_players():
            if p.role() == "union":
                if p.vote == "Yes":
                    union = "For"
                else:
                    union = "Against"
            if p.role() == "gov":
                if p.vote == "Yes":
                    gov = "For"
                else:
                    gov = "Against"
            if p.role() == "dcr":
                if p.vote == "Yes":
                    dcr = "For"
                else:
                    dcr = "Against"
            if p.role() == "enviro":
                if p.vote == "Yes":
                    enviro = "For"
                else:
                    enviro = "Against"
            if p.role() == "ports":
                if p.vote == "Yes":
                    ports = "For"
                else:
                    ports = "Against"
        return {"union": union, "gov": gov, "ports": ports, "enviro": enviro, "dcr": dcr}


class Timed_out(Page):
    form_model = 'group'

    @staticmethod
    def is_displayed(player: Player):
        return player.group.timed_out and not player.group.pass_displayed

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.group.pass_displayed = True


page_sequence = [
    New_round,
    Proposal,
    Proposal_wait,
    Vote,
    Tally,
    Results_high_pass,
    Results_pass,
    Results_not_passed,
    Results_veto,
    Timed_out,
]
