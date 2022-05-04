from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


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

    timeout_seconds = Constants.calculator_time * 60



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

    timeout_seconds = Constants.calculator_time * 60


class Explore_calc(Page):

    form_model = "player"

    form_fields = ['bonus_pareto',
                            'job_assignment_pareto',
                            'location_pareto',
                            'insurance_coverage_pareto',
                            'vacation_time_pareto',
                            'moving_expenses_pareto',
                            "salary_pareto",
                            'starting_date_pareto',
                            'bonus_pair',
                            'job_assignment_pair',
                            'location_pair',
                            'insurance_coverage_pair',
                            'vacation_time_pair',
                            'moving_expenses_pair',
                            "salary_pair",
                            'starting_date_pair']

    #timeout_seconds = Constants.calculator_time * 60

    def before_next_page(self):


        points_recruiter = Constants.salary[self.player.salary_pareto][0]+\
                                Constants.bonus[self.player.bonus_pareto][0]+\
                                Constants.location[self.player.location_pareto][0]+\
                                Constants.insurance_coverage[self.player.insurance_coverage_pareto][0]+\
                                Constants.vacation_time[self.player.vacation_time_pareto][0]+\
                                Constants.moving_expenses[self.player.moving_expenses_pareto][0]+\
                                Constants.job_assignment[self.player.job_assignment_pareto][0]+\
                                Constants.starting_date[self.player.starting_date_pareto][0]

        points_candidate = Constants.salary[self.player.salary_pareto][1]+\
                                Constants.bonus[self.player.bonus_pareto][1]+\
                                Constants.location[self.player.location_pareto][1]+\
                                Constants.insurance_coverage[self.player.insurance_coverage_pareto][1]+\
                                Constants.vacation_time[self.player.vacation_time_pareto][1]+\
                                Constants.moving_expenses[self.player.moving_expenses_pareto][1]+\
                                Constants.job_assignment[self.player.job_assignment_pareto][1]+\
                                Constants.starting_date[self.player.starting_date_pareto][1]

        self.player.optimal_points = points_candidate + points_recruiter

class Explore_calc2(Page):

    form_model = "player"



page_sequence = [Candidate_calculator, Recruiter_calculator, Explore_calc, Explore_calc2]
