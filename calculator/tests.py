from otree.api import Currency as cu, currency_range
from . import *
from otree.api import Bot



class PlayerBot(Bot):
    """
    Test bot that simulates player behavior for automated testing.
    Inherits from oTree's Bot class to run through game scenarios.
    """
    def play_round(self):
        pass
