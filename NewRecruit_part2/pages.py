from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants



class Create_groups(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'set_groups'
    form_model = "player"


class Show_groups(Page):
    form_model = "group"

    def vars_for_template(self):
            return {"zoom_link":self.participant.vars["zoom_link"], "pdf_file":"global/OutdoorMap.pdf"}


class Candidate_no_timer(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.participant.vars["role"] == "candidate"

    def vars_for_template(self):
        return {"pdf_file": "NewRecruit/Candidate.pdf"}

    def js_vars(self):
        return dict(button_show=0)#Constants.material_button_show_no_timer*60000)


class Recruiter_no_timer(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.participant.vars["role"] == "recruiter"

    def vars_for_template(self):
        return {"pdf_file": "NewRecruit/Recruiter.pdf"}

    def js_vars(self):
        return dict(button_show=0)#Constants.material_button_show_no_timer*60000)


class Negotiated_outcome(Page):

    form_model = "group"
    form_fields = ['salary',
                            'bonus',
                            'location',
                            'insurance_coverage',
                            'vacation_time',
                            'moving_expenses',
                            'job_assignment',
                            'starting_date']
    def is_displayed(self):
        return self.player.participant.vars["role"]  == "recruiter"


class Negotiation_process(Page):
    form_model = "player"
    form_fields = ["salary_fract","bonus_fract","job_assignment_fract","insurance_coverage_fract","moving_expenses_fract","vacation_time_fract","location_fract","starting_date_fract"]



class Journaling_page(Page):
    form_model = "player"

    form_fields = ["journaling_text"]

    timeout_seconds = 180

    def vars_for_template(self):
        return {"Recruiter": "NewRecruit/Recruiter.pdf", "Candidate": "NewRecruit/Candidate.pdf"}

class Outcome_wait(WaitPage):
    form_model = "group"

    def vars_for_template(self):
        return {"title_text": "Reporting the outcome", "body_text":"As the person in the role of the Candidate, you'll stay on this page until the Recruiter finishes inputting the results.\n\n"}


class Outro(Page):
    form_model = "group"

class Explore_calc(Page):

    form_model = "group"




page_sequence = [Create_groups, Show_groups, Candidate_no_timer, Recruiter_no_timer, Negotiated_outcome, Negotiation_process, Journaling_page, Outro, Explore_calc]
