from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Preferences_input(Page):
    form_model = "player"
    form_fields = ['salary',
                            'bonus',
                            'location',
                            'insurance_coverage',
                            'vacation_time',
                            'moving_expenses',
                            'job_assignment',
                            'starting_date']

    def before_next_page(self):
        id = self.player.id_in_group - 1

        total_points = Constants.salary[self.player.salary][id]+\
                                Constants.bonus[self.player.bonus][id]+\
                                Constants.location[self.player.location][id]+\
                                Constants.insurance_coverage[self.player.insurance_coverage][id]+\
                                Constants.vacation_time[self.player.vacation_time][id]+\
                                Constants.moving_expenses[self.player.moving_expenses][id]+\
                                Constants.job_assignment[self.player.job_assignment][id]+\
                                Constants.starting_date[self.player.starting_date][id]
        if total_points != 13200:
            self.player.low_score = True
        self.player.total_points = total_points



class Preferences_result(Page):
    form_model = "player"

class Case_page(Page):
    form_model = "player"

    timeout_seconds= Constants.reading_time * 60
    def vars_for_template(self):
        if self.player.id_in_group == 1:
            return dict(file_loc='NR_bot/Recruiter.pdf#toolbar=0')
        else:
            return dict(file_loc='NR_bot/Candidate.pdf#toolbar=0')

class Case_page_no_timer(Page):
    form_model = "player"

    def vars_for_template(self):
        if self.player.id_in_group == 1:
            return dict(file_loc='NR_bot/Recruiter.pdf#toolbar=0')
        else:
            return dict(file_loc='NR_bot/Candidate.pdf#toolbar=0')


class Planning_doc(Page):
    form_model = "player"
    form_fields = ["planning_text"]


    timeout_seconds = 120

    def vars_for_template(self):
        return dict(max_word_limit=Constants.planning_doc_length, timeout_seconds=120)

class Introduction(Page):
    form_model = "player"

    def vars_for_template(self):
        return dict(reading_limit=Constants.reading_time)

class Link_to_simulation(Page):
    form_model = "group"

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
        return self.player.id_in_group == 1

class Negotiation_process(Page):
    form_model = "group"
    form_fields = ["salary_fract","bonus_fract","job_assignment_fract","insurance_coverage_fract","moving_expenses_fract","vacation_time_fract","location_fract","starting_date_fract"]

    def is_displayed(self):
        return self.player.id_in_group == 1

class Outcome_intro(Page):
    form_model = "group"

class MyWaitPage(WaitPage):
    pass


#Introduction, Case_page, Preferences_input, Preferences_result, Planning_doc, Link_to_simulation, Case_page_no_timer, Negotiated_outcome
page_sequence = [Introduction, Case_page, Preferences_input, Preferences_result, Planning_doc, Link_to_simulation, Case_page_no_timer,Outcome_intro, Negotiated_outcome, Negotiation_process, MyWaitPage]
