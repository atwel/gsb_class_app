import random

from otree.api import *


author = 'Jon Atwell'
doc = """
Negotating Fillmore Lawns
"""


class C(BaseConstants):
    NAME_IN_URL = 'Fillmore_Lawns'
    PLAYERS_PER_GROUP = 6
    STANFORD_VERSION = False
    NUM_ROUNDS = 1
    CLASSCODE = 190881
    PLANNING_ASSIGNMENT_CODE = 610705
    STELLAR_COVE_RP =  32
    ILLIUM_RP = 55
    NPC_RP = 65
    BACKYARDS_RP = 50
    MAYOR_RP = 40
    GLC_RP = 51


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    calc_props = models.StringField(initial="")
    name = models.StringField(label="First and last name")


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
class GetName(Page):
    form_model = 'player'
    form_fields = ["name"]
    


class Introduction(Page):
    form_model = "player"


class Stellar_Cove(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "Stellar_Cove"

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
            pass

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Fillmore_Lawns/Stellar Cove.pdf",
                     "assignment_url": "/{}/assignments/{}".format(C.CLASSCODE, C.PLANNING_ASSIGNMENT_CODE),
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
                      "venue_5": "19"}


class Green_Living(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "Green_Living"

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
            pass

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Fillmore_Lawns/Green Living Collective.pdf",
                  "my_name": "Green Living",
                  "assignment_url": "/{}/assignments/{}".format(C.CLASSCODE, C.PLANNING_ASSIGNMENT_CODE),
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


class Illium(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "Illium"

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
            pass

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Fillmore_Lawns/Illium Group.pdf",
                  "assignment_url": "/{}/assignments/{}".format(C.CLASSCODE, C.PLANNING_ASSIGNMENT_CODE),
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


class Mayor_Gabriel(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "Mayor_Gabriel"

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
            pass

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Fillmore_Lawns/Mayor Gabriel.pdf",
                 "assignment_url": "/{}/assignments/{}".format(C.CLASSCODE, C.PLANNING_ASSIGNMENT_CODE),
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


class Our_Backyards(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "Our_Backyards"

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
            pass

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Fillmore_Lawns/Our Backyards.pdf",
                  "assignment_url": "/{}/assignments/{}".format(C.CLASSCODE, C.PLANNING_ASSIGNMENT_CODE),
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


class Planning_Commission(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "Planning_Commission"

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
            pass

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Fillmore_Lawns/Newpoint Planning Commission.pdf",
                  "assignment_url": "/{}/assignments/{}".format(C.CLASSCODE, C.PLANNING_ASSIGNMENT_CODE),
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



page_sequence = [GetName,Introduction,
    Stellar_Cove,
    Green_Living,
    Illium,
    Mayor_Gabriel,
    Our_Backyards,
    Planning_Commission,
]
