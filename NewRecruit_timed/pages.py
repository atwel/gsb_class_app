from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class IntroWaitPage(WaitPage):

    def vars_for_template(self):
        return {"title_text": "Waiting for your partner", "body_text":"Wait a moment while your partner signs on.\n\n"}

    def after_all_players_arrive(self):
        csv_str = "Pre-assign Room Name, Email Address\n"
        for index, players in enumerate(self.subsession.get_group_matrix()):
                for player in players:
                    csv_str += "room{},{}@stanford.edu\n".format(index+1,player.participant.label)
        print(csv_str)

        c, r = self.group.get_players()
        try:
            c.participant.vars["partner_name"] = Constants.SUNet_to_name[r.participant.label]
        except:
            c.participant.vars["partner_name"] = "Unidentified"
        try:
            r.participant.vars["partner_name"] = Constants.SUNet_to_name[c.participant.label]
        except:
            r.participant.vars["partner_name"] =  "Unidentified"



class Introduction(Page):
    form_model = "player"

    def before_next_page(self):
        count = 0
        for player in self.player.get_others_in_subsession():
            try:
                print(player.participant.vars["arrival_time"])
                count+=1
            except:
                pass
        print("count of player list", count)


class Candidate(Page):
    form_model = "player"

    #timeout_seconds = Constants.reading_time*60
    #timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.role() == "candidate"

    def vars_for_template(self):
        return {"pdf_file": "NewRecruit/Candidate.pdf"}

    def js_vars(self):
        return dict(button_show=0)#Constants.material_button_show*60000)


class Recruiter(Page):
    form_model = "player"

    #timeout_seconds = Constants.reading_time*60
    #timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.role() == "recruiter"

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
        return self.player.role() == "candidate"

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
        return self.player.role() == "recruiter"

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
        if self.player.role() == "recruiter":
            return {"pdf_file": "NewRecruit/Recruiter.pdf"}
        else:
            return {"pdf_file": "NewRecruit/Candidate.pdf"}



class Wait_for_class(Page):
    form_model = "player"

class Create_groups(WaitPage):
    form_model = "group"
    #group_by_arrival_time = True

class Show_groups(Page):
    form_model = "group"
    after_all_players_arrive = 'set_timer'


class Candidate_no_timer(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.role() == "candidate"

    def vars_for_template(self):
        return {"pdf_file": "NewRecruit/Candidate.pdf"}

    def js_vars(self):
        return dict(button_show=Constants.material_button_show_no_timer*60000)


class Recruiter_no_timer(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.role() == "recruiter"

    def vars_for_template(self):
        return {"pdf_file": "NewRecruit/Recruiter.pdf"}

    def js_vars(self):
        return dict(button_show=Constants.material_button_show_no_timer*60000)


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
        return self.player.role() == "recruiter"


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




page_sequence = [Introduction, Candidate, Recruiter, Candidate_calculator, Recruiter_calculator, Planning_doc, Wait_for_class, Candidate_no_timer, Recruiter_no_timer, Negotiated_outcome, Negotiation_process, Journaling_page, Outro, Explore_calc]
