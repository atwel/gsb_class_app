from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants
import time



class Journaling_page(Page):

        form_model = "player"
        form_fields = ["journaling_text"]

class Outro(Page):
    form_model = "group"

page_sequence = [Journaling_page, Outro]
