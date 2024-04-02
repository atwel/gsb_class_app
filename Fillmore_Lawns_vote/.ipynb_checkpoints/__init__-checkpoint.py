import random
import time

from otree.api import *


author = 'Jon Atwell'
doc = """
Calculator and vote taker for Fillmore Lawns
"""

class C(BaseConstants):
    NAME_IN_URL = 'Voting'
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 3
    STELLAR_COVE_RP =  32
    ILLIUM_RP = 55
    NPC_RP = 65
    BACKYARDS_RP = 50
    MAYOR_RP = 40
    GLC_RP = 51

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    mix = models.StringField(
        choices=["30:70", "50:50", "70:30"],
        default="30:70"
    )
    low_income = models.StringField(
        choices=["6", "9", "12","15"],
        default="6"
    )
    green = models.StringField(
        choices=["14", "16", "18", "20"],
        default="14"
    )
    height = models.StringField(
        choices=["400", "500", "600", "700", "800"],
        default="800"
    )
    venues = models.StringField(
        choices=["0", "1", "2", "3", "4"],
        default="4"
    )

    straw_prop = models.StringField(initial="0")
    straw_init = models.StringField(initial="None")
    straw_polls = models.StringField(initial="")
    straw_votes = models.StringField(initial="")

    proposal_timeout = models.BooleanField()
    passed = models.BooleanField(default=False)
    votes_for = models.StringField()
    votes_against = models.StringField()
    votes_for_count = models.IntegerField()

class Player(BasePlayer):
    straw_votes = models.StringField(initial="")
    calc_props = models.StringField(initial="")
    straw_vote = models.BooleanField()
    straw_voted = models.BooleanField(initial=0)

    vote_timeout = models.BooleanField(default=0)
    vote = models.BooleanField(default=0)


    def vote_outcome(self):
        votes_for=[]
        votes_against=[]
        vetoed=0
        for p in self.group.get_players():
            if p.participant.label=="Stellar_Cove":
                if p.straw_vote == 0:
                    vetoed=1 #veto power
                    votes_against.append(p.participant.label)
                else:
                    votes_for.append(p.participant.label)
            else:
                if p.straw_vote == 1:
                    votes_for.append(p.participant.label)
                else:
                    votes_against.append(p.participant.label)
        self.group.straw_votes += (",".join(votes_for)+";")

        return "3<strong>For:</strong> {}<br><strong>Against</strong>: {}".format(", ".join(votes_for),", ".join(votes_against))

class Calculator(Page):
    form_model = "player"
    timer_text = "Time until an official vote:"

    @staticmethod
    def get_timeout_seconds(player):
        if player.round_number == 1:
            return player.session.vars["first_vote_time"] - time.time()
        elif player.round_number == 2:
            return player.session.vars["second_vote_time"] - time.time()
        else:
            return player.session.vars["third_vote_time"] - time.time()

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
            for p in player.group.get_players():
                p.straw_voted = 0
                p.straw_vote = 0
            player.group.straw_prop = prop
            player.group.straw_init = player.participant.label
            player.group.straw_polls += (data[2:]+";")
            return {0: "2" + prop + player.participant.label.replace("_", " ")}
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

        if(player.participant.label=="Stellar_Cove"):
            return {"straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
            "my_name": "Stellar Cove",
            "my_rp": C.STELLAR_COVE_RP,
            "mix_1": "23",
            "mix_2": "9",
            "mix_3": "0",
            "li_1": "11",
            "li_2": "8",
            "li_3": "4",
            "li_4": "0",
            "green_1": "17",
            "green_2": "11",
            "green_3": "8",
            "green_4": "0",
            "height_1": "0",
            "height_2": "0",
            "height_3": "10",
            "height_4": "20",
            "height_5": "30",
            "venue_1": "0",
            "venue_2": "5",
            "venue_3": "11",
            "venue_4": "14",
            "venue_5": "19"
            }

        if (player.participant.label == "Green_Living"):
            return {"straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
            "my_name": "Green Living",
            "my_rp": C.GLC_RP,
            "mix_1": "0",
            "mix_2": "10",
            "mix_3": "20",
            "li_1": "0",
            "li_2": "5",
            "li_3": "20",
            "li_4": "25",
            "green_1": "0",
            "green_2": "10",
            "green_3": "15",
            "green_4": "35",
            "height_1": "15",
            "height_2": "10",
            "height_3": "5",
            "height_4": "0",
            "height_5": "0",
            "venue_1": "5",
            "venue_2": "5",
            "venue_3": "5",
            "venue_4": "0",
            "venue_5": "0"
            }

        if (player.participant.label=="Illium"):
             return {"straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
            "my_name": "Illium",
            "my_rp": C.ILLIUM_RP,
            "mix_1": "0",
            "mix_2": "5",
            "mix_3": "10",
            "li_1": "0",
            "li_2": "5",
            "li_3": "10",
            "li_4": "15",
            "green_1": "0",
            "green_2": "4",
            "green_3": "10",
            "green_4": "15",
            "height_1": "25",
            "height_2": "15",
            "height_3": "10",
            "height_4": "5",
            "height_5": "0",
            "venue_1": "35",
            "venue_2": "20",
            "venue_3": "20",
            "venue_4": "0",
            "venue_5": "0"
            }

        if (player.participant.label=="Mayor_Gabriel"):

            return {"straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
            "my_name": "Mayor Gabriel",
            "my_rp": C.MAYOR_RP,
            "mix_1": "21",
            "mix_2": "10",
            "mix_3": "0",
            "li_1": "0",
            "li_2": "2",
            "li_3": "4",
            "li_4": "10",
            "green_1": "30",
            "green_2": "20",
            "green_3": "9",
            "green_4": "0",
            "height_1": "0",
            "height_2": "5",
            "height_3": "10",
            "height_4": "15",
            "height_5": "25",
            "venue_1": "0",
            "venue_2": "5",
            "venue_3": "6",
            "venue_4": "9",
            "venue_5": "14"
            }

        if (player.participant.label=="Our_Backyards"):
             return {"straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
            "my_name": "Our Backyards",
            "my_rp": C.BACKYARDS_RP,
            "mix_1": "0",
            "mix_2": "13",
            "mix_3": "6",
            "li_1": "9",
            "li_2": "6",
            "li_3": "3",
            "li_4": "0",
            "green_1": "0",
            "green_2": "8",
            "green_3": "16",
            "green_4": "24",
            "height_1": "38",
            "height_2": "20",
            "height_3": "10",
            "height_4": "0",
            "height_5": "0",
            "venue_1": "4",
            "venue_2": "12",
            "venue_3": "16",
            "venue_4": "8",
            "venue_5": "0"
            }

        if (player.participant.label=="Planning_Commission"):
             return {"straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
            "my_name": "Planning Commission",
            "my_rp": C.NPC_RP,
            "mix_1": "0",
            "mix_2": "20",
            "mix_3": "10",
            "li_1": "0",
            "li_2": "15",
            "li_3": "15",
            "li_4": "0",
            "green_1": "0",
            "green_2": "20",
            "green_3": "30",
            "green_4": "0",
            "height_1": "0",
            "height_2": "20",
            "height_3": "15",
            "height_4": "5",
            "height_5": "5",
            "venue_1": "0",
            "venue_2": "15",
            "venue_3": "15",
            "venue_4": "15",
            "venue_5": "0"
            }

        else:
            pass

class Proposal(Page):
    form_model = "group"
    form_fields = ["mix", "low_income", "green", "height", "venues" ]
    timer_text = "Time to finish crafting a proposal:"

    @staticmethod
    def get_timeout_seconds(player):
        return player.session.config["propose_time"] *60

    @staticmethod
    def vars_for_template(player: Player):
        return {
        "my_name": "Stellar Cove",
        "my_rp": C.STELLAR_COVE_RP,
        "mix_1": "23",
        "mix_2": "9",
        "mix_3": "0",
        "li_1": "11",
        "li_2": "8",
        "li_3": "4",
        "li_4": "0",
        "green_1": "17",
        "green_2": "11",
        "green_3": "8",
        "green_4": "0",
        "height_1": "0",
        "height_2": "0",
        "height_3": "10",
        "height_4": "20",
        "height_5": "30",
        "venue_1": "0",
        "venue_2": "5",
        "venue_3": "11",
        "venue_4": "14",
        "venue_5": "19"
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.label == "Stellar_Cove"

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.group.proposal_timeout = True
            if player.group.mix == "":
                player.group.mix = "30:70"
            if player.group.green == "":
                player.group.green = "14"
            if player.group.height == "":
                player.group.height = "800"
            if player.group.low_income == "":
                player.group.low_income = "6"
            if player.group.venues == "":
                player.group.venues = "4"
        else:
            player.group.proposal_timeout = False

class Proposal_wait(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.label != "Stellar_Cove"

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": "Voting",
            "body_text": "Please wait while Stellar Cove enters a proposal for you to vote on.",
        }

class Vote(Page):
    form_model = "player"
    form_fields = ["vote"]
    timer_text = "Time to finish voting:"

    @staticmethod
    def get_timeout_seconds(player):
        return player.session.config["vote_time"] *60

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
        else:
            print("calc tracking is not right")

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.label != "Stellar_Cove"

    def vars_for_template(player: Player):

        if (player.participant.label == "Green_Living"):
            return {
            "green": player.group.green.lower(),
            "mix": player.group.mix.lower(),
            "height": player.group.height.lower(),
            "venues": player.group.venues.lower(),
            "low_income": player.group.low_income.lower(),
            "my_name": "Green Living",
            "my_rp": C.GLC_RP,
            "mix_1": "0",
            "mix_2": "10",
            "mix_3": "20",
            "li_1": "0",
            "li_2": "5",
            "li_3": "20",
            "li_4": "25",
            "green_1": "0",
            "green_2": "10",
            "green_3": "15",
            "green_4": "35",
            "height_1": "15",
            "height_2": "10",
            "height_3": "5",
            "height_4": "0",
            "height_5": "0",
            "venue_1": "5",
            "venue_2": "5",
            "venue_3": "5",
            "venue_4": "0",
            "venue_5": "0"
            }

        if (player.participant.label =="Illium"):
             return {
             "green": player.group.green.lower(),
             "mix": player.group.mix.lower(),
             "height": player.group.height.lower(),
             "venues": player.group.venues.lower(),
             "low_income": player.group.low_income.lower(),
            "my_name": "Illium",
            "my_rp": C.ILLIUM_RP,
            "mix_1": "0",
            "mix_2": "5",
            "mix_3": "10",
            "li_1": "0",
            "li_2": "5",
            "li_3": "10",
            "li_4": "15",
            "green_1": "0",
            "green_2": "4",
            "green_3": "10",
            "green_4": "15",
            "height_1": "25",
            "height_2": "15",
            "height_3": "10",
            "height_4": "5",
            "height_5": "0",
            "venue_1": "35",
            "venue_2": "20",
            "venue_3": "20",
            "venue_4": "0",
            "venue_5": "0"
            }

        if (player.participant.label =="Mayor_Gabriel"):

            return {
            "green": player.group.green.lower(),
            "mix": player.group.mix.lower(),
            "height": player.group.height.lower(),
            "venues": player.group.venues.lower(),
            "low_income": player.group.low_income.lower(),
            "my_name": "Mayor Gabriel",
            "my_rp": C.MAYOR_RP,
            "mix_1": "21",
            "mix_2": "10",
            "mix_3": "0",
            "li_1": "0",
            "li_2": "2",
            "li_3": "4",
            "li_4": "10",
            "green_1": "30",
            "green_2": "20",
            "green_3": "9",
            "green_4": "0",
            "height_1": "0",
            "height_2": "5",
            "height_3": "10",
            "height_4": "15",
            "height_5": "25",
            "venue_1": "0",
            "venue_2": "5",
            "venue_3": "6",
            "venue_4": "9",
            "venue_5": "14"
            }

        if (player.participant.label=="Our_Backyards"):
             return {
             "green": player.group.green.lower(),
             "mix": player.group.mix.lower(),
             "height": player.group.height.lower(),
             "venues": player.group.venues.lower(),
             "low_income": player.group.low_income.lower(),
            "my_name": "Our Backyards",
            "my_rp": C.BACKYARDS_RP,
            "mix_1": "0",
            "mix_2": "13",
            "mix_3": "6",
            "li_1": "9",
            "li_2": "6",
            "li_3": "3",
            "li_4": "0",
            "green_1": "0",
            "green_2": "8",
            "green_3": "16",
            "green_4": "24",
            "height_1": "38",
            "height_2": "20",
            "height_3": "10",
            "height_4": "0",
            "height_5": "0",
            "venue_1": "4",
            "venue_2": "12",
            "venue_3": "16",
            "venue_4": "8",
            "venue_5": "0"
            }

        if (player.participant.label=="Planning_Commission"):
             return {
             "green": player.group.green.lower(),
             "mix": player.group.mix.lower(),
             "height": player.group.height.lower(),
             "venues": player.group.venues.lower(),
             "low_income": player.group.low_income.lower(),
            "my_name": "Planning Commission",
            "my_rp": C.NPC_RP,
            "mix_1": "0",
            "mix_2": "20",
            "mix_3": "10",
            "li_1": "0",
            "li_2": "15",
            "li_3": "15",
            "li_4": "0",
            "green_1": "0",
            "green_2": "20",
            "green_3": "30",
            "green_4": "0",
            "height_1": "0",
            "height_2": "20",
            "height_3": "15",
            "height_4": "5",
            "height_5": "5",
            "venue_1": "0",
            "venue_2": "15",
            "venue_3": "15",
            "venue_4": "15",
            "venue_5": "0"
            }


        else:
            pass

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.vote_timeout = True

class Tally(WaitPage):

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": "Waiting for all votes to be cast.",
            "body_text": "Other parties are still voting. Once votes are in and tallied, the results will be shown.",
        }

    @staticmethod
    def after_all_players_arrive(group: Group):
            votes_for = ["Stellar Cove"]
            votes_against = []
            for p in group.get_players():
                if p.participant.label != "Stellar_Cove":
                    if p.vote == 1:
                        votes_for.append(p.participant.label)
                    else:
                        votes_against.append(p.participant.label)

            total_for = len(votes_for)
            group.votes_for = ", ".join(votes_for)
            group.votes_for_count = total_for
            group.votes_against = ", ".join(votes_against)

            if total_for > 4:
                group.passed = True
            else:
                group.passed = False

class Results(Page):
    form_model = "group"
    timeout_seconds = 60

    @staticmethod
    def vars_for_template(player: Player):
        if player.group.passed == True:
            against_round = player.group.votes_against
            if against_round == "":
                against_round = "No one"
            return {"for_votes":player.group.votes_for,
                         "against": against_round}
        else:
            return {"outcome": player.group.votes_for_count}

    @staticmethod
    def app_after_this_page(player, upcoming_apps):

        if player.group.passed:
            return "Fillmore_Lawns_end"

page_sequence = [Calculator, Proposal, Proposal_wait, Vote, Tally, Results]
