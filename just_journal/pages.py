from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants
import time



class Journaling_page(Page):

    form_model = "player"

    def vars_for_template(self):
        return {"assignment_url":"https://canvas.stanford.edu/courses/173725/assignments/514485"}

class Outro(Page):
    form_model = "group"

page_sequence = [Journaling_page, Outro]
