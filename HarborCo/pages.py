from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants



class Introduction(Page):
    form_model = "player"

    """def before_next_page(self):
        count_present =0
        for player in self.player.get_others_in_subsession():
            if "arrival_time" in player.participant.vars:
                count_present += 1


        if self.participant.vars["name"] != "autoadvanced":
            my_role = count_present % 6

            if my_role ==  0:
                self.player.role() = "union"
            elif my_role == 1:
                self.player.role() = "enviro"
            elif my_role == 2:
                self.player.role() = "ports"
            elif my_role == 3:
                self.player.role() = "dcr"
            elif my_role == 4:
                self.player.role() = "gov"
            else:
                self.player.role() = "harborco"
        """




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
    #form_fields = ["planning_text"]

    def vars_for_template(self):
        if self.player.role() == "dcr":
            return {"pdf_file": "HarborCo/FederalDCR.pdf","assignment_url":"https://canvas.stanford.edu/courses/173725/assignments/514484"}
        elif self.player.role() == "harborco":
            return {"pdf_file": "HarborCo/Harborco.pdf","assignment_url":"https://canvas.stanford.edu/courses/173725/assignments/514484"}
        elif self.player.role() == "ports":
            return {"pdf_file": "HarborCo/OtherPorts.pdf","assignment_url":"https://canvas.stanford.edu/courses/173725/assignments/514484"}
        elif self.player.role() == "union":
            return {"pdf_file": "HarborCo/Union.pdf","assignment_url":"https://canvas.stanford.edu/courses/173725/assignments/514484"}
        elif self.player.role() == "gov":
            return {"pdf_file": "HarborCo/Governor.pdf","assignment_url":"https://canvas.stanford.edu/courses/173725/assignments/514484"}
        elif self.player.role() == "enviro":
            return {"pdf_file": "HarborCo/EnvironmentalLeague.pdf","assignment_url":"https://canvas.stanford.edu/courses/173725/assignments/514484"}
        else:
            return {"pdf_file":"HarborCo/Governor.pdf","assignment_url":"https://canvas.stanford.edu/courses/173725/assignments/514484"}


class Back_to_class(Page):
    form_model = "player"



page_sequence = [Introduction, Union, Ports, Dcr, Harborco, Enviro, Governor, Planning_doc, Back_to_class, Union, Ports, Dcr, Harborco, Enviro, Governor]
