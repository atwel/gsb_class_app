from otree.api import Currency as cu, currency_range
from . import *
from otree.api import Bot



class PlayerBot(Bot):
    """
    Automated bot for testing the HarborCo voting game.
    This bot simulates player behavior during game rounds for automated testing purposes.
    """
    def play_round(self):
        """
        Define the bot's behavior for a single round of the game.
        This method should contain the sequence of actions the bot will take during one round.
        """
        pass
