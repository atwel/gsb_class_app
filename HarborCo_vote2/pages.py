from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants



class Introduction(Page):
    form_model = "player"

    after_all_players_arrive = "set_first_meet"


class Proposal(Page):
    form_model = "group"

    form_fields = ["mix","eco","union","loan","comp"]

    def is_displayed(self):
        return self.player.role() == "harborco"

    def vars_for_template(self):
        return {"pdf_file": "HarborCo/Harborco.pdf"}


class Tally(WaitPage):

    def vars_for_template(self):
        return {"title_text": "Waiting for all votes to be cast.", "body_text": "Other parties are still voting. Once votes are in and tallied, the results will be shown."}

    def after_all_players_arrive(self):

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
            self.group.no_pass = False
        else:
            self.group.vetoed = False
            if count == 5:
                print("In count == 5")
                self.group.high_passed = True
                self.group.passed = False
                self.group.no_pass = False
            elif count == 4:
                self.group.high_passed = False
                self.group.passed = True
                self.group.no_pass = False
            elif count <=3:
                self.group.high_passed = False
                self.group.passed = False
                self.group.no_pass = True



class Vote(Page):
    form_model = "player"

    form_fields = ["vote"]

    timeout_seconds = 60

    def is_displayed(self):
        return self.player.role() != "harborco"

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
        return {"eco_if":eco_if, "pdf_file":pdf_file, "loan_if":loan_if,"eco":self.group.eco.lower(),"mix":self.group.mix.lower(),"loan":self.group.loan.lower(), "union":self.group.union.lower(),"comp":self.group.comp}


class Results_high_pass(Page):

    form_model = "group"

    timeout_seconds = 60

    def is_displayed(self):
        return self.group.high_passed


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
        return self.group.passed

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
        return self.group.no_pass

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


class New_round(Page):
    form_model = "group"

    timeout_seconds = 60



class Proposal_wait(WaitPage):
    def vars_for_template(self):
        return {"title_text": "Negotiations and Proposal Crafting", "body_text": "You are currently in negotiations and will remain so until a scheduled vote is called or HarborCo puts a proposal up for a vote."}

page_sequence = [New_round, Proposal, Proposal_wait, Vote, Tally, Results_veto,Results_high_pass, Results_not_passed, Results_pass]
