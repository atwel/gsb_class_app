from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import time


class IntroWaitPage(WaitPage):
    group_by_arrival_time = True

    def vars_for_template(self):
        return {"title_text": "Hang tight", "body_text":"Please wait a moment to get paired.\n\nIf you've been on this page for a while, try refreshing the page."}


class Introduction(Page):
    form_model = "player"

    def vars_for_template(self):
        return dict(reading_limit=Constants.reading_time)


class Meeting_location(Page):
    form_model = "player"

    def vars_for_template(self):
            return {"zoom_link":self.participant.vars["zoom_link"], "pdf_file":"global/OutdoorMap.pdf"}


class Seltek_materials(Page):
    form_model = "player"

    timeout_seconds= Constants.reading_time * 60
    timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return {"pdf_file": "BiopharmSeltek/Seltek.pdf"}


class Biopharm_materials(Page):
    form_model = "player"

    timeout_seconds= Constants.reading_time * 60
    timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        return {"pdf_file": "BiopharmSeltek/BioPharm.pdf"}


class Preferences_input_ST(Page):
    form_model = "group"
    form_fields = ['target_ST', "batna_ST"]

    timeout_seconds= 120
    timer_text = 'Time left to input values'
    def is_displayed(self):
            return self.player.id_in_group == 1

    def vars_for_template(self):
        return {"pdf_file": "BiopharmSeltek/Seltek.pdf"}


class Preferences_input_BF(Page):
    form_model = "group"
    form_fields = ['target_BF', "batna_BF"]

    timeout_seconds= 120
    timer_text = 'Time left to input values'
    def is_displayed(self):
            return self.player.id_in_group == 2

    def vars_for_template(self):
        return {"pdf_file": "BiopharmSeltek/BioPharm.pdf"}


class Planning_doc(Page):
    form_model = "player"
    form_fields = ["planning_text"]

    timeout_seconds= Constants.planning_doc_time_minutes * 60
    timer_text = 'Time left for writing your document:'

    def vars_for_template(self):
        if self.player.id_in_group == 1:
            return {"return_link": "BiopharmSeltek/Seltek_materials.html","max_word_limit":Constants.planning_doc_length}
        if self.player.id_in_group == 2:
            return {"return_link": "BiopharmSeltek/Biopharm_materials.html","max_word_limit":Constants.planning_doc_length}


class Meeting_location_reminder(Page):
    form_model = "player"

    def vars_for_template(self):
            return {"zoom_link":self.participant.vars["zoom_link"], "pdf_file":"global/OutdoorMap.pdf"}


class Meeting_wait(WaitPage):
    form_model = "group"
    after_all_players_arrive = 'set_timer'

    def vars_for_template(self):
            return {"title_text":"Waiting...","body_text":"We're waiting for your counterparty to be ready. Once they finish up, you'll go back to the case materials page and the timed negotiation will begin."}


class Seltek_materials_no_timer(Page):
    form_model = "player"

    template_name = "BiopharmSeltek/Seltek_materials.html"

    timer_text = 'Time left for negotiating the case:'

    def get_timeout_seconds(self):
        return self.participant.vars["sim_timer"] - time.time()

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return {"pdf_file": "BiopharmSeltek/Seltek.pdf"}


class BioPharm_materials_no_timer(Page):
    form_model = "player"
    template_name = "BiopharmSeltek/Biopharm_materials.html"

    timer_text = 'Time left for negotiating the case:'

    def get_timeout_seconds(self):
        return self.participant.vars["sim_timer"] - time.time()

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        return {"pdf_file": "BiopharmSeltek/BioPharm.pdf"}


class Negotiated_outcome_one(Page):

    form_model = "group"
    form_fields = ["made_initial","initial_price","deal"]

    def is_displayed(self):
        return self.player.id_in_group == 2


class Negotiated_outcome_two(Page):

    form_model = "group"

    def get_form_fields(self):
        if self.group.deal:
            return ['final_sale_price']
        else:
            return ["last_Seltek","last_Biopharm"]

    def is_displayed(self):
        return self.player.id_in_group == 2


class Outcome_wait(WaitPage):
    form_model = "group"

    form_fields = ["nego_time"]

    def vars_for_template(self):
        if self.player.id_in_group == 1:
            return {"title_text": "Reporting the outcome", "body_text":"Wait a moment while the BioPharm representative finishes inputting the results.\n\n"}
        else:
            return {"title_text": "Waiting", "body_text":"Wait a moment for the Seltek representative.\n\n"}


class Sign_off_page(Page):
    form_model = "group"

    def before_next_page(self):
        bio = self.group.get_player_by_id(2)
        self.group.nego_time = int(time.time() - bio.participant.vars["sim_start"])

class Finished_case(Page):
    form_model = "group"


class Journaling_page(Page):
    form_model = "player"

    form_fields = ["journaling_text"]

    timeout_seconds = 180

    def vars_for_template(self):
        if self.player.id_in_group == 1:
            return {"pdf_file": "BiopharmSeltek/Seltek.pdf"}
        if self.player.id_in_group == 2:
            return {"pdf_file": "BiopharmSeltek/BioPharm.pdf"}


class Outro(Page):
    form_model = "group"





page_sequence = [IntroWaitPage, Introduction, Meeting_location, Seltek_materials, Biopharm_materials, Preferences_input_BF, Preferences_input_ST, Planning_doc, Meeting_wait, Meeting_location_reminder, Seltek_materials_no_timer, BioPharm_materials_no_timer, Negotiated_outcome_one, Negotiated_outcome_two, Outcome_wait,  Finished_case, Journaling_page, Outro]
