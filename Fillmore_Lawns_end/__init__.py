import random
import time

from otree.api import *


author = 'Jon Atwell'
doc = "Sign off for Fillmore Lawns"

class C(BaseConstants):
    NAME_IN_URL = 'Exit'
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pass

class Goodbye(Page):
    pass

page_sequence = [Goodbye]
