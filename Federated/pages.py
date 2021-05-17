from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class IntroWaitPage(WaitPage):

    after_all_players_arrive = "set_first_meet"


    def vars_for_template(self):
        return {"title_text": "Waiting for others", "body_text":"Please wait a moment while your partners sign on.\n\n"}



class Introduction(Page):
    form_model = "player"


class Stockman(Page):
    form_model = "player"

    #timeout_seconds = Constants.reading_time*60
    #timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.role() == "stockman"

    def vars_for_template(self):
        return {"pdf_file": "Federated/Stockman.pdf"}

    def js_vars(self):
        return dict(button_show=Constants.material_button_show*60000)


class Stockman_nt(Page):
    form_model = "player"

    template_name = "Federated/Stockman.html"

    def is_displayed(self):
        return self.player.role() == "stockman"

    def vars_for_template(self):
        return {"pdf_file": "Federated/Stockman.pdf"}

    def js_vars(self):
        return dict(button_show=Constants.material_button_show*60000)


class Turbo(Page):
    form_model = "player"

    #timeout_seconds = Constants.reading_time*60
    #timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.role() == "turbo"

    def vars_for_template(self):
        return {"pdf_file": "Federated/Turbo.pdf"}

    def js_vars(self):
        return dict(button_show=Constants.material_button_show*60000)


class Turbo_nt(Page):
    form_model = "player"

    template_name = "Federated/Turbo.html"

    def is_displayed(self):
        return self.player.role() == "turbo"

    def vars_for_template(self):
        return {"pdf_file": "Federated/Turbo.pdf"}

    def js_vars(self):
        return dict(button_show=Constants.material_button_show*60000)


class United(Page):
    form_model = "player"

    #timeout_seconds = Constants.reading_time*60
    #timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.role() == "united"

    def vars_for_template(self):
        return {"pdf_file": "Federated/United.pdf"}

    def js_vars(self):
        return dict(button_show=Constants.material_button_show*60000)


class United_nt(Page):
    form_model = "player"

    template_name = "Federated/United.html"

    def is_displayed(self):
        return self.player.role() == "united"

    def vars_for_template(self):
        return {"pdf_file": "Federated/United.pdf"}

    def js_vars(self):
        return dict(button_show=Constants.material_button_show*60000)



class Planning_doc(Page):
    form_model = "player"
    form_fields = ["planning_text"]

    #timeout_seconds = Constants.planning_doc_time *60
    #timer_text = "Time left to finish the planning document"

    def vars_for_template(self):
        if self.player.role() == "stockman":
            return {"pdf_file": "Federated/Stockman.pdf"}
        elif self.player.role() == "turbo":
            return {"pdf_file": "Federated/Turbo.pdf"}
        elif self.player.role() == "united":
            return {"pdf_file": "Federated/United.pdf"}


class Ready_for_class(Page):
    form_model = "player"

class Wait_to_negotiate(WaitPage):

    form_model = "group"

    after_all_players_arrive = "set_start_time"

    def vars_for_template(self):
        return {"title_text": "Waiting for your counterparts to finish preparing", "body_text":"It shouldn't be too long now!\n\n"}


class Back_to_class(Page):
    form_model = "player"

    def vars_for_template(self):

        if self.group.stockman:
            if self.player.role() == "united":
                return {"rep": "United", "alter":"Stockman", "in_first":True}
            elif self.player.role() == "stockman":
                return {"alter": "United", "rep":"Stockman", "in_first":True}
            else:
                return {"rep": "Turbo", "alter":"NA", "in_first":False}
        else:
            if self.player.role() == "united":
                return {"rep": "United", "alter":"Turbo", "in_first":True}
            elif self.player.role() == "turbo":
                return {"alter": "United", "rep":"Turbo", "in_first":True}
            else:
                return {"rep": "Stockman", "alter":"NA", "in_first":False}




class Outcome(Page):
    form_model = "player"

    form_fields = ["united","stockman","turbo","first_meeting"]



class Journaling_page(Page):
    form_model = "player"

    form_fields = ["journaling_text"]

    timeout_seconds = Constants.reflection_time*60


class Outro(Page):
    form_model = "group"






page_sequence = [Introduction, Stockman, Turbo, United, Planning_doc, Ready_for_class, Back_to_class, Stockman_nt, Turbo_nt, United_nt, Outcome, Journaling_page, Outro]
