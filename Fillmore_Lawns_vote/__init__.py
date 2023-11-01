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
    vote2 = models.StringField(
        choices=["Yes", "No"],
        label="Would you like to vote in favor of this proposal?")
    vote3 = models.StringField(
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
    timer_text = "Time until the first official vote:"

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

#updated below

    def vars_for_template(player: Player):
        print(f"Player role: {player.role}")

        if(player.role=="Stellar Cove"):
            return {"straw_prop": player.group.straw_prop
            , "straw_init": player.group.straw_init,

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

        if (player.role == "GLC"):
            print(77777777777777777777777777777777)  # ############# test
            return {"straw_prop": player.group.straw_prop
            , "straw_init": player.group.straw_init,

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

        if (player.role=="Illium"):
             return {"straw_prop": player.group.straw_prop
            , "straw_init": player.group.straw_init,

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
        if (player.role=="Mayor"):

            return {"straw_prop": player.group.straw_prop
            , "straw_init": player.group.straw_init,

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

        if (player.role=="Our Backyards"):
             return {"straw_prop": player.group.straw_prop
            , "straw_init": player.group.straw_init,

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

        if (player.role=="NPC"):
             return {"straw_prop": player.group.straw_prop
            , "straw_init": player.group.straw_init,

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
            return {
            "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,

            "mix_1": "0",
            "mix_2": "0",
            "mix_3": "0",
            "li_1": "0",
            "li_2": "0",
            "li_3": "0",
            "li_4": "0",
            "green_1": "0",
            "green_2": "0",
            "green_3": "0",
            "green_4": "0",
            "height_1": "0",
            "height_2": "0",
            "height_3": "0",
            "height_4": "0",
            "height_5": "0",
            "venue_1": "0",
            "venue_2": "0",
            "venue_3": "0",
            "venue_4": "0",
            "venue_5": "0"
            }

class Calculator2(Page):
    form_model = "player"
    timer_text = "Time until the second official vote:"

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

#updated below

    def vars_for_template(player: Player):
        print(f"Player role: {player.role}")

        if(player.role=="Stellar Cove"):
            return {"straw_prop": player.group.straw_prop
            , "straw_init": player.group.straw_init,

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

        if (player.role == "GLC"):
            print(77777777777777777777777777777777)  # ############# test
            return {"straw_prop": player.group.straw_prop
            , "straw_init": player.group.straw_init,

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

        if (player.role=="Illium"):
             return {"straw_prop": player.group.straw_prop
            , "straw_init": player.group.straw_init,

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
        if (player.role=="Mayor"):

            return {"straw_prop": player.group.straw_prop
            , "straw_init": player.group.straw_init,

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

        if (player.role=="Our Backyards"):
             return {"straw_prop": player.group.straw_prop
            , "straw_init": player.group.straw_init,

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

        if (player.role=="NPC"):
             return {"straw_prop": player.group.straw_prop
            , "straw_init": player.group.straw_init,

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
            return {
            "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,

            "mix_1": "0",
            "mix_2": "0",
            "mix_3": "0",
            "li_1": "0",
            "li_2": "0",
            "li_3": "0",
            "li_4": "0",
            "green_1": "0",
            "green_2": "0",
            "green_3": "0",
            "green_4": "0",
            "height_1": "0",
            "height_2": "0",
            "height_3": "0",
            "height_4": "0",
            "height_5": "0",
            "venue_1": "0",
            "venue_2": "0",
            "venue_3": "0",
            "venue_4": "0",
            "venue_5": "0"
            }

class Calculator3(Page):
    form_model = "player"
    timer_text = "Time until the third official vote:"

    @staticmethod
    def get_timeout_seconds(player):
        if player.group.our_round == 1:
            return player.group.first_vote - time.time()
        elif player.group.our_round == 2:
            return player.group.second_vote - time.time()
        elif player.group.our_round == 3:
            print(player.group.our_round)
            return player.group.third_vote - time.time()
        else:
            print("error")

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

#updated below

    def vars_for_template(player: Player):
        print(f"Player role: {player.role}")

        if(player.role=="Stellar Cove"):
            return {"straw_prop": player.group.straw_prop
            , "straw_init": player.group.straw_init,

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

        if (player.role == "GLC"):
            print(77777777777777777777777777777777)  # ############# test
            return {"straw_prop": player.group.straw_prop
            , "straw_init": player.group.straw_init,

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

        if (player.role=="Illium"):
             return {"straw_prop": player.group.straw_prop
            , "straw_init": player.group.straw_init,

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
        if (player.role=="Mayor"):

            return {"straw_prop": player.group.straw_prop
            , "straw_init": player.group.straw_init,

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

        if (player.role=="Our Backyards"):
             return {"straw_prop": player.group.straw_prop
            , "straw_init": player.group.straw_init,

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

        if (player.role=="NPC"):
             return {"straw_prop": player.group.straw_prop
            , "straw_init": player.group.straw_init,

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
            return {
            "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,

            "mix_1": "0",
            "mix_2": "0",
            "mix_3": "0",
            "li_1": "0",
            "li_2": "0",
            "li_3": "0",
            "li_4": "0",
            "green_1": "0",
            "green_2": "0",
            "green_3": "0",
            "green_4": "0",
            "height_1": "0",
            "height_2": "0",
            "height_3": "0",
            "height_4": "0",
            "height_5": "0",
            "venue_1": "0",
            "venue_2": "0",
            "venue_3": "0",
            "venue_4": "0",
            "venue_5": "0"
            }

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
        return player.role != C.STELLAR_ROLE


    def vars_for_template(player: Player):
        if(player.role=="Stellar Cove"):
            return {
            "green": player.group.green.lower(),
            "mix": player.group.mix.lower(),
            "height": player.group.height.lower(),
            "venues": player.group.venues.lower(),
            "low_income": player.group.low_income.lower(),
            "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
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

        if (player.role == "GLC"):
            return {
            "green": player.group.green.lower(),
            "mix": player.group.mix.lower(),
            "height": player.group.height.lower(),
            "venues": player.group.venues.lower(),
            "low_income": player.group.low_income.lower(),
            "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
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

        if (player.role=="Illium"):
             return {
             "green": player.group.green.lower(),
             "mix": player.group.mix.lower(),
             "height": player.group.height.lower(),
             "venues": player.group.venues.lower(),
             "low_income": player.group.low_income.lower(),
             "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
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
        if (player.role=="Mayor"):

            return {
            "green": player.group.green.lower(),
            "mix": player.group.mix.lower(),
            "height": player.group.height.lower(),
            "venues": player.group.venues.lower(),
            "low_income": player.group.low_income.lower(),
            "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
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

        if (player.role=="Our Backyards"):
             return {
             "green": player.group.green.lower(),
             "mix": player.group.mix.lower(),
             "height": player.group.height.lower(),
             "venues": player.group.venues.lower(),
             "low_income": player.group.low_income.lower(),
             "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
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

        if (player.role=="NPC"):
             return {
             "green": player.group.green.lower(),
             "mix": player.group.mix.lower(),
             "height": player.group.height.lower(),
             "venues": player.group.venues.lower(),
             "low_income": player.group.low_income.lower(),
             "straw_prop": player.group.straw_prop,
             "straw_init": player.group.straw_init,
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
            return {
            "green": player.group.green.lower(),
            "mix": player.group.mix.lower(),
            "height": player.group.height.lower(),
            "venues": player.group.venues.lower(),
            "low_income": player.group.low_income.lower(),
            "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
            "mix_1": "0",
            "mix_2": "0",
            "mix_3": "0",
            "li_1": "0",
            "li_2": "0",
            "li_3": "0",
            "li_4": "0",
            "green_1": "0",
            "green_2": "0",
            "green_3": "0",
            "green_4": "0",
            "height_1": "0",
            "height_2": "0",
            "height_3": "0",
            "height_4": "0",
            "height_5": "0",
            "venue_1": "0",
            "venue_2": "0",
            "venue_3": "0",
            "venue_4": "0",
            "venue_5": "0"
            }

class Vote2(Page):
    form_model = "player"
    form_fields = ["vote2"]

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
        return player.role != C.STELLAR_ROLE


    def vars_for_template(player: Player):
        if(player.role=="Stellar Cove"):
            return {
            "green": player.group.green.lower(),
            "mix": player.group.mix.lower(),
            "height": player.group.height.lower(),
            "venues": player.group.venues.lower(),
            "low_income": player.group.low_income.lower(),
            "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
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

        if (player.role == "GLC"):
            return {
            "green": player.group.green.lower(),
            "mix": player.group.mix.lower(),
            "height": player.group.height.lower(),
            "venues": player.group.venues.lower(),
            "low_income": player.group.low_income.lower(),
            "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
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

        if (player.role=="Illium"):
             return {
             "green": player.group.green.lower(),
             "mix": player.group.mix.lower(),
             "height": player.group.height.lower(),
             "venues": player.group.venues.lower(),
             "low_income": player.group.low_income.lower(),
             "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
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
        if (player.role=="Mayor"):

            return {
            "green": player.group.green.lower(),
            "mix": player.group.mix.lower(),
            "height": player.group.height.lower(),
            "venues": player.group.venues.lower(),
            "low_income": player.group.low_income.lower(),
            "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
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

        if (player.role=="Our Backyards"):
             return {
             "green": player.group.green.lower(),
             "mix": player.group.mix.lower(),
             "height": player.group.height.lower(),
             "venues": player.group.venues.lower(),
             "low_income": player.group.low_income.lower(),
             "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
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

        if (player.role=="NPC"):
             return {
             "green": player.group.green.lower(),
             "mix": player.group.mix.lower(),
             "height": player.group.height.lower(),
             "venues": player.group.venues.lower(),
             "low_income": player.group.low_income.lower(),
             "straw_prop": player.group.straw_prop,
             "straw_init": player.group.straw_init,
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
            return {
            "green": player.group.green.lower(),
            "mix": player.group.mix.lower(),
            "height": player.group.height.lower(),
            "venues": player.group.venues.lower(),
            "low_income": player.group.low_income.lower(),
            "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
            "mix_1": "0",
            "mix_2": "0",
            "mix_3": "0",
            "li_1": "0",
            "li_2": "0",
            "li_3": "0",
            "li_4": "0",
            "green_1": "0",
            "green_2": "0",
            "green_3": "0",
            "green_4": "0",
            "height_1": "0",
            "height_2": "0",
            "height_3": "0",
            "height_4": "0",
            "height_5": "0",
            "venue_1": "0",
            "venue_2": "0",
            "venue_3": "0",
            "venue_4": "0",
            "venue_5": "0"
            }

class Vote3(Page):
    form_model = "player"
    form_fields = ["vote3"]

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
        return player.role != C.STELLAR_ROLE


    def vars_for_template(player: Player):
        if(player.role=="Stellar Cove"):
            return {
            "green": player.group.green.lower(),
            "mix": player.group.mix.lower(),
            "height": player.group.height.lower(),
            "venues": player.group.venues.lower(),
            "low_income": player.group.low_income.lower(),
            "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
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

        if (player.role == "GLC"):
            return {
            "green": player.group.green.lower(),
            "mix": player.group.mix.lower(),
            "height": player.group.height.lower(),
            "venues": player.group.venues.lower(),
            "low_income": player.group.low_income.lower(),
            "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
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

        if (player.role=="Illium"):
             return {
             "green": player.group.green.lower(),
             "mix": player.group.mix.lower(),
             "height": player.group.height.lower(),
             "venues": player.group.venues.lower(),
             "low_income": player.group.low_income.lower(),
             "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
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
        if (player.role=="Mayor"):

            return {
            "green": player.group.green.lower(),
            "mix": player.group.mix.lower(),
            "height": player.group.height.lower(),
            "venues": player.group.venues.lower(),
            "low_income": player.group.low_income.lower(),
            "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
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

        if (player.role=="Our Backyards"):
             return {
             "green": player.group.green.lower(),
             "mix": player.group.mix.lower(),
             "height": player.group.height.lower(),
             "venues": player.group.venues.lower(),
             "low_income": player.group.low_income.lower(),
             "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
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

        if (player.role=="NPC"):
             return {
             "green": player.group.green.lower(),
             "mix": player.group.mix.lower(),
             "height": player.group.height.lower(),
             "venues": player.group.venues.lower(),
             "low_income": player.group.low_income.lower(),
             "straw_prop": player.group.straw_prop,
             "straw_init": player.group.straw_init,
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
            return {
            "green": player.group.green.lower(),
            "mix": player.group.mix.lower(),
            "height": player.group.height.lower(),
            "venues": player.group.venues.lower(),
            "low_income": player.group.low_income.lower(),
            "straw_prop": player.group.straw_prop,
            "straw_init": player.group.straw_init,
            "mix_1": "0",
            "mix_2": "0",
            "mix_3": "0",
            "li_1": "0",
            "li_2": "0",
            "li_3": "0",
            "li_4": "0",
            "green_1": "0",
            "green_2": "0",
            "green_3": "0",
            "green_4": "0",
            "height_1": "0",
            "height_2": "0",
            "height_3": "0",
            "height_4": "0",
            "height_5": "0",
            "venue_1": "0",
            "venue_2": "0",
            "venue_3": "0",
            "venue_4": "0",
            "venue_5": "0"
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
                else:
                    group.our_round +=1

            total_for = sum(votes)
            group.votes_for = total_for
            if total_for > 4:
                group.passed = True
                group.first_vote = True
            else:
                group.passed = False
                group.first_vote = False

class Tally2(WaitPage):

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
                    if p.vote2 == "Yes":
                        votes.append(1)
                    else:
                        votes.append(0)

            total_for = sum(votes)
            group.votes_for = total_for
            if total_for > 4:
                group.passed = True
                group.second_vote = True
            else:
                group.passed = False
                group.second_vote = False

class Tally3(WaitPage):

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
                    if p.vote3 == "Yes":
                        votes.append(1)
                    else:
                        votes.append(0)

            total_for = sum(votes)
            group.votes_for = total_for
            if total_for > 4:
                group.passed = True
                group.third_vote = True
            else:
                group.passed = False
                group.third_vote = False

class Results(Page):
    form_model = "group"
    timeout_seconds = 60

    @staticmethod
    def vars_for_template(player: Player):
        if player.group.passed == True:
            return {"outcome": "passed"}
        else:
            return {"outcome": "did not pass"}

page_sequence = [Assemble, Calculator, Proposal, Proposal_wait, Vote, Tally, Results,Calculator2, Proposal, Proposal_wait, Vote2, Tally2, Results,Calculator3, Proposal, Proposal_wait, Vote3, Tally3, Results]
