from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

SUNet_to_name = {'fredaddy':'Fred Addy', 'aabd':'Armando Alejandro Borda', 'zakb':'Zak Budden', 'connorca':'Connor Callaway', 'acohen22':'Adam Scott Cohen', 'annafilo':'Anna Filochowska', 'wf539':'Wanning Fu', 'shreyaa':'Shreya Gupta', 'lhaffer':'Lukas Haffer', 'sehughes':'Sarah Hughes', 'skawatra':'Srishti Kawatra', 'dkhar22':'David Kharatishvili', 'yooekim':'Yoo Eun Kim', 'nskolber':'Natalie Sarah Kolber', 'kompalla':'Julia Franziska Kompalla', 'lask1952':'Alexis Misha Laskowski', 'qixuanli':'Qixuan Li', 'jackfm':'Jack Francis Michaels', 'traje':'Tanvi Nikita Vikas Raje', 'cregan7':'Connor Regan', 'erose4':'Ethan Rose', 'tomrose':'Tom Stern Rosenblatt', 'isabate':'Ignacio Sabaté', 'nschlein':'Nate Schlein', 'skrobach':'Mykhailo Skrobach', 'stanstic':'Stanford Stickney', 'suwimana':'Sandy Uwimana', 'markwhit':'Mark Robert Whittaker', 'grayy':'Gray Scott Young', 'drharris':'david harris', 'ipshita9':'Ipshita Agarwal', 'ioannaa':'Ioanna Aguilar', 'piali':'Piali Bopanna', 'ncable':'Nik Cable', 'cycampos':'Cheryl Campos', 'schang63':'Samuel C Chang', 'amanc2':'Aman Chaudhary', 'julietc1':'Juliet Choi', 'ccranmer':'Caitlin Cranmer', 'jdumiak':'Jen Dumiak', 'sdunau':'Shane Nicole Dunau', 'nflanary':'Nicole Flanary', 'ssfree':'Sarah Seaborn Freeman', 'cegarcia':'Catalina Eugenia Garcia Gajardo', 'egetty':'Erin Getty', 'amholt':'Mandy Holt', 'blaireym':'Blaire Huang', 'harshitk':'Harshit Kohli', 'jkubert':'Jon Kubert', 'mliamos':'Michael Charles Liamos', 'lyliang':'Lyanne Liang', 'jdlorenz':'Jonathon Lorenz', 'irfanx':'Irfan Mahmud', 'mmallah':'Mariama Mallah', 'mhmann':'Myles Mann', 'martyj':'Jason Marty', 'minali':'Minali Mohindra', 'toure':'Toure Kwame Owen', 'jonpeder':'Jonathan Pedersen', 'mikepeng':'Mike Peng', 'woodsrp':'Woods Preechawit', 'craiff':'Clay Raiff', 'juromero':'Julieta Aldana Romero', 'jpsand95':'Juan Pablo Sandoval Celis', 'csapan':'Claire Sapan', 'msauvage':'Michael Sauvage', 'jhstyles':'John Henry Styles', 'darrenjt':'Darren Tan', 'mtw693':'Marshall Thomas Watkins', 'emwaxman':'Emily Waxman', 'liawe':'Lia Michal Weiner', 'fangfeiy':'Fangfei Yin', 'aleksz':'Aleksandar Zdravkovski', 'shaden':'Shaden Alsheik', 'aamdekar':'Atharva Amdekar', 'beattymg':'Matt Beatty', 'zachboy':'Zach Boyette', 'ychoi24':'Young Choi', 'rdensley':'Rachel Densley', 'elaine24':'Elaine Fang', 'jierui':'Jierui Fang', 'alisdair':'Alisdair Ferguson', 'tgerrard':'Tye Gerrard', 'whoran':'Wyatt Horan', 'jchwang':'Jennifer C. Hwang', 'nitikaj':'Nitika Johri', 'diegollm':'Diego Lloreda Martín', 'mmadding':'Michael Madding', 'alvarom':'Alvaro Marin Melero', 'amedina8':'Antonio Rafael Medina Perez', 'emuco':'Evi Muco', 'amurtlan':'Andrew Murtland', 'roakley1':'Rae Oakley', 'danpil':'Dan Pilewski', 'epowers2':'Emily Powers', 'mschein':'Mara Gabrielle Schein', 'jserra':'Julian Jaime Serra', 'jsharma3':'Jigyasa Sharma', 'socarras':'Esteban Socarras', 'dwagura':'David Wangombe Wagura', 'gwatsham':'Ginny Watsham', 'lgwhite':'Louise White', 'fangting':'Angela Wu', 'yuchenz':'Yuchen Zou', 'decarlos':'Iñigo de Carlos Artajo',"extra1":"Unnamed #1","extra2":"Unnamed #2","extra3":"Unnamed #3","extra4":"Unnamed #4","extra5":"Unnamed #5","extra6":"Unnamed #6","extra7":"Unnamed #7","extra8":"Unnamed #8","extra9":"Unnamed #9","extra10":"Unnamed #10"}

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

class DTV(Page):
    form_model = "player"

    #timeout_seconds= Constants.reading_time * 60
    #timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.role() == "3dtv"

    def vars_for_template(self):
        return {"pdf_file": "OmniChannel/3DTV.pdf"}

class Omni(Page):
    form_model = "player"

    #timeout_seconds= Constants.reading_time * 60
    #timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.role() == "omni"

    def vars_for_template(self):
        return {"pdf_file": "OmniChannel/OmniChannel.pdf"}

class Message_DTV(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.role() == "3dtv"

class Message_OC(Page):
    form_model = "player"

    def is_displayed(self):
        return self.player.role() == "omni"

class Planning_doc(Page):
    form_model = "player"

    #timeout_seconds= Constants.planning_doc_time * 60
    #timer_text = 'Time left to finish writing your planning document'

    def vars_for_template(self):
        if self.player.role() == "3dtv":
            return {"pdf_file": "OmniChannel/3DTV.pdf","assignment_url":"https://canvas.stanford.edu/courses/173725/assignments/514474"}
        elif self.player.role() == "omni":
            return {"pdf_file": "OmniChannel/OmniChannel.pdf","assignment_url":"https://canvas.stanford.edu/courses/173725/assignments/514474"}

class Wait_until_open(Page):
    form_model = "player"
    #remove  next line when not demo-ing
    #timeout_seconds = 10

class Agreement(Page):
    form_model = "player"
    form_fields = ["agreement"]

    def is_displayed(self):
        if self.player.role() =="3dtv":
            return True
        else:
            return False

class Outcome(Page):
    form_model = "player"
    form_fields = ["data","license_restrictions","premium_count","premium_fees","regular_count","regular_fees","data_center_fees","length","termination"]

    def is_displayed(self):
        if self.player.role() =="3dtv" and self.player.agreement =="Yes":
            return True
        else:
            return False


class Journaling_page(Page):
    form_model = "player"

    def vars_for_template(self):
        return {"assignment_url":"https://canvas.stanford.edu/courses/173725/assignments/514475"}

class Outro(Page):
    form_model = "group"


page_sequence = [Introduction, DTV, Omni, Message_DTV, Message_OC, Planning_doc, Wait_until_open, DTV, Omni, Agreement,Outcome, Journaling_page, Outro]
