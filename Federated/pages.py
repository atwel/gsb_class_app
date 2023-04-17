from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

SUNet_to_name = {'fredaddy':'Fred Addy', 'aabd':'Armando Alejandro Borda', 'zakb':'Zak Budden', 'connorca':'Connor Callaway', 'acohen22':'Adam Scott Cohen', 'annafilo':'Anna Filochowska', 'wf539':'Wanning Fu', 'shreyaa':'Shreya Gupta', 'lhaffer':'Lukas Haffer', 'sehughes':'Sarah Hughes', 'skawatra':'Srishti Kawatra', 'dkhar22':'David Kharatishvili', 'yooekim':'Yoo Eun Kim', 'nskolber':'Natalie Sarah Kolber', 'kompalla':'Julia Franziska Kompalla', 'lask1952':'Alexis Misha Laskowski', 'qixuanli':'Qixuan Li', 'jackfm':'Jack Francis Michaels', 'traje':'Tanvi Nikita Vikas Raje', 'cregan7':'Connor Regan', 'erose4':'Ethan Rose', 'tomrose':'Tom Stern Rosenblatt', 'isabate':'Ignacio Sabaté', 'nschlein':'Nate Schlein', 'skrobach':'Mykhailo Skrobach', 'stanstic':'Stanford Stickney', 'suwimana':'Sandy Uwimana', 'markwhit':'Mark Robert Whittaker', 'grayy':'Gray Scott Young', 'drharris':'david harris', 'ipshita9':'Ipshita Agarwal', 'ioannaa':'Ioanna Aguilar', 'piali':'Piali Bopanna', 'ncable':'Nik Cable', 'cycampos':'Cheryl Campos', 'schang63':'Samuel C Chang', 'amanc2':'Aman Chaudhary', 'julietc1':'Juliet Choi', 'ccranmer':'Caitlin Cranmer', 'jdumiak':'Jen Dumiak', 'sdunau':'Shane Nicole Dunau', 'nflanary':'Nicole Flanary', 'ssfree':'Sarah Seaborn Freeman', 'cegarcia':'Catalina Eugenia Garcia Gajardo', 'egetty':'Erin Getty', 'amholt':'Mandy Holt', 'blaireym':'Blaire Huang', 'harshitk':'Harshit Kohli', 'jkubert':'Jon Kubert', 'mliamos':'Michael Charles Liamos', 'lyliang':'Lyanne Liang', 'jdlorenz':'Jonathon Lorenz', 'irfanx':'Irfan Mahmud', 'mmallah':'Mariama Mallah', 'mhmann':'Myles Mann', 'martyj':'Jason Marty', 'minali':'Minali Mohindra', 'toure':'Toure Kwame Owen', 'jonpeder':'Jonathan Pedersen', 'mikepeng':'Mike Peng', 'woodsrp':'Woods Preechawit', 'craiff':'Clay Raiff', 'juromero':'Julieta Aldana Romero', 'jpsand95':'Juan Pablo Sandoval Celis', 'csapan':'Claire Sapan', 'msauvage':'Michael Sauvage', 'jhstyles':'John Henry Styles', 'darrenjt':'Darren Tan', 'mtw693':'Marshall Thomas Watkins', 'emwaxman':'Emily Waxman', 'liawe':'Lia Michal Weiner', 'fangfeiy':'Fangfei Yin', 'aleksz':'Aleksandar Zdravkovski', 'shaden':'Shaden Alsheik', 'aamdekar':'Atharva Amdekar', 'beattymg':'Matt Beatty', 'zachboy':'Zach Boyette', 'ychoi24':'Young Choi', 'rdensley':'Rachel Densley', 'elaine24':'Elaine Fang', 'jierui':'Jierui Fang', 'alisdair':'Alisdair Ferguson', 'tgerrard':'Tye Gerrard', 'whoran':'Wyatt Horan', 'jchwang':'Jennifer C. Hwang', 'nitikaj':'Nitika Johri', 'diegollm':'Diego Lloreda Martín', 'mmadding':'Michael Madding', 'alvarom':'Alvaro Marin Melero', 'amedina8':'Antonio Rafael Medina Perez', 'emuco':'Evi Muco', 'amurtlan':'Andrew Murtland', 'roakley1':'Rae Oakley', 'danpil':'Dan Pilewski', 'epowers2':'Emily Powers', 'mschein':'Mara Gabrielle Schein', 'jserra':'Julian Jaime Serra', 'jsharma3':'Jigyasa Sharma', 'socarras':'Esteban Socarras', 'dwagura':'David Wangombe Wagura', 'gwatsham':'Ginny Watsham', 'lgwhite':'Louise White', 'fangting':'Angela Wu', 'yuchenz':'Yuchen Zou', 'decarlos':'Iñigo de Carlos Artajo',"extra1":"Unnamed #1","extra2":"Unnamed #2","extra3":"Unnamed #3","extra4":"Unnamed #4","extra5":"Unnamed #5","extra6":"Unnamed #6","extra7":"Unnamed #7","extra8":"Unnamed #8","extra9":"Unnamed #9","extra10":"Unnamed #10"}


class IntroWaitPage(WaitPage):
    group_by_arrival_time = True

    def vars_for_template(self):
        return {"title_text": "Waiting for others", "body_text":"Please wait a moment while you're assigned to a group.\n\n"}


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


class Stockman(Page):
    form_model = "player"

    #timeout_seconds = Constants.reading_time*60
    #timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.role() == "stockman"

    def vars_for_template(self):
        return {"pdf_file": "Federated/Stockman.pdf","End_time":"","show_end_time":False}

    def js_vars(self):
        return dict(button_show=Constants.material_button_show*60000)


class Stockman_nt(Page):
    form_model = "player"

    template_name = "Federated/Stockman.html"


    def is_displayed(self):
        return self.player.role() == "stockman"

    def vars_for_template(self):
        return {"pdf_file": "Federated/Stockman.pdf","End_time":self.group.end_time,"show_end_time":False}

    def js_vars(self):
        return dict(button_show=Constants.material_button_show*60000)


class Turbo(Page):
    form_model = "player"

    #timeout_seconds = Constants.reading_time*60
    #timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.role() == "turbo"

    def vars_for_template(self):
        return {"pdf_file": "Federated/Turbo.pdf","End_time":"","show_end_time":False}

    def js_vars(self):
        return dict(button_show=Constants.material_button_show*60000)


class Turbo_nt(Page):
    form_model = "player"

    template_name = "Federated/Turbo.html"

    def is_displayed(self):
        return self.player.role() == "turbo"

    def vars_for_template(self):
        return {"pdf_file": "Federated/Turbo.pdf","End_time":self.group.end_time,"show_end_time":False}

    def js_vars(self):
        return dict(button_show=Constants.material_button_show*60000)


class United(Page):
    form_model = "player"

    #timeout_seconds = Constants.reading_time*60
    #timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.role() == "united"

    def vars_for_template(self):
        return {"pdf_file": "Federated/United.pdf","End_time":"","show_end_time":False}

    def js_vars(self):
        return dict(button_show=Constants.material_button_show*60000)


class United_nt(Page):
    form_model = "player"

    template_name = "Federated/United.html"

    def is_displayed(self):
        return self.player.role() == "united"

    def vars_for_template(self):
        return {"pdf_file": "Federated/United.pdf","End_time":self.group.end_time,"show_end_time":False}

    def js_vars(self):
        return dict(button_show=Constants.material_button_show*60000)



class Planning_doc(Page):
    form_model = "player"
    #form_fields = ["planning_text"]

    #timeout_seconds = Constants.planning_doc_time *60
    #timer_text = "Time left to finish the planning document"

    def vars_for_template(self):
        if self.player.role() == "stockman":
            return {"pdf_file": "Federated/Stockman.pdf"}
        elif self.player.role() == "turbo":
            return {"pdf_file": "Federated/Turbo.pdf"}
        elif self.player.role() == "united":
            return {"pdf_file": "Federated/United.pdf"}


class Ready_for_class(Page):
    form_model = "player"

class Wait_to_negotiate(WaitPage):
    form_model = "group"

    def vars_for_template(self):
        return {"title_text": "Waiting for your counterparts to finish preparing", "body_text":"It shouldn't be too long now!\n\n"}


class Back_to_class(Page):
    form_model = "player"

    def before_next_page(self):
        if not self.group.started:
            self.group.set_end_time()

    def vars_for_template(self):
        partners = self.player.get_others_in_group()
        part_1 = partners[0].name
        part_2 = partners[1].name

        if self.group.stockman:
            if self.player.role() == "united":
                return {"rep": "United", "alter":"Stockman", "in_first":True, "partner_1":part_1, "partner_2":part_2}
            elif self.player.role() == "stockman":
                return {"alter": "United", "rep":"Stockman", "in_first":True, "partner_1":part_1, "partner_2":part_2}
            else:
                return {"rep": "Turbo", "alter":"NA", "in_first":False, "partner_1":part_1, "partner_2":part_2}
        else:
            if self.player.role() == "united":
                return {"rep": "United", "alter":"Turbo", "in_first":True, "partner_1":part_1, "partner_2":part_2}
            elif self.player.role() == "turbo":
                return {"alter": "United", "rep":"Turbo", "in_first":True, "partner_1":part_1, "partner_2":part_2}
            else:
                return {"rep": "Stockman", "alter":"NA", "in_first":False, "partner_1":part_1, "partner_2":part_2}



class Outcome(Page):
    form_model = "player"

    form_fields = ["united","stockman","turbo","first_meeting"]



class Journaling_page(Page):
    form_model = "player"

    #form_fields = ["journaling_text"]

    #timeout_seconds = Constants.reflection_time*60


class Outro(Page):
    form_model = "group"


page_sequence = [Introduction, Stockman, Turbo, United, Planning_doc, Ready_for_class, Wait_to_negotiate, Back_to_class, Stockman_nt, Turbo_nt, United_nt, Outcome, Journaling_page, Outro]
