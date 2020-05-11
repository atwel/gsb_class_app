from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants




class Introduction(Page):
    form_model = "player"


class Buyer(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.role() == "buyer"

    def vars_for_template(self):
        return {"pdf_file": "SugarBowl_Section1/Buyer.pdf"}


class Dealer(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.role() == "dealer"

    def vars_for_template(self):
        return {"pdf_file": "SugarBowl_Section1/Dealer.pdf"}



class Planning_doc(Page):
    form_model = "player"
    form_fields = ["planning_text"]

    def vars_for_template(self):
        if self.player.role() == "buyer":
            return {"pdf_file": "SugarBowl_Section1/Buyer.pdf"}
        else:
            return {"pdf_file": "SugarBowl_Section1/Dealer.pdf"}

class Initial_offer(Page):
    form_model = "group"
    form_fields= ["initial_offer","reservation_price_buyer"]

    def is_displayed(self):
        return self.player.role() == "buyer"

class Reservation_price(Page):
    form_model = "group"
    form_fields= ["reservation_price_dealer","target_price_dealer"]

    def is_displayed(self):
        return self.player.role() == "dealer"



class Email_page(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.role() == "buyer"

    def vars_for_template(self):
        c, r = self.group.get_players()
        try:
            email = r.participant.label
            name = Constants.SUNet_to_name[email]
        except:
            email = "atwell"
            name = "Unidentified; Email Professor Atwell to get a correct email address"

        return {"email":email +"@stanford.edu", "name": name}


class Email_wait_page(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.role() == "dealer"

class Negotiated_outcome(Page):

    form_model = "group"
    form_fields = ["final_price","who_purchased"]

    def is_displayed(self):
        return self.player.role() == "buyer"


class Journaling_page(Page):
    form_model = "player"

    form_fields = ["journaling_text"]

    def vars_for_template(self):
        return {"Buyer": "SugarBowl_Section1/Buyer.pdf", "Dealer": "SugarBowl_Section1/Dealer.pdf"}


class Outro(Page):
    form_model = "group"


page_sequence = [Introduction, Buyer, Dealer, Planning_doc, Initial_offer,Reservation_price, Email_page, Email_wait_page, Buyer, Dealer, Negotiated_outcome, Journaling_page, Outro]
