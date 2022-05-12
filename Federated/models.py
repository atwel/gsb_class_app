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
import datetime
import itertools

author = 'Jon Atwell'

doc = """
Negotiating Federated Sciences with two partners
"""

SUNet_to_name = {"oakkurt":"Ozlem Akkurt","sarahand":"Sarah Anderson","sankalpb":"Sankalp Banerjee","abertha":"Andrew Bertha","jhbuchel":"Jason Buchel","daviscm":"Carolyn Davis","mdicou":"Matt Dicou","dhfranks":"David Franks","jigs":"Jose Garcia Suarez","kgea":"Kathy Gea","ehuscher":"Elspeth Huscher","yvj":"Yash Jain","mlamdan":"Matan Lamdan","cdlince":"Carly Lincenberg","asmartin":"Anne-Sophie Martin","kmodukan":"Kesaobaka Modukanele","povalleb":"Pablo Ovalle","spatarca":"Santiago Patarca","leilap":"Leila Pirbay","kpolle":"Karen Polle","pretes":"Paola Petes Pineda","drichey":"Dan Rickey","wrodrig":"Wes Rodriguez","jrowley":"Josh Rowley","nishaad":"Nishaad Ruparel","juansaez":"Juan Saez Vera","talsarig":"Tal Sarig","nschlein":"Nate Schlein","mariasw":"Maria Silva Willson","kstein10":"Kate Steinman","tstone":"Thomas Stone","ianas":"Iana Stoytcheva","tejsun":"Tejas Sundaresan","mtakasak":"Midori Takasaki","stopper":"Sydni Topper","tjwater":"Tanner Waterstreet","eview":"Evie Woodforde","mzxie":"Michelle Xie","cqyuan":"Chris Yuan","edzhai":"Ethan Zhai","jrbz":"Justin Ziegler","taftab":"Taleha Aftab","oyinda":"Oyinda Ajayi","hajmani":"Hannah Ajmani","hrma":"Henrique Albuquerque","lallende":"Luife Allende","dalpuche":"Dominique Alpuche","annesan":"Annes An","casawa":"Chaitanya Asawa","sherb":"Sher Bhullar","jsburns":"James Burn","cc16":"Charlotte Camacho","ecambern":"Emily Cambern","iw1000":"Lucas Cheon","hamzac":"Hamza Choudery","ncole2":"Nyamekye Coleman","pcout":"Peter Coutoulas","adavis29":"Alexa Davis","sef07":"Steven Ferreira","wglick":"Whitney Glick","anna425":"Anna Gurevich","royhage":"Roy Hage","davidh7":"David Harrison","rbhuang":"Richard Huang","jh21":"Jonathan Hurowitz","andyjin":"Andy Jin","mjuzwiak":"Monika Juzwiak","hkling":"Henry Klingenstein","macklee":"Mackenzie Lee","levinelu":"Lucas Levine","natm":"Natalie Meurer","cliffmil":"Cliff Miller","jmorton4":"Jackson Morton","karlyosb":"Karly Osborne","playfair":"Katherine Playfair","yploder":"Yvonne Ploder","eportura":"Eliann Porturas","psaength":"Phanthila Saengthong","jsayadi":"Jamasb Sayadi","jeremycs":"Jeremy Scott","sheldon3":"Casey Sheldon","amys2023":"Amy Marie Slaughter","nsuchato":"Prao Suchato","m2taylor":"Margot Taylor","wilkinsj":"Jonathan Wilkins","kwolsten":"Kyle Wolstencroft","mzincone":"Michael Zincone","anibaldf":"Anibal de Frankenberg","tracycao":"Tracy Cao","amanc2":"Aman Chaudhary","crozelcm":"Claire Crozel","vdivi":"Vasu Divi","fadavi":"Faraz Fadavi","jhamying":"Julien Ham-Ying","shasson":"Sophie Hasson","srkarr":"S Karr","nkasper":"Nolan Kasper","bkhoo":"Bryan Khoo","akiam":"Alex Kiam","albertwj":"Albert Lee","diane8":"Diane Lee","jackylin":"Jacky Lin","samzliu":"Samuel Liu","sliu2022":"Stella Liu","jmunoz8":"Jaime Munoz Jr.","misatonk":"Misato Nakayama","lneise":"Luke Neise","sanvar":"Sanvar Oberoi","sraches":"Steven Rachesky","ramayya":"Sulekha Pamayya","lukeren":"Luke Ren","ninasab":"Nina Sabharwal","kshah1":"Kevin Shah","fsa":"Frances Simpson-Allen","dss93":"David Steiner","sunilrao":"Sunil Sudhakaran","yalew":"Yale Wang","cjmeerst":"Charlotte Meerstadt","atwell":"Prof. Atwell","clide":"Chelsea Lide (CA)","lizixin":"Lambert Li (CA)","extra_01":"Unnamed #1","extra_02":"Unnamed #2","extra_03":"Unnamed #3","extra_04":"Unnamed #4","extra_05":"Unnamed #5","extra_06":"Unnamed #6"}


class Constants(BaseConstants):
    name_in_url = 'Federated_Sciences'
    players_per_group = 3
    num_rounds = 1

    reading_time = 10 #minutes
    material_button_show= 2 #minutes
    planning_doc_time = 10 # minutes
    negotiating_time = 30 # minutes
    reflection_time  = 5 # minutes

    planning_doc_length = 100 #words


class Subsession(BaseSubsession):

    def creating_session(self):
        stock = itertools.cycle([True, False])
        for g in self.get_groups():
            g.stockman = next(stock)

    def vars_for_admin_report(self):
        stockman = []
        united = []
        turbo = []

        for p in self.get_players():
            the_label = p.participant.vars["name"]
            if p.role() == "stockman":
                stockman.append(the_label)
            elif p.role() == "turbo":
                turbo.append(the_label)
            else:
                united.append(the_label)


        return {"Stockman":stockman,"Turbo":turbo,"United":united}

class Group(BaseGroup):
    stockman = models.BooleanField()
    pairing = models.StringField()
    end_time = models.StringField()

    def set_end_time(self):
        self.end_time = (datetime.datetime.now() + datetime.timedelta(minutes=Constants.negotiating_time + 1)).strftime("%H:%M:%S")

    def set_first_meet(self):
        for i, p in enumerate(self.get_players()):
            try:
                p.name = SUNet_to_name[p.participant.label]
            except:
                p.name = "Demo_{}".format(i)

        for p in self.get_players():
            if p.role() == "stockman":
                stockman = p.name
            elif p.role() == "turbo":
                turbo = p.name
            else:
                united = p.name

        if self.stockman:
            self.pairing = ",".join([united, stockman, turbo])
        else:
            self.pairing = ",".join([united, turbo, stockman])


class Player(BasePlayer):
    name = models.StringField()

    planning_text = models.LongStringField(label="Describe your plan for this negotiation. In particular, how do intend to approach dealing with coalitions?")

    united = models.IntegerField()
    turbo = models.IntegerField()
    stockman= models.IntegerField()
    first_meeting = models.StringField(label="Who did Turbo start the negotiation with?",choices=["Stockman","United","Both"], widget=widgets.RadioSelectHorizontal)

    journaling_text = models.LongStringField(label="Please describe your experience of the negotiation.")


    def role(self):
        if self.id_in_group == 1:
            return 'stockman'
        elif self.id_in_group == 2:
            return 'turbo'
        else:
            return 'united'
