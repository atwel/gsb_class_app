from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import time


class IntroWaitPage(WaitPage):

    def vars_for_template(self):
            return {"title_text": "Waiting for your partner", "body_text":"Wait a moment while your partner signs on.\n\n"}

    def after_all_players_arrive(self):
            csv_str = "Pre-assign Room Name,Email Address\n"
            for index, players in enumerate(self.subsession.get_group_matrix()):
                    for player in players:
                        csv_str += "room{},{}@stanford.edu\n".format(index+1,player.participant.label)
            print(csv_str)


class Introduction(Page):
    form_model = "player"

    def vars_for_template(self):
        return dict(reading_limit=Constants.reading_time)

class Survey(Page):
    form_model = "player"

    form_fields = ["settings_rating", "skilled_rating","experience_rating"]


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

    timeout_seconds= 60
    timer_text = 'Time left to input values'
    def is_displayed(self):
            return self.player.id_in_group == 1

    def vars_for_template(self):
        return {"return_link": "BiopharmSeltek/Seltek_materials.html"}


class Preferences_input_BF(Page):
    form_model = "group"
    form_fields = ['target_BF', "batna_BF"]

    timeout_seconds= 60
    timer_text = 'Time left to input values'
    def is_displayed(self):
            return self.player.id_in_group == 2

    def vars_for_template(self):
        return {"return_link": "BiopharmSeltek/Biopharm_materials.html"}


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


class Create_link(Page):
    form_model = "group"

    form_fields = ["link"]

    def is_displayed(self):
        return self.player.id_in_group == 1


class Start_recording(Page):
    form_model = "group"

    def is_displayed(self):
        return self.player.id_in_group == 1

    def before_next_page(self):
        self.participant.vars["sim_start"] = time.time()
        self.participant.vars["sim_timer"] = time.time() + Constants.negotiating_time * 60 + 30


class Create_link_wait(WaitPage):
    form_model = "player"

    def vars_for_template(self):
        if self.player.id_in_group == 1:
            return {"title_text": "Partner is catching up", "body_text": "Your Biopharm partner is catching up. You'll wait here until they arrive."}
        else:
            return {"title_text":"Creation of Meeting","body_text":"The Seltek representative is creating a Zoom meeting. You'll get a link for it shortly."}



class Link_to_simulation(Page):
    form_model = "group"

    def get_timeout_seconds(self):
        seltek = self.group.get_player_by_id(1)
        return seltek.participant.vars["sim_timer"] - time.time()

    timer_text = 'Time left for negotiating the case:'

    def vars_for_template(self):
        try:
            if self.participant.label in Constants.section_1_participants:
                return {"return_link": Constants.link_581_1}
            elif self.participant.label in Constants.section_2_participants:
                return {"return_link": Constants.link_581_2}
            else:
                return {"return_link":"http://google.com"}
        except:
            return {"return_link":"http://google.com"}



class Seltek_materials_no_timer(Page):
    form_model = "player"

    template_name = "BiopharmSeltek/Seltek_materials.html"

    timer_text = 'Time left for negotiating the case:'

    def get_timeout_seconds(self):
        seltek = self.group.get_player_by_id(1)
        return seltek.participant.vars["sim_timer"] - time.time()

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return {"pdf_file": "BiopharmSeltek/Seltek.pdf"}


class BioPharm_materials_no_timer(Page):
    form_model = "player"
    template_name = "BiopharmSeltek/Biopharm_materials.html"

    timer_text = 'Time left for negotiating the case:'

    def get_timeout_seconds(self):
        seltek = self.group.get_player_by_id(1)
        return seltek.participant.vars["sim_timer"] - time.time()

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
        if self.player.id_in_group == 1:
            self.group.nego_time = int(time.time() - self.participant.vars["sim_start"])

class Journaling_page(Page):
    form_model = "player"

    form_fields = ["journaling_text"]

    timeout_seconds = 180

    def vars_for_template(self):
        if self.player.id_in_group == 1:
            return {"return_link": "BiopharmSeltek/Seltek_materials.html"}
        if self.player.id_in_group == 2:
            return {"return_link": "BiopharmSeltek/Biopharm_materials.html"}


class Alter_questions(Page):

    form_model = "player"

    form_fields = ["alter_interact", "alter_closeness"]



class Outro(Page):
    form_model = "group"

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        try:
            if self.participant.label in Constants.section_1_participants:
                return {"return_link": Constants.link_581_1}
            elif self.participant.label in Constants.section_2_participants:
                return {"return_link": Constants.link_581_2}
            else:
                return {"return_link":"https://gsb.stanford.edu"}
        except:
            return {"return_link":"https://gsb.stanford.edu"}

class Link_to_recording(Page):
    form_model = "group"

    form_fields = ["link_to_recording"]

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        try:
            if self.participant.label in Constants.section_1_participants:
                return {"return_link": Constants.link_581_1}
            elif self.participant.label in Constants.section_2_participants:
                return {"return_link": Constants.link_581_2}
            else:
                return {"return_link":"https://gsb.stanford.edu"}
        except:
            return {"return_link":"https://gsb.stanford.edu"}




page_sequence = [IntroWaitPage, Introduction, Survey, Seltek_materials, Biopharm_materials, Preferences_input_BF, Preferences_input_ST, Planning_doc, Create_link, Start_recording, Create_link_wait, Link_to_simulation, Seltek_materials_no_timer, BioPharm_materials_no_timer, Negotiated_outcome_one, Negotiated_outcome_two, Outcome_wait, Sign_off_page, Journaling_page, Alter_questions, Outro, Link_to_recording]
