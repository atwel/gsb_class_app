from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import random


author = 'Jon Atwell'

doc = """
Voting platform for HarborCo
"""

with open("_rooms/Sp23_01.txt", "r") as f:
    raw_string = f.read()
    names_section1 = raw_string.split("\n")
    #names_section1.pop()

with open("_rooms/Sp23_02.txt", "r") as f:
    raw_string = f.read()
    names_section2 = raw_string.split("\n")
    #names_section2.pop()

with open("_rooms/Sp23_03.txt", "r") as f:
    raw_string = f.read()
    names_section3 = raw_string.split("\n")
    #names_section3.pop()

SUNet_to_name = {'fredaddy':'Fred Addy', 'aabd':'Armando Alejandro Borda', 'zakb':'Zak Budden', 'connorca':'Connor Callaway', 'acohen22':'Adam Scott Cohen', 'annafilo':'Anna Filochowska', 'wf539':'Wanning Fu', 'shreyaa':'Shreya Gupta', 'lhaffer':'Lukas Haffer', 'sehughes':'Sarah Hughes', 'skawatra':'Srishti Kawatra', 'dkhar22':'David Kharatishvili', 'yooekim':'Yoo Eun Kim', 'nskolber':'Natalie Sarah Kolber', 'kompalla':'Julia Franziska Kompalla', 'lask1952':'Alexis Misha Laskowski', 'qixuanli':'Qixuan Li', 'jackfm':'Jack Francis Michaels', 'traje':'Tanvi Nikita Vikas Raje', 'cregan7':'Connor Regan', 'erose4':'Ethan Rose', 'tomrose':'Tom Stern Rosenblatt', 'isabate':'Ignacio Sabaté', 'nschlein':'Nate Schlein', 'skrobach':'Mykhailo Skrobach', 'stanstic':'Stanford Stickney', 'suwimana':'Sandy Uwimana', 'markwhit':'Mark Robert Whittaker', 'grayy':'Gray Scott Young', 'drharris':'david harris', 'ipshita9':'Ipshita Agarwal', 'ioannaa':'Ioanna Aguilar', 'piali':'Piali Bopanna', 'ncable':'Nik Cable', 'cycampos':'Cheryl Campos', 'schang63':'Samuel C Chang', 'amanc2':'Aman Chaudhary', 'julietc1':'Juliet Choi', 'ccranmer':'Caitlin Cranmer', 'jdumiak':'Jen Dumiak', 'sdunau':'Shane Nicole Dunau', 'nflanary':'Nicole Flanary', 'ssfree':'Sarah Seaborn Freeman', 'cegarcia':'Catalina Eugenia Garcia Gajardo', 'egetty':'Erin Getty', 'amholt':'Mandy Holt', 'blaireym':'Blaire Huang', 'harshitk':'Harshit Kohli', 'jkubert':'Jon Kubert', 'mliamos':'Michael Charles Liamos', 'lyliang':'Lyanne Liang', 'jdlorenz':'Jonathon Lorenz', 'irfanx':'Irfan Mahmud', 'mmallah':'Mariama Mallah', 'mhmann':'Myles Mann', 'martyj':'Jason Marty', 'minali':'Minali Mohindra', 'toure':'Toure Kwame Owen', 'jonpeder':'Jonathan Pedersen', 'mikepeng':'Mike Peng', 'woodsrp':'Woods Preechawit', 'craiff':'Clay Raiff', 'juromero':'Julieta Aldana Romero', 'jpsand95':'Juan Pablo Sandoval Celis', 'csapan':'Claire Sapan', 'msauvage':'Michael Sauvage', 'jhstyles':'John Henry Styles', 'darrenjt':'Darren Tan', 'mtw693':'Marshall Thomas Watkins', 'emwaxman':'Emily Waxman', 'liawe':'Lia Michal Weiner', 'fangfeiy':'Fangfei Yin', 'aleksz':'Aleksandar Zdravkovski', 'shaden':'Shaden Alsheik', 'aamdekar':'Atharva Amdekar', 'beattymg':'Matt Beatty', 'zachboy':'Zach Boyette', 'ychoi24':'Young Choi', 'rdensley':'Rachel Densley', 'elaine24':'Elaine Fang', 'jierui':'Jierui Fang', 'alisdair':'Alisdair Ferguson', 'tgerrard':'Tye Gerrard', 'whoran':'Wyatt Horan', 'jchwang':'Jennifer C. Hwang', 'nitikaj':'Nitika Johri', 'diegollm':'Diego Lloreda Martín', 'mmadding':'Michael Madding', 'alvarom':'Alvaro Marin Melero', 'amedina8':'Antonio Rafael Medina Perez', 'emuco':'Evi Muco', 'amurtlan':'Andrew Murtland', 'roakley1':'Rae Oakley', 'danpil':'Dan Pilewski', 'epowers2':'Emily Powers', 'mschein':'Mara Gabrielle Schein', 'jserra':'Julian Jaime Serra', 'jsharma3':'Jigyasa Sharma', 'socarras':'Esteban Socarras', 'dwagura':'David Wangombe Wagura', 'gwatsham':'Ginny Watsham', 'lgwhite':'Louise White', 'fangting':'Angela Wu', 'yuchenz':'Yuchen Zou', 'decarlos':'Iñigo de Carlos Artajo',"extra1":"Unnamed #1","extra2":"Unnamed #2","extra3":"Unnamed #3","extra4":"Unnamed #4","extra5":"Unnamed #5","extra6":"Unnamed #6","extra7":"Unnamed #7","extra8":"Unnamed #8","extra9":"Unnamed #9","extra10":"Unnamed #10"}



class Constants(BaseConstants):
    name_in_url = 'Voting'
    players_per_group = 6
    num_rounds = 10
    SUNet_to_name = SUNet_to_name

    names_section1 = names_section1
    names_section2 = names_section2
    names_section3 = names_section3


class Subsession(BaseSubsession):

    def creating_session(self):

        if self.session.config["section_number"] == 1:
            section_labels = Constants.names_section1.copy()
        elif self.session.config["section_number"] == 2:
            section_labels = Constants.names_section2.copy()
        elif self.session.config["section_number"] == 3:
            section_labels = Constants.names_section3.copy()
        print(section_labels)
        print(len(self.get_players()), len(section_labels))
        for p in self.get_players():
            p.participant.label = section_labels.pop(0)



class Group(BaseGroup):
    mix = models.StringField(label="Industry Mix", choices=["Primarily dirty","Clean & dirty","All clean"],initial="Primarily dirty")
    eco = models.StringField(label="Ecological Impact",choices=["Some harm","Maintain & repair","Improve"], initial="Some harm")
    union = models.StringField(label="Employment Rules",choices=["Unlimited union preference","Union quota 2:1","Union quota 1:1","No union preference"], initial="No union preference")
    loan = models.StringField(label="Federal Loan", choices=["$3 Billion","$2 Billion","$1 Billion","No federal loan"],initial="$3 Billion")
    comp = models.StringField( label = "Compensation to other ports", choices=["HarborCo pays $600 million","HarborCo pays $450 million","HarborCo pays $300 million","HarborCo pays $150 million","HarborCo pays nothing"],initial="HarborCo pays nothing")

    passed = models.BooleanField(default=False)
    high_passed = models.BooleanField(default=False)
    vetoed = models.BooleanField(default=False)
    did_not_pass = models.BooleanField(default=True)
    timed_out = models.BooleanField(default=False)
    pass_displayed = models.BooleanField(default=False)
    start_time = models.FloatField()



class Player(BasePlayer):

    name = models.StringField()
    vote = models.StringField(choices=["Yes","No"], label="Would you like to vote in favor of this proposal?", initial="No")

    def role(self):
        if self.id_in_group == 1:
            return 'union'
        elif self.id_in_group == 2:
            return 'enviro'
        elif self.id_in_group == 3:
            return 'ports'
        elif self.id_in_group == 4:
            return 'dcr'
        elif self.id_in_group == 5:
            return 'gov'
        else:
            return 'harborco'
