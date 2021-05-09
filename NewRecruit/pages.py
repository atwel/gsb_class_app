from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants




class Introduction(Page):
    form_model = "player"

    def before_next_page(self):

        remote_all = 0
        remote_candidates = 0
        inperson_all = 0
        inperson_candidates = 0
        count_in_subsession = len(self.subsession.get_players())

        for player in self.player.get_others_in_subsession():

            if "arrival_time" in player.participant.vars:
                if player.participant.vars["inperson"]:
                    inperson_all +=1
                    if player.candidate:
                        inperson_candidates +=1
                else:
                    remote_all +=1
                    if player.candidate:
                        remote_candidates += 1

        if remote_all + inperson_all == count_in_subsession - 1:
            self.player.candidate = False
            self.player.participant.vars["role"] = "recruiter"
        else:
            if self.participant.vars["inperson"]:
                if inperson_candidates > inperson_all/2:
                    # True when more than half are candidates
                    self.player.candidate = False
                    self.player.participant.vars["role"] = "recruiter"
                else:
                    self.player.candidate = True
                    self.player.participant.vars["role"] = "candidate"
            else:
                if remote_candidates > remote_all/2:
                    self.player.candidate = False
                    self.player.participant.vars["role"] = "recruiter"
                else:
                    self.player.candidate = True
                    self.player.participant.vars["role"] = "candidate"



class Candidate(Page):
    form_model = "player"

    #timeout_seconds = Constants.reading_time*60
    #timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.candidate

    def vars_for_template(self):
        return {"pdf_file": "NewRecruit/Candidate.pdf"}

    def js_vars(self):
        return dict(button_show=0)#Constants.material_button_show*60000)


class Recruiter(Page):
    form_model = "player"

    #timeout_seconds = Constants.reading_time*60
    #timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return not self.player.candidate

    def vars_for_template(self):
        return {"pdf_file": "NewRecruit/Recruiter.pdf"}

    def js_vars(self):
        return dict(button_show=0)#Constants.material_button_show*60000)


class Candidate_calculator(Page):
    form_model = "player"
    form_fields = ['bonus',
                            'job_assignment',
                            'location',
                            'insurance_coverage',
                            'vacation_time',
                            'moving_expenses',
                            "salary",
                            'starting_date']

    #timeout_seconds = Constants.calculator_time * 60
    #timer_text = "Time left to come up with an initial offer"

    def is_displayed(self):
        return self.player.candidate

    def before_next_page(self):
        if self.timeout_happened:
            self.player.initial_offer_points=0
            self.player.bonus=10
            self.player.job_assignment="Division A"
            self.player.location = "San Francisco"
            self.player.insurance_coverage = "Plan A"
            self.player.vacation_time = 25
            self.player.moving_expenses = 100
            self.player.salary = 90000
            self.player.starting_date = "June 1"

        id = 1
        self.player.initial_offer_points = Constants.salary[self.player.salary][id]+\
                                Constants.bonus[self.player.bonus][id]+\
                                Constants.location[self.player.location][id]+\
                                Constants.insurance_coverage[self.player.insurance_coverage][id]+\
                                Constants.vacation_time[self.player.vacation_time][id]+\
                                Constants.moving_expenses[self.player.moving_expenses][id]+\
                                Constants.job_assignment[self.player.job_assignment][id]+\
                                Constants.starting_date[self.player.starting_date][id]

class Recruiter_calculator(Page):
    form_model = "player"
    form_fields = ['bonus',
                            'job_assignment',
                            'location',
                            'insurance_coverage',
                            'vacation_time',
                            'moving_expenses',
                            "salary",
                            'starting_date']

    #timeout_seconds = Constants.calculator_time * 60
    #timer_text = "Time left to come up with an initial offer"

    def is_displayed(self):
        return not self.player.candidate

    def before_next_page(self):
        if self.timeout_happened:
            self.player.initial_offer_points=0
            self.player.bonus=10
            self.player.job_assignment="Division A"
            self.player.location = "San Francisco"
            self.player.insurance_coverage = "Plan A"
            self.player.vacation_time = 25
            self.player.moving_expenses = 100
            self.player.salary = 90000
            self.player.starting_date = "June 1"
        id = 0
        self.player.initial_offer_points = Constants.salary[self.player.salary][id]+\
                                Constants.bonus[self.player.bonus][id]+\
                                Constants.location[self.player.location][id]+\
                                Constants.insurance_coverage[self.player.insurance_coverage][id]+\
                                Constants.vacation_time[self.player.vacation_time][id]+\
                                Constants.moving_expenses[self.player.moving_expenses][id]+\
                                Constants.job_assignment[self.player.job_assignment][id]+\
                                Constants.starting_date[self.player.starting_date][id]


class Planning_doc(Page):
    form_model = "player"
    form_fields = ["planning_text"]

    #timeout_seconds = Constants.planning_doc_time *60
    #timer_text = "Time left to finish the planning document"


    def vars_for_template(self):
        if self.player.candidate:
            return {"pdf_file": "NewRecruit/Candidate.pdf"}
        else:
            return {"pdf_file": "NewRecruit/Recruiter.pdf"}



class Wait_for_class(Page):
    form_model = "player"





page_sequence = [Introduction, Candidate, Recruiter, Candidate_calculator, Recruiter_calculator, Planning_doc, Wait_for_class]
