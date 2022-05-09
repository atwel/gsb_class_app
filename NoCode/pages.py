from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import time

SUNet_to_name = {"oakkurt":"Ozlem Akkurt","sarahand":"Sarah Anderson","sankalpb":"Sankalp Banerjee","abertha":"Andrew Bertha","jhbuchel":"Jason Buchel","daviscm":"Carolyn Davis","mdicou":"Matt Dicou","dhfranks":"David Franks","jigs":"Jose Garcia Suarez","kgea":"Kathy Gea","ehuscher":"Elspeth Huscher","yvj":"Yash Jain","mlamdan":"Matan Lamdan","cdlince":"Carly Lincenberg","asmartin":"Anne-Sophie Martin","kmodukan":"Kesaobaka Modukanele","povalleb":"Pablo Ovalle","spatarca":"Santiago Patarca","leilap":"Leila Pirbay","kpolle":"Karen Polle","pretes":"Paola Petes Pineda","drichey":"Dan Rickey","wrodrig":"Wes Rodriguez","jrowley":"Josh Rowley","nishaad":"Nishaad Ruparel","juansaez":"Juan Saez Vera","talsarig":"Tal Sarig","nschlein":"Nate Schlein","mariasw":"Maria Silva Willson","kstein10":"Kate Steinman","tstone":"Thomas Stone","ianas":"Iana Stoytcheva","tejsun":"Tejas Sundaresan","mtakasak":"Midori Takasaki","stopper":"Sydni Topper","tjwater":"Tanner Waterstreet","eview":"Evie Woodforde","mzxie":"Michelle Xie","cqyuan":"Chris Yuan","edzhai":"Ethan Zhai","jrbz":"Justin Ziegler","taftab":"Taleha Aftab","oyinda":"Oyinda Ajayi","hajmani":"Hannah Ajmani","hrma":"Henrique Albuquerque","lallende":"Luife Allende","dalpuche":"Dominique Alpuche","annesan":"Annes An","casawa":"Chaitanya Asawa","sherb":"Sher Bhullar","jsburns":"James Burn","cc16":"Charlotte Camacho","ecambern":"Emily Cambern","iw1000":"Lucas Cheon","hamzac":"Hamza Choudery","ncole2":"Nyamekye Coleman","pcout":"Peter Coutoulas","adavis29":"Alexa Davis","sef07":"Steven Ferreira","wglick":"Whitney Glick","anna425":"Anna Gurevich","royhage":"Roy Hage","davidh7":"David Harrison","rbhuang":"Richard Huang","jh21":"Jonathan Hurowitz","andyjin":"Andy Jin","mjuzwiak":"Monika Juzwiak","hkling":"Henry Klingenstein","macklee":"Mackenzie Lee","levinelu":"Lucas Levine","natm":"Natalie Meurer","cliffmil":"Cliff Miller","jmorton4":"Jackson Morton","karlyosb":"Karly Osborne","playfair":"Katherine Playfair","yploder":"Yvonne Ploder","eportura":"Eliann Porturas","psaength":"Phanthila Saengthong","jsayadi":"Jamasb Sayadi","jeremycs":"Jeremy Scott","sheldon3":"Casey Sheldon","amys2023":"Amy Marie Slaughter","nsuchato":"Prao Suchato","m2taylor":"Margot Taylor","wilkinsj":"Jonathan Wilkins","kwolsten":"Kyle Wolstencroft","mzincone":"Michael Zincone","anibaldf":"Anibal de Frankenberg","tracycao":"Tracy Cao","amanc2":"Aman Chaudhary","crozelcm":"Claire Crozel","vdivi":"Vasu Divi","fadavi":"Faraz Fadavi","jhamying":"Julien Ham-Ying","shasson":"Sophie Hasson","srkarr":"S Karr","nkasper":"Nolan Kasper","bkhoo":"Bryan Khoo","akiam":"Alex Kiam","albertwj":"Albert Lee","diane8":"Diane Lee","jackylin":"Jacky Lin","samzliu":"Samuel Liu","sliu2022":"Stella Liu","jmunoz8":"Jaime Munoz Jr.","misatonk":"Misato Nakayama","lneise":"Luke Neise","sanvar":"Sanvar Oberoi","sraches":"Steven Rachesky","ramayya":"Sulekha Pamayya","lukeren":"Luke Ren","ninasab":"Nina Sabharwal","kshah1":"Kevin Shah","fsa":"Frances Simpson-Allen","dss93":"David Steiner","sunilrao":"Sunil Sudhakaran","yalew":"Yale Wang","cjmeerst":"Charlotte Meerstadt","mitra":"Mirta","atwell":"Prof. Atwell","clide":"Chelsea Lide (CA)","lizixin":"Lambert Li (CA)","extra_01":"Unnamed #1","extra_02":"Unnamed #2","extra_03":"Unnamed #3","extra_04":"Unnamed #4","extra_05":"Unnamed #5","extra_06":"Unnamed #6"}


class IntroWaitPage(WaitPage):
    group_by_arrival_time = True

    def vars_for_template(self):
        return {"title_text": "Hang tight", "body_text":"Please wait a moment to get paired.\n\nIf you've been on this page for a while, try refreshing the page or flagging down Dr. Atwell."}


class Introduction(Page):
    form_model = "player"

    def before_next_page(self):
        try:
            self.participant.vars["SUNet"] = self.participant.label
            self.participant.vars["name"] = SUNet_to_name[self.participant.label]
        except:
            self.participant.vars["SUNet"] = "none"
            self.participant.vars["name"] = "(come see Dr. Atwell)"

        self.player.name = self.participant.vars["name"]

    def vars_for_template(self):
        total_time = Constants.reading_time + Constants.planning_doc_time_minutes + Constants.negotiating_time + 5
        return {"reading_limit":Constants.reading_time,"total_time":total_time,"planning_doc_time":Constants.planning_doc_time_minutes}


class Meeting_location(Page):
    form_model = "player"

    def vars_for_template(self):
            return {"zoom_link":self.participant.vars["zoom_link"], "pdf_file":"global/OutdoorMap.pdf"}


class Stanfield_materials(Page):
    form_model = "player"

    timeout_seconds= Constants.reading_time * 60
    timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return {"pdf_file":"NoCode/Stanfield.pdf","xlsx_file":"NoCode/Stanfield Point System.xlsx"}


class Sproles_materials(Page):
    form_model = "player"

    timeout_seconds= Constants.reading_time * 60
    timer_text = 'Time left for reading the materials'


    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        return {"pdf_file": "NoCode/Sproles.pdf","xlsx_file":"NoCode/Sproles Point System.xlsx"}


class Target_input(Page):
    form_model = "player"
    form_fields = ['target_points']

    timeout_seconds= 120
    timer_text = 'Time left to input values'

    def vars_for_template(self):
        if self.player.id_in_group == 1:
            return {"pdf_file": "NoCode/Stanfield.pdf","xlsx_file":"NoCode/Stanfield Point System.xlsx"}
        if self.player.id_in_group == 2:
            return {"pdf_file": "NoCode/Sproles.pdf","xlsx_file":"NoCode/Sproles Point System.xlsx"}


class Planning_doc(Page):
    form_model = "player"
    form_fields = ["planning_text"]

    timeout_seconds= Constants.planning_doc_time_minutes * 60
    timer_text = 'Time left for writing your document:'

    def vars_for_template(self):
        if self.player.id_in_group == 1:
            return {"pdf_file": "NoCode/Stanfield.pdf","max_word_limit":Constants.planning_doc_length,"xlsx_file":"NoCode/Stanfield Point System.xlsx"}
        if self.player.id_in_group == 2:
            return {"pdf_file": "NoCode/Sproles.pdf","max_word_limit":Constants.planning_doc_length,"xlsx_file":"NoCode/Sproles Point System.xlsx"}


class Meeting_location_reminder(Page):
    form_model = "player"

    def vars_for_template(self):
            partner = self.player.get_others_in_group()[0]
            self.player.partner = partner.participant.vars["name"]
            if self.player.id_in_group ==1:
                self.player.grole = "Stanfield"
            else:
                self.player.grole = "Sproles"

            return {"negotiating_time":Constants.negotiating_time,"partner":partner.participant.vars["name"] }



class Meeting_wait(WaitPage):
    form_model = "group"
    after_all_players_arrive = 'set_timer'

    def vars_for_template(self):
            return {"title_text":"Waiting...","body_text":"We're waiting for your counterparty to be ready. Once they finish up, you'll go back to the case materials page and the timed negotiation will begin."}


class Stanfield_materials_no_timer(Page):
    form_model = "player"

    template_name = "NoCode/Stanfield_materials.html"

    timeout_seconds= Constants.negotiation_time * 60
    timer_text = 'Time left to negotiate the case'

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return {"pdf_file": "NoCode/Stanfield.pdf","xlsx_file":"NoCode/Stanfield Point System.xlsx"}


class Sproles_materials_no_timer(Page):
    form_model = "player"
    template_name = "NoCode/Sproles_materials.html"

    timeout_seconds= Constants.negotiation_time * 60
    timer_text = 'Time left to negotiate the case'

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        return {"pdf_file": "NoCode/Sproles.pdf","xlsx_file":"NoCode/Sproles Point System.xlsx"}


class Negotiated_outcome_one(Page):

    form_model = "group"
    form_fields = ["deal"]

    def is_displayed(self):
        return self.player.id_in_group == 2


class Negotiated_outcome_two(Page):

    form_model = "group"

    def get_form_fields(self):
        if self.group.deal:
            return ["Salary", "Bonus","Equity","Days","Start"]
        else:
            return ["last_Salary_Stanfield","last_Bonus_Stanfield","last_Equity_Stanfield","last_Days_Stanfield","last_Start_Stanfield","last_Salary_Sproles","last_Bonus_Sproles","last_Equity_Sproles","last_Days_Sproles","last_Start_Sproles"]

    def is_displayed(self):
        return self.player.id_in_group == 2


class Outcome_wait(WaitPage):
    form_model = "group"

    form_fields = ["nego_time"]

    def vars_for_template(self):
        if self.player.id_in_group == 1:
            return {"title_text": "Reporting the outcome", "body_text":"Wait a moment while Sproles finishes inputting the results.\n\n"}
        else:
            return {"title_text": "Waiting", "body_text":"Wait a moment for both parties to advance.\n\n"}


class Sign_off_page(Page):
    form_model = "group"

    def before_next_page(self):
        bio = self.group.get_player_by_id(2)
        self.group.nego_time = int(time.time() - bio.participant.vars["sim_start"])

class Finished_case(Page):
    form_model = "group"


class Journaling_page(Page):
    form_model = "player"

    form_fields = ["journaling_text"]

    def vars_for_template(self):
        if self.player.id_in_group == 1:
            return {"pdf_file": "NoCode/Stanfield.pdf","xlsx_file":"NoCode/Stanfield Point System.xlsx"}
        if self.player.id_in_group == 2:
            return {"pdf_file": "NoCode/Sproles.pdf","xlsx_file":"NoCode/Sproles Point System.xlsx"}


class Outro(Page):
    form_model = "group"





page_sequence = [IntroWaitPage, Introduction, Sproles_materials, Stanfield_materials, Planning_doc, Target_input, Meeting_wait, Meeting_location_reminder, Sproles_materials_no_timer, Stanfield_materials_no_timer,Negotiated_outcome_one, Negotiated_outcome_two, Outcome_wait,Finished_case, Journaling_page, Outro]
