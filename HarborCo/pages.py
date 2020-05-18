from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants



class Introduction(Page):
    form_model = "player"


class Harborco(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.role() == "harborco"

    def vars_for_template(self):
        return {"pdf_file": "HarborCo/Harborco.pdf"}



class Union(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.role() == "union"

    def vars_for_template(self):
        return {"pdf_file": "HarborCo/Union.pdf"}


class Enviro(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.role() == "enviro"

    def vars_for_template(self):
        return {"pdf_file": "HarborCo/EnvironmentalLeague.pdf"}


class Governor(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.role() == "gov"

    def vars_for_template(self):
        return {"pdf_file": "HarborCo/Governor.pdf"}


class Ports(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.role() == "ports"

    def vars_for_template(self):
        return {"pdf_file": "HarborCo/OtherPorts.pdf"}


class Dcr(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.role() == "dcr"

    def vars_for_template(self):
        return {"pdf_file": "HarborCo/FederalDCR.pdf"}



class Planning_doc(Page):
    form_model = "player"
    form_fields = ["planning_text"]

    def vars_for_template(self):
        if self.player.role() == "dcr":
            return {"pdf_file": "HarborCo/FederalDCR.pdf"}
        elif self.player.role() == "harborco":
            return {"pdf_file": "HarborCo/Harborco.pdf"}
        elif self.player.role() == "ports":
            return {"pdf_file": "HarborCo/OtherPorts.pdf"}
        elif self.player.role() == "union":
            return {"pdf_file": "HarborCo/Union.pdf"}
        elif self.player.role() == "gov":
            return {"pdf_file": "HarborCo/Governor.pdf"}
        elif self.player.role() == "enviro":
            return {"pdf_file": "HarborCo/EnvironmentalLeague.pdf"}



class Back_to_class(Page):
    form_model = "player"





page_sequence = [Introduction, Union, Ports, Dcr, Harborco, Enviro, Governor, Planning_doc, Back_to_class, Union, Ports, Dcr, Harborco, Enviro, Governor]
