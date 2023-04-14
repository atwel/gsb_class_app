from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import time

SUNet_to_name = {'fredaddy':'Fred Addy', 'aabd':'Armando Alejandro Borda', 'zakb':'Zak Budden', 'connorca':'Connor Callaway', 'acohen22':'Adam Scott Cohen', 'annafilo':'Anna Filochowska', 'wf539':'Wanning Fu', 'shreyaa':'Shreya Gupta', 'lhaffer':'Lukas Haffer', 'sehughes':'Sarah Hughes', 'skawatra':'Srishti Kawatra', 'dkhar22':'David Kharatishvili', 'yooekim':'Yoo Eun Kim', 'nskolber':'Natalie Sarah Kolber', 'kompalla':'Julia Franziska Kompalla', 'lask1952':'Alexis Misha Laskowski', 'qixuanli':'Qixuan Li', 'jackfm':'Jack Francis Michaels', 'traje':'Tanvi Nikita Vikas Raje', 'cregan7':'Connor Regan', 'erose4':'Ethan Rose', 'tomrose':'Tom Stern Rosenblatt', 'isabate':'Ignacio Sabaté', 'nschlein':'Nate Schlein', 'skrobach':'Mykhailo Skrobach', 'stanstic':'Stanford Stickney', 'suwimana':'Sandy Uwimana', 'markwhit':'Mark Robert Whittaker', 'grayy':'Gray Scott Young', 'drharris':'david harris', 'ipshita9':'Ipshita Agarwal', 'ioannaa':'Ioanna Aguilar', 'piali':'Piali Bopanna', 'ncable':'Nik Cable', 'cycampos':'Cheryl Campos', 'schang63':'Samuel C Chang', 'amanc2':'Aman Chaudhary', 'julietc1':'Juliet Choi', 'ccranmer':'Caitlin Cranmer', 'jdumiak':'Jen Dumiak', 'sdunau':'Shane Nicole Dunau', 'nflanary':'Nicole Flanary', 'ssfree':'Sarah Seaborn Freeman', 'cegarcia':'Catalina Eugenia Garcia Gajardo', 'egetty':'Erin Getty', 'amholt':'Mandy Holt', 'blaireym':'Blaire Huang', 'harshitk':'Harshit Kohli', 'jkubert':'Jon Kubert', 'mliamos':'Michael Charles Liamos', 'lyliang':'Lyanne Liang', 'jdlorenz':'Jonathon Lorenz', 'irfanx':'Irfan Mahmud', 'mmallah':'Mariama Mallah', 'mhmann':'Myles Mann', 'martyj':'Jason Marty', 'minali':'Minali Mohindra', 'toure':'Toure Kwame Owen', 'jonpeder':'Jonathan Pedersen', 'mikepeng':'Mike Peng', 'woodsrp':'Woods Preechawit', 'craiff':'Clay Raiff', 'juromero':'Julieta Aldana Romero', 'jpsand95':'Juan Pablo Sandoval Celis', 'csapan':'Claire Sapan', 'msauvage':'Michael Sauvage', 'jhstyles':'John Henry Styles', 'darrenjt':'Darren Tan', 'mtw693':'Marshall Thomas Watkins', 'emwaxman':'Emily Waxman', 'liawe':'Lia Michal Weiner', 'fangfeiy':'Fangfei Yin', 'aleksz':'Aleksandar Zdravkovski', 'shaden':'Shaden Alsheik', 'aamdekar':'Atharva Amdekar', 'beattymg':'Matt Beatty', 'zachboy':'Zach Boyette', 'ychoi24':'Young Choi', 'rdensley':'Rachel Densley', 'elaine24':'Elaine Fang', 'jierui':'Jierui Fang', 'alisdair':'Alisdair Ferguson', 'tgerrard':'Tye Gerrard', 'whoran':'Wyatt Horan', 'jchwang':'Jennifer C. Hwang', 'nitikaj':'Nitika Johri', 'diegollm':'Diego Lloreda Martín', 'mmadding':'Michael Madding', 'alvarom':'Alvaro Marin Melero', 'amedina8':'Antonio Rafael Medina Perez', 'emuco':'Evi Muco', 'amurtlan':'Andrew Murtland', 'roakley1':'Rae Oakley', 'danpil':'Dan Pilewski', 'epowers2':'Emily Powers', 'mschein':'Mara Gabrielle Schein', 'jserra':'Julian Jaime Serra', 'jsharma3':'Jigyasa Sharma', 'socarras':'Esteban Socarras', 'dwagura':'David Wangombe Wagura', 'gwatsham':'Ginny Watsham', 'lgwhite':'Louise White', 'fangting':'Angela Wu', 'yuchenz':'Yuchen Zou', 'decarlos':'Iñigo de Carlos Artajo',"extra1":"Unnamed #1","extra2":"Unnamed #2","extra3":"Unnamed #3","extra4":"Unnamed #4","extra5":"Unnamed #5","extra6":"Unnamed #6","extra7":"Unnamed #7","extra8":"Unnamed #8","extra9":"Unnamed #9","extra10":"Unnamed #10"}


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

    #timeout_seconds= Constants.reading_time * 60
    #timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return {"pdf_file":"NoCode/Stanfield.pdf","xlsx_file":"NoCode/Stanfield Point System.xlsx"}


class Sproles_materials(Page):
    form_model = "player"

    #timeout_seconds= Constants.reading_time * 60
    #timer_text = 'Time left for reading the materials'


    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        return {"pdf_file": "NoCode/Sproles.pdf","xlsx_file":"NoCode/Sproles Point System.xlsx"}


class Target_input(Page):
    form_model = "player"
    form_fields = ['target_points']


    def vars_for_template(self):
        if self.player.id_in_group == 1:
            return {"pdf_file": "NoCode/Stanfield.pdf","xlsx_file":"NoCode/Stanfield Point System.xlsx"}
        if self.player.id_in_group == 2:
            return {"pdf_file": "NoCode/Sproles.pdf","xlsx_file":"NoCode/Sproles Point System.xlsx"}


class Planning_doc(Page):
    form_model = "player"

    #timeout_seconds= Constants.planning_doc_time_minutes * 60
    #timer_text = 'Time left for writing your document:'

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

    #timeout_seconds= Constants.negotiation_time * 60
    #timer_text = 'Time left to negotiate the case'

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return {"pdf_file": "NoCode/Stanfield.pdf","xlsx_file":"NoCode/Stanfield Point System.xlsx"}


class Sproles_materials_no_timer(Page):
    form_model = "player"
    template_name = "NoCode/Sproles_materials.html"

    #timeout_seconds= Constants.negotiation_time * 60
    #timer_text = 'Time left to negotiate the case'

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

    def vars_for_template(self):
        if self.player.id_in_group == 1:
            return {"pdf_file": "NoCode/Stanfield.pdf","xlsx_file":"NoCode/Stanfield Point System.xlsx"}
        if self.player.id_in_group == 2:
            return {"pdf_file": "NoCode/Sproles.pdf","xlsx_file":"NoCode/Sproles Point System.xlsx"}


class Outro(Page):
    form_model = "group"



page_sequence = [IntroWaitPage, Introduction, Sproles_materials, Stanfield_materials, Planning_doc, Target_input, Meeting_wait, Meeting_location_reminder, Sproles_materials_no_timer, Stanfield_materials_no_timer,Negotiated_outcome_one, Negotiated_outcome_two, Outcome_wait,Finished_case, Journaling_page, Outro]
