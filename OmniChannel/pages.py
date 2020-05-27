from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants



class Introduction(Page):
    form_model = "player"


class DTV(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.role() == "3dtv"

    def vars_for_template(self):
        return {"pdf_file": "OmniChannel/3DTV.pdf"}

class Message_DTV(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.role() == "3dtv"


class Omni(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.role() == "omni"

    def vars_for_template(self):
        return {"pdf_file": "OmniChannel/OmniChannel.pdf"}

class Message_OC(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.role() == "omni"


class Agreement(Page):
    form_model = "player"

    form_fields = ["agreement"]

class Planning_doc(Page):
    form_model = "player"
    form_fields = ["planning_text"]

    def vars_for_template(self):
        if self.player.role() == "3dtv":
            return {"pdf_file": "OmniChannel/3DTV.pdf"}
        elif self.player.role() == "omni":
            return {"pdf_file": "OmniChannel/OmniChannel.pdf"}

class Wait_until_open(Page):
    form_model = "player"

class Outcome(Page):
    form_model = "player"

    form_fields = ["data","license_restrictions","premium_count","premium_fees","regular_count","regular_fees","data_center_fees","length","termination"]

    def is_displayed(self):
        if self.player.agreement =="Yes":
            return True
        else:
            return False

class Journaling_page(Page):
    form_model = "player"

    form_fields = ["journaling_text"]

    timeout_seconds = Constants.reflection_time*60

class Outro(Page):
    form_model = "group"


page_sequence = [Introduction, DTV, Omni, Message_DTV, Message_OC, Planning_doc, Wait_until_open, DTV, Omni, Agreement,Outcome, Journaling_page,Outro]
