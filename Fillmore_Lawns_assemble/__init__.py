import random
import time

from otree.api import *


author = 'Jon Atwell'
doc = """
Initializer for Fillmore Lawns
"""

with open("_rooms/Fillmore_Lawns_apx.txt", "r") as f:
    raw_string = f.read()
    party_names = raw_string.split("\n")



class C(BaseConstants):
    NAME_IN_URL = 'Assembling'
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 1
    STELLAR_COVE_RP =  32
    ILLIUM_RP = 55
    NPC_RP = 65
    BACKYARDS_RP = 50
    MAYOR_RP = 40
    GLC_RP = 51
    PARTY_NAMES = party_names

class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    section_labels = C.PARTY_NAMES.copy()
    for p, label in zip( subsession.get_players(),C.PARTY_NAMES):
        p.participant.label = label
        print(label)

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pass

class Assemble(WaitPage):

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": "Convening the meeting",
            "body_text": "We are waiting for all parties to log into the voting platform. You'll automatically advance once everyone has logged in.",
        }

    @staticmethod
    def after_all_players_arrive(group: Group):
        now = time.time()
        group.session.vars["first_vote_time"] = now + (group.session.config["first_vote_minutes"]*60)
        group.session.vars["second_vote_time"] = now + (group.session.config["second_vote_minutes"]*60)
        group.session.vars["third_vote_time"] = now + (group.session.config["third_vote_minutes"]*60)

page_sequence = [Assemble]
