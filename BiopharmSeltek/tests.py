from otree.api import Currency as cu, currency_range
from . import *
from otree.api import Bot



class PlayerBot(Bot):
    """
    Bot player for automated testing of the BiopharmSeltek experiment.
    Inherits from oTree's Bot class to simulate player behavior during testing.
    """
    def play_round(self):
        """
        Define the bot's behavior for a single round of the experiment.
        This method should contain the sequence of actions the bot will take during one round.
        """
        pass
