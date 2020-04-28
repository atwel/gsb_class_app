from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class IntroWaitPage(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
            csv_str = "Pre-assign Room Name,Email Address\n"
            for index, players in enumerate(self.subsession.get_group_matrix()):
                    for player in players:
                        csv_str += "room{},{}@stanford.edu\n".format(index+1,player.participant.label)
            print(csv_str)
            with open("breakout_room_assignment.csv","w+") as f:
                f.write(csv_str)


class Introduction(Page):
    form_model = "player"

    def vars_for_template(self):
        return dict(reading_limit=Constants.reading_time)


class Case_page(Page):
    form_model = "player"

    timeout_seconds= Constants.reading_time * 60
    def vars_for_template(self):
        if self.player.id_in_group == 1:
            # is meeting host
            return dict(file_loc='BiopharmSeltek/Seltek.pdf')
        else:
            return dict(file_loc='BiopharmSeltek/BioPharm.pdf')


class Preferences_input_ST(Page):
    form_model = "group"
    form_fields = ['target_ST', "batna_ST"]

    def is_displayed(self):
            return self.player.id_in_group == 1


class Preferences_input_BF(Page):
    form_model = "group"
    form_fields = ['target_BF', "batna_BF"]

    def is_displayed(self):
            return self.player.id_in_group == 2


class Planning_doc(Page):
    form_model = "player"
    form_fields = ["planning_text"]

    timeout_seconds= Constants.planning_doc_time_minutes * 60

    def vars_for_template(self):
        return dict(max_word_limit=Constants.planning_doc_length)


class Create_link(Page):
    form_model = "group"

    form_fields = ["link"]

    def is_displayed(self):
        return self.player.id_in_group == 1


class Create_link_wait(WaitPage):
    form_model = "player"

    def vars_for_template(self):
        return {"title_text":"Creation of Meeting"}


class Link_to_simulation(Page):
    form_model = "group"


class Case_page_no_timer(Page):
    form_model = "player"

    def vars_for_template(self):
        if self.player.id_in_group == 1:
            return dict(file_loc='BiopharmSeltek/Seltek.pdf')
        else:
            return dict(file_loc='BiopharmSeltek/BioPharm.pdf')


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

    def vars_for_template(self):
        return {"title_text": "Reporting the outcome", "body_text":"As the Seltek representative, you'll stay on this page until the BioPharm representative finishes inputing the results.\n\n"}


class Outro(Page):
    form_model = "group"


page_sequence = [IntroWaitPage, Introduction, Case_page, Preferences_input_BF, Preferences_input_ST, Planning_doc, Create_link, Create_link_wait, Link_to_simulation, Case_page_no_timer, Negotiated_outcome_one, Negotiated_outcome_two, Outcome_wait, Outro]
