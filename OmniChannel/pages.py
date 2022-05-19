from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants



class Introduction(Page):
    form_model = "player"

    def before_next_page(self):
        try:
            self.participant.vars["SUNet"] = self.participant.label
            self.participant.vars["name"] = SUNet_to_name[self.participant.label]
        except:
            self.participant.vars["SUNet"] = "none"
            self.participant.vars["name"] = "(come see Dr. Atwell)"

        self.player.name = self.participant.vars["name"]

class DTV(Page):
    form_model = "player"

    timeout_seconds= Constants.reading_time * 60
    timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.role() == "3dtv"

    def vars_for_template(self):
        return {"pdf_file": "OmniChannel/3DTV.pdf"}

class Omni(Page):
    form_model = "player"

    timeout_seconds= Constants.reading_time * 60
    timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.role() == "omni"

    def vars_for_template(self):
        return {"pdf_file": "OmniChannel/OmniChannel.pdf"}

class Message_DTV(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.role() == "3dtv"

class Message_OC(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.role() == "omni"

class Planning_doc(Page):
    form_model = "player"
    form_fields = ["planning_text"]

    timeout_seconds= Constants.planning_doc_time * 60
    timer_text = 'Time left to finish writing your planning document'

    def vars_for_template(self):
        if self.player.role() == "3dtv":
            return {"pdf_file": "OmniChannel/3DTV.pdf"}
        elif self.player.role() == "omni":
            return {"pdf_file": "OmniChannel/OmniChannel.pdf"}

class Wait_until_open(Page):
    form_model = "player"
    #remove  next line when not demo-ing
    #timeout_seconds = 10

class Agreement(Page):
    form_model = "player"
    form_fields = ["agreement"]

    def is_displayed(self):
        if self.player.role() =="3dtv":
            return True
        else:
            return False

class Outcome(Page):
    form_model = "player"
    form_fields = ["data","license_restrictions","premium_count","premium_fees","regular_count","regular_fees","data_center_fees","length","termination"]

    def is_displayed(self):
        if self.player.role() =="3dtv" and self.player.agreement =="Yes":
            return True
        else:
            return False

class Journaling_page_pause(Page):
    form_model = "player"

class Journaling_page(Page):
    form_model = "player"

    form_fields = ["journaling_text"]

class Outro(Page):
    form_model = "group"


page_sequence = [Introduction, DTV, Omni, Message_DTV, Message_OC, Planning_doc, Wait_until_open, DTV, Omni, Agreement,Outcome, Journaling_page_pause, Journaling_page, Outro]
