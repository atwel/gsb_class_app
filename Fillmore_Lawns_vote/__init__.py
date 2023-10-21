import random
import time

from otree.api import *


author = 'Jon Atwell'
doc = """
Voting platform for Fillmore Lawns
"""


class C(BaseConstants):
    NAME_IN_URL = 'Voting'
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 3
    STELLAR_ROLE = "Stellar Cove"
    ILLIUM_ROLE = "Illium"
    NPC_ROLE = "NPC"
    BACKYARDS_ROLE = "Our Backyards"
    MAYOR_ROLE = "Mayor"
    GLC_ROLE = "GLC"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    mix = models.StringField(
        label="Property Mix (residential:commercial)",
        choices=["30:70", "50:50", "70:30"]
    )
    low_income = models.StringField(
        label="Low Income Residential",
        choices=["6%", "9%", "12%","15%"]
    )
    green = models.StringField(
        label="Green Space",
        choices=["14", "16", "18", "20"]
    )
    height = models.StringField(
        label="Maximum Building Height",
        choices=["400ft", "500ft", "600ft", "700ft", "800ft"]
    )
    venues = models.StringField(
        label="Entertainment complexes",
        choices=["0 venues", "1 venue", "2 venues", "3 venues", "4 venues"]
    )

    straw_prop = models.StringField(initial="0")
    straw_init = models.StringField(initial="No Current")
    straw_polls = models.StringField(initial="")
    straw_votes = models.StringField(initial="")

    passed = models.BooleanField(default=False)
    votes_for = models.IntegerField()

    first_vote = models.FloatField()
    second_vote = models.FloatField()
    third_vote = models.FloatField()
    our_round = models.IntegerField(initial=0)


class Player(BasePlayer):
    straw_votes = models.StringField(initial="")
    calc_props = models.StringField(initial="")
    straw_vote = models.BooleanField()
    straw_voted = models.BooleanField(initial=0)
    vote = models.StringField(
        choices=["Yes", "No"],
        label="Would you like to vote in favor of this proposal?")

    def vote_outcome(self):
        votes=[]
        vetoed=0
        for p in self.group.get_players():
            if p.role=="Stellar Cove":
                if p.straw_vote == 0:
                    vetoed=1 #veto power
                    votes.append(0)
                else:
                    votes.append(1)
            else:
                if p.straw_vote == 1:
                    votes.append(1)
                else:
                    votes.append(0)
        self.group.straw_votes += ("".join([str(i) for i in votes])+";")
        count_for = sum(votes)
        if count_for > 4 and not vetoed:
            return "1{}".format(count_for)
        else:
            return "2{}".format(count_for)


class Assemble(WaitPage):

    @staticmethod
    def after_all_players_arrive(group: Group):
        now = time.time()
        group.first_vote = now + 900
        group.second_vote = now + 2400
        group.third_vote = now + 4500
        group.our_round = 1

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": "Convening the meeting",
            "body_text": "We are waiting for all parties to log into the voting platform. You'll automatically advance once everyone has logged in.",
        }

class Calculator(Page):
    form_model = "player"
    timer_text = "Time until the next official vote:"

    @staticmethod
    def get_timeout_seconds(player):
        if player.group.our_round == 1:
            return player.group.first_vote - time.time()
        elif player.group.our_round == 2:
            return player.group.second_vote - time.time()
        else:
            print(player.group.our_round)
            return player.group.third_vote - time.time()

    @staticmethod
    def live_method(player, data):
        """
        There is only a single live_method() call so I've come up with a system for
        sending and parsing different types. It gets encoded and decoded on the client
        side with switch functions.

        The basic response is a string of numbers, e.g.
        0;23214;90aoeustnhstnh;182508092409;
        A;BCDEFG;X;Z

        A - the message type
          - 1: Calculator change
          - 2: Straw poll initiation
          - 3: Straw poll vote
        B - The "Max Building Height" issue level
          - 0: undefined
          - 1: 400ft
          - 2: 500ft
          - 3: 600ft
          - 4: 700ft
          - 5: 800ft
        C - The "Entertainment Venue" issue level
          - 0: undefined
          - 1: 0 venues
          - 2: 1 venue
          - 3: 2 venues
          - 4: 3 venues
          - 5: 4 venues
        D - The "Green Space" issue level
          - 0: undefined
          - 1: 14 acres
          - 2: 16 acres
          - 3: 18 acres
          - 4: 20 acres
        E - The "Low Income" issue level
          - 0: undefined
          - 1: 6%
          - 2: 9%
          - 3: 12%
          - 4: 15%
        F - The "Property Mix" issue level
          - 0: undefined
          - 1: 30:70
          - 2: 50:50
          - 3: 70:30
        G - Straw poll vote
          - 0: oppose
          - 1: support
        X - cookie (to uniquely identify people incase if multiple people log into the same role)
        Z - The UNIX epoch time stamp
        """
        if data[0] == "1":
            # A calculator change
            # data[1:] is the string of issue levels
            props_str = player.calc_props # all previous proposals
            player.calc_props = props_str + "," + data[2:] # adding the new proposal and time stamp
        elif data[0]== "2":
            # An incoming straw proposal
            prop = data[2:7]
            # The return sends the proposal out to everyone, including who proposed it.
            for p in player.get_others_in_group():
                p.straw_voted = 0
                p.straw_vote = 0
            player.group.straw_prop = prop
            player.group.straw_init = player.role + "'s"
            player.group.straw_polls += (data[2:]+";")
            return {0: "2" + prop + player.role}
        else:
            # An incoming straw poll vote
            proposal = data[2:7]
            vote = data[8]
            if not player.straw_voted:
                player.straw_vote = int(vote)
                player.straw_voted = 1
            if all([p.straw_voted for p in player.get_others_in_group()]):
                return {0: "3" + str(player.vote_outcome())}

    def vars_for_template(player: Player):
        return {"straw_prop": player.group.straw_prop, "straw_init": player.group.straw_init, "mix_1": "23", "mix_2": "9", "mix_3": "0"}




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
    form_fields = ["height", "venues", "green", "low_income", "mix"]

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.STELLAR_ROLE


class Proposal_wait(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.role != C.STELLAR_ROLE

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": "Voting",
            "body_text": "Please wait while Stellar Cove enters a proposal for you to vote on.",
        }

class Vote(Page):
    form_model = "player"
    form_fields = ["vote"]

    @staticmethod
    def is_displayed(player: Player):
        return player.role != C.STELLAR_ROLE

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "green": player.group.green.lower(),
            "mix": player.group.mix.lower(),
            "height": player.group.height.lower(),
            "venues": player.group.venues.lower(),
            "low_income": player.group.low_income.lower(),
        }

class Tally(WaitPage):

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": "Waiting for all votes to be cast.",
            "body_text": "Other parties are still voting. Once votes are in and tallied, the results will be shown.",
        }

    @staticmethod
    def after_all_players_arrive(group: Group):
            votes = [1]
            for p in group.get_players():
                if p.role != C.STELLAR_ROLE:
                    if p.vote == "Yes":
                        votes.append(1)
                    else:
                        votes.append(0)

            total_for = sum(votes)
            group.votes_for = total_for
            if total_for > 4:
                group.passed = True
            else:
                group.passed = False

class Results(Page):
    form_model = "group"
    timeout_seconds = 60


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.group.pass_displayed = True

    @staticmethod
    def vars_for_template(player: Player):
        if player.group.passed == True:
            return {"outcome": "passed"}

page_sequence = [Assemble, Calculator, Proposal, Proposal_wait, Vote, Tally, Results]
#, Vote, Calculator, Vote, Calculator, Vote]#
#Assemble,
#    Welcome,
#    New_round,
#    Proposal,
#    Proposal_wait,
#    Vote,
#    Tally,
#    Results_high_pass,
#    Results_pass,
#    Results_not_passed,
#    Results_veto,
#    Timed_out,
#]
