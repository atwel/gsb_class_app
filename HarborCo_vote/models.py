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

with open("_rooms/Sp22_01.txt", "r") as f:
    raw_string = f.read()
    names_section1 = raw_string.split("\n")
    #names_section1.pop()

with open("_rooms/Sp22_02.txt", "r") as f:
    raw_string = f.read()
    names_section2 = raw_string.split("\n")
    #names_section2.pop()

with open("_rooms/Sp22_03.txt", "r") as f:
    raw_string = f.read()
    names_section3 = raw_string.split("\n")
    #names_section3.pop()

SUNet_to_name = {"oakkurt":"Ozlem Akkurt","sarahand":"Sarah Anderson","sankalpb":"Sankalp Banerjee","abertha":"Andrew Bertha","jhbuchel":"Jason Buchel","daviscm":"Carolyn Davis","mdicou":"Matt Dicou","dhfranks":"David Franks","jigs":"Jose Garcia Suarez","kgea":"Kathy Gea","ehuscher":"Elspeth Huscher","yvj":"Yash Jain","mlamdan":"Matan Lamdan","cdlince":"Carly Lincenberg","asmartin":"Anne-Sophie Martin","kmodukan":"Kesaobaka Modukanele","povalleb":"Pablo Ovalle","spatarca":"Santiago Patarca","leilap":"Leila Pirbay","kpolle":"Karen Polle","pretes":"Paola Petes Pineda","drichey":"Dan Rickey","wrodrig":"Wes Rodriguez","jrowley":"Josh Rowley","nishaad":"Nishaad Ruparel","juansaez":"Juan Saez Vera","talsarig":"Tal Sarig","nschlein":"Nate Schlein","mariasw":"Maria Silva Willson","kstein10":"Kate Steinman","tstone":"Thomas Stone","ianas":"Iana Stoytcheva","tejsun":"Tejas Sundaresan","mtakasak":"Midori Takasaki","stopper":"Sydni Topper","tjwater":"Tanner Waterstreet","eview":"Evie Woodforde","mzxie":"Michelle Xie","cqyuan":"Chris Yuan","edzhai":"Ethan Zhai","jrbz":"Justin Ziegler","taftab":"Taleha Aftab","oyinda":"Oyinda Ajayi","hajmani":"Hannah Ajmani","hrma":"Henrique Albuquerque","lallende":"Luife Allende","dalpuche":"Dominique Alpuche","annesan":"Annes An","casawa":"Chaitanya Asawa","sherb":"Sher Bhullar","jsburns":"James Burn","cc16":"Charlotte Camacho","ecambern":"Emily Cambern","iw1000":"Lucas Cheon","hamzac":"Hamza Choudery","ncole2":"Nyamekye Coleman","pcout":"Peter Coutoulas","adavis29":"Alexa Davis","sef07":"Steven Ferreira","wglick":"Whitney Glick","anna425":"Anna Gurevich","royhage":"Roy Hage","davidh7":"David Harrison","rbhuang":"Richard Huang","jh21":"Jonathan Hurowitz","andyjin":"Andy Jin","mjuzwiak":"Monika Juzwiak","hkling":"Henry Klingenstein","macklee":"Mackenzie Lee","levinelu":"Lucas Levine","natm":"Natalie Meurer","cliffmil":"Cliff Miller","jmorton4":"Jackson Morton","karlyosb":"Karly Osborne","playfair":"Katherine Playfair","yploder":"Yvonne Ploder","eportura":"Eliann Porturas","psaength":"Phanthila Saengthong","jsayadi":"Jamasb Sayadi","jeremycs":"Jeremy Scott","sheldon3":"Casey Sheldon","amys2023":"Amy Marie Slaughter","nsuchato":"Prao Suchato","m2taylor":"Margot Taylor","wilkinsj":"Jonathan Wilkins","kwolsten":"Kyle Wolstencroft","mzincone":"Michael Zincone","anibaldf":"Anibal de Frankenberg","tracycao":"Tracy Cao","amanc2":"Aman Chaudhary","crozelcm":"Claire Crozel","vdivi":"Vasu Divi","fadavi":"Faraz Fadavi","jhamying":"Julien Ham-Ying","shasson":"Sophie Hasson","srkarr":"S Karr","nkasper":"Nolan Kasper","bkhoo":"Bryan Khoo","akiam":"Alex Kiam","albertwj":"Albert Lee","diane8":"Diane Lee","jackylin":"Jacky Lin","samzliu":"Samuel Liu","sliu2022":"Stella Liu","jmunoz8":"Jaime Munoz Jr.","misatonk":"Misato Nakayama","lneise":"Luke Neise","sanvar":"Sanvar Oberoi","sraches":"Steven Rachesky","ramayya":"Sulekha Pamayya","lukeren":"Luke Ren","ninasab":"Nina Sabharwal","kshah1":"Kevin Shah","fsa":"Frances Simpson-Allen","dss93":"David Steiner","sunilrao":"Sunil Sudhakaran","yalew":"Yale Wang","cjmeerst":"Charlotte Meerstadt","mitra":"Mirta","atwell":"Prof. Atwell","clide":"Chelsea Lide (CA)","lizixin":"Lambert Li (CA)","extra_01":"Unnamed #1","extra_02":"Unnamed #2","extra_03":"Unnamed #3","extra_04":"Unnamed #4","extra_05":"Unnamed #5","extra_06":"Unnamed #6"}



class Constants(BaseConstants):
    name_in_url = 'Voting'
    players_per_group = 6
    num_rounds = 10
    SUNet_to_name = SUNet_to_name

    names_section1 = names_section1
    names_section2 = names_section2
    names_section3 = names_section3


class Subsession(BaseSubsession):

    def before_session_starts(self):

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
