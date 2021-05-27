from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time

class New_round(Page):
    form_model = "group"

    timeout_seconds = 60

    def is_displayed(self):
        if self.subsession.round_number == 1:
            return True
        else:
            if not all([g.did_not_pass for g in self.group.in_previous_rounds()]) or self.group.in_round(self.group.round_number-1).timed_out:
                self.group.did_not_pass = False
                self.group.timed_out = True
                self.group.pass_displayed = True
            return False

    def before_next_page(self):
        if self.player.role() == "harborco":
            if self.subsession.round_number == 1:
                self.group.start_time = time.time()



class Proposal(Page):
    form_model = "group"

    form_fields = ["mix","eco","union","loan","comp"]

    def is_displayed(self):
        return (self.group.did_not_pass and self.player.role() == "harborco")

    def vars_for_template(self):
        return {"pdf_file": "HarborCo/Harborco.pdf"}


class Proposal_wait(WaitPage):
    def is_displayed(self):
        return self.group.did_not_pass and not self.group.pass_displayed

    def vars_for_template(self):
        return {"title_text": "Negotiations and Proposal Crafting", "body_text": "You are currently in negotiations and will remain so until a scheduled vote is called or HarborCo puts a proposal up for a vote."}


class Vote(Page):
    form_model = "player"

    form_fields = ["vote"]

    timeout_seconds = 90


    def is_displayed(self):
        return self.group.did_not_pass and self.player.role() != "harborco"

    def vars_for_template(self):
        if self.player.role() == "union":
            pdf_file="HarborCo/Union.pdf"
        if self.player.role() == "enviro":
            pdf_file="HarborCo/EnvironmentalLeague.pdf"
        if self.player.role() == "gov":
            pdf_file="HarborCo/Governor.pdf"
        if self.player.role() == "ports":
            pdf_file="HarborCo/OtherPorts.pdf"
        if self.player.role() == "dcr":
            pdf_file="HarborCo/FederalDCR.pdf"
        eco_if = (self.group.eco == "Some harm")
        loan_if = (self.group.loan != "No federal loan")
        return {"eco_if":eco_if,"pdf_file":pdf_file, "loan_if":loan_if,"eco":self.group.eco.lower(),"mix":self.group.mix.lower(),"loan":self.group.loan.lower(), "union":self.group.union.lower(),"comp":self.group.comp}

class Tally(WaitPage):

    def is_displayed(self):
        return self.group.did_not_pass

    def vars_for_template(self):
        return {"title_text": "Waiting for all votes to be cast.", "body_text": "Other parties are still voting. Once votes are in and tallied, the results will be shown."}

    def after_all_players_arrive(self):

        if self.group.did_not_pass:

            count = 0
            veto = False

            for p in self.group.get_players():
                if p.vote == "Yes":
                    count +=1

                if p.role() == "dcr":
                    if (p.vote == "No" and self.group.loan != "No federal loan"):
                        veto = True

            if veto:
                self.group.high_passed = False
                self.group.passed = False
                self.group.vetoed = True
                self.group.did_not_pass = True
            else:
                self.group.vetoed = False
                if count == 5:
                    self.group.high_passed = True
                    self.group.passed = False
                    self.group.did_not_pass = False
                elif count == 4:
                    self.group.high_passed = False
                    self.group.passed = True
                    self.group.did_not_pass = False
                elif count <=3:
                    self.group.high_passed = False
                    self.group.passed = False
                    self.group.did_not_pass = True



        print(time.time(), self.group.in_round(1).start_time)
        print("time passed", (time.time() - self.group.in_round(1).start_time)/60)
        if (time.time() - self.group.in_round(1).start_time) / 60 > 4:
            if not any([self.group.passed, self.group.high_passed]):
                self.group.timed_out = True






class Results_high_pass(Page):

    form_model = "group"

    timeout_seconds = 60

    def is_displayed(self):
        value = self.group.high_passed and not self.group.pass_displayed
        return value

    def before_next_page(self):
        self.group.pass_displayed = True


    def vars_for_template(self):
        for p in self.group.get_players():
            if p.role() == "union":
                if p.vote == "Yes":
                    union = "For"
                else:
                    union = "Against"
            if p.role() == "gov":
                if p.vote == "Yes":
                    gov = "For"
                else:
                    gov = "Against"
            if p.role() == "dcr":
                if p.vote == "Yes":
                    dcr = "For"
                else:
                    dcr = "Against"
            if p.role() == "enviro":
                if p.vote == "Yes":
                    enviro = "For"
                else:
                    enviro = "Against"
            if p.role() == "ports":
                if p.vote == "Yes":
                    ports = "For"
                else:
                    ports = "Against"
        return {"union":union,"gov":gov,"ports":ports, "enviro":enviro,"dcr":dcr }


class Results_pass(Page):

    form_model = "group"

    timeout_seconds = 60

    def is_displayed(self):
        value = self.group.passed and not self.group.pass_displayed
        return value

    def before_next_page(self):
        self.group.pass_displayed = True

    def vars_for_template(self):
        for p in self.group.get_players():
            if p.role() == "union":
                if p.vote == "Yes":
                    union = "For"
                else:
                    union = "Against"
            if p.role() == "gov":
                if p.vote == "Yes":
                    gov = "For"
                else:
                    gov = "Against"
            if p.role() == "dcr":
                if p.vote == "Yes":
                    dcr = "For"
                else:
                    dcr = "Against"
            if p.role() == "enviro":
                if p.vote == "Yes":
                    enviro = "For"
                else:
                    enviro = "Against"
            if p.role() == "ports":
                if p.vote == "Yes":
                    ports = "For"
                else:
                    ports = "Against"
        return {"union":union,"gov":gov,"ports":ports, "enviro":enviro,"dcr":dcr }


class Results_not_passed(Page):

    form_model = "group"

    timeout_seconds = 60

    def is_displayed(self):
        value = self.group.did_not_pass and not self.group.vetoed
        return value

    def vars_for_template(self):
        for p in self.group.get_players():
            if p.role() == "union":
                if p.vote == "Yes":
                    union = "For"
                else:
                    union = "Against"
            if p.role() == "gov":
                if p.vote == "Yes":
                    gov = "For"
                else:
                    gov = "Against"
            if p.role() == "dcr":
                if p.vote == "Yes":
                    dcr = "For"
                else:
                    dcr = "Against"
            if p.role() == "enviro":
                if p.vote == "Yes":
                    enviro = "For"
                else:
                    enviro = "Against"
            if p.role() == "ports":
                if p.vote == "Yes":
                    ports = "For"
                else:
                    ports = "Against"
        return {"union":union,"gov":gov,"ports":ports, "enviro":enviro,"dcr":dcr }


class Results_veto(Page):

    form_model = "group"

    timeout_seconds = 60

    def is_displayed(self):
        return self.group.vetoed

    def vars_for_template(self):

        for p in self.group.get_players():
            if p.role() == "union":
                if p.vote == "Yes":
                    union = "For"
                else:
                    union = "Against"
            if p.role() == "gov":
                if p.vote == "Yes":
                    gov = "For"
                else:
                    gov = "Against"
            if p.role() == "dcr":
                if p.vote == "Yes":
                    dcr = "For"
                else:
                    dcr = "Against"
            if p.role() == "enviro":
                if p.vote == "Yes":
                    enviro = "For"
                else:
                    enviro = "Against"
            if p.role() == "ports":
                if p.vote == "Yes":
                    ports = "For"
                else:
                    ports = "Against"
        return {"union":union,"gov":gov,"ports":ports, "enviro":enviro,"dcr":dcr }

class Timed_out(Page):
    form_model = 'group'

    def is_displayed(self):
        return self.group.timed_out and not self.group.pass_displayed

    def before_next_page(self):
        self.group.pass_displayed = True


page_sequence = [New_round, Proposal, Proposal_wait, Vote, Tally, Results_high_pass, Results_pass, Results_not_passed, Results_veto,Timed_out]
