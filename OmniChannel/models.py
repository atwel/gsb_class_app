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
Negotating OmniChannel with two teams
"""

SUNet_to_name = {"oakkurt":"Ozlem Akkurt","sarahand":"Sarah Anderson","sankalpb":"Sankalp Banerjee","abertha":"Andrew Bertha","jhbuchel":"Jason Buchel","daviscm":"Carolyn Davis","mdicou":"Matt Dicou","dhfranks":"David Franks","jigs":"Jose Garcia Suarez","kgea":"Kathy Gea","ehuscher":"Elspeth Huscher","yvj":"Yash Jain","mlamdan":"Matan Lamdan","cdlince":"Carly Lincenberg","asmartin":"Anne-Sophie Martin","kmodukan":"Kesaobaka Modukanele","povalleb":"Pablo Ovalle","spatarca":"Santiago Patarca","leilap":"Leila Pirbay","kpolle":"Karen Polle","pretes":"Paola Petes Pineda","drichey":"Dan Rickey","wrodrig":"Wes Rodriguez","jrowley":"Josh Rowley","nishaad":"Nishaad Ruparel","juansaez":"Juan Saez Vera","talsarig":"Tal Sarig","nschlein":"Nate Schlein","mariasw":"Maria Silva Willson","kstein10":"Kate Steinman","tstone":"Thomas Stone","ianas":"Iana Stoytcheva","tejsun":"Tejas Sundaresan","mtakasak":"Midori Takasaki","stopper":"Sydni Topper","tjwater":"Tanner Waterstreet","eview":"Evie Woodforde","mzxie":"Michelle Xie","cqyuan":"Chris Yuan","edzhai":"Ethan Zhai","jrbz":"Justin Ziegler","taftab":"Taleha Aftab","oyinda":"Oyinda Ajayi","hajmani":"Hannah Ajmani","hrma":"Henrique Albuquerque","lallende":"Luife Allende","dalpuche":"Dominique Alpuche","annesan":"Annes An","casawa":"Chaitanya Asawa","sherb":"Sher Bhullar","jsburns":"James Burns","cc16":"Charlotte Camacho","ecambern":"Emily Cambern","iw1000":"Lucas Cheon","hamzac":"Hamza Choudery","ncole2":"Nyamekye Coleman","pcout":"Peter Coutoulas","adavis29":"Alexa Davis","sef07":"Steven Ferreira","wglick":"Whitney Glick","anna425":"Anna Gurevich","royhage":"Roy Hage","davidh7":"David Harrison","rbhuang":"Richard Huang","jh21":"Jonathan Hurowitz","andyjin":"Andy Jin","mjuzwiak":"Monika Juzwiak","hkling":"Henry Klingenstein","macklee":"Mackenzie Lee","levinelu":"Lucas Levine","natm":"Natalie Meurer","cliffmil":"Cliff Miller","jmorton4":"Jackson Morton","karlyosb":"Karly Osborne","playfair":"Katherine Playfair","yploder":"Yvonne Ploder","eportura":"Eliann Porturas","psaength":"Mook Phanthila","jsayadi":"Jamasb Sayadi","jeremycs":"Jeremy Scott","sheldon3":"Casey Sheldon","amys2023":"Amy Marie Slaughter","nsuchato":"Prao Suchato","m2taylor":"Margot Taylor","wilkinsj":"Jonathan Wilkins","kwolsten":"Kyle Wolstencroft","mzincone":"Michael Zincone","anibaldf":"Anibal de Frankenberg","tracycao":"Tracy Cao","amanc2":"Aman Chaudhary","crozelcm":"Claire Crozel","vdivi":"Vasu Divi","fadavi":"Faraz Fadavi","jhamying":"Julien Ham-Ying","shasson":"Sophie Hasson","srkarr":"S Karr","nkasper":"Nolan Kasper","bkhoo":"Bryan Khoo","akiam":"Alex Kiam","albertwj":"Albert Lee","diane8":"Diane Lee","jackylin":"Jacky Lin","samzliu":"Samuel Liu","sliu2022":"Stella Liu","jmunoz8":"Jaime Munoz Jr.","misatonk":"Misato Nakayama","lneise":"Luke Neise","sanvar":"Sanvar Oberoi","sraches":"Steven Rachesky","ramayya":"Sulekha Ramayya","lukeren":"Luke Ren","ninasab":"Nina Sabharwal","kshah1":"Kevin Shah","fsa":"Frances Simpson-Allen","dss93":"David Steiner","sunilrao":"Sunil Sudhakaran","yalew":"Yale Wang","cjmeerst":"Charlotte Meerstadt","mitra":"Mirta","atwell":"Prof. Atwell","clide":"Chelsea Lide (CA)","lizixin":"Lambert Li (CA)","extra_01":"Unnamed #1","extra_02":"Unnamed #2","extra_03":"Unnamed #3","extra_04":"Unnamed #4","extra_05":"Unnamed #5","extra_06":"Unnamed #6"}


class Constants(BaseConstants):
    name_in_url = 'OmniChannel'
    players_per_group = 2
    num_rounds = 1
    reading_time = 15
    planning_doc_time  = 10 # minutes
    coordinating_time = 20
    negotiating_time = 60
    planning_doc_length = 100 #words


class Subsession(BaseSubsession):

    def vars_for_admin_report(self):
        omni = []
        DTV = []

        for p in self.get_players():
            if p.role() == "3dtv":
                DTV.append(p.name)
            else:
                omni.append(p.name)

        return {"DTV_ip":DTV, "Omni_ip":omni}

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    name = models.StringField()

    agreement = models.StringField(label="Did the parties reach an agreement on all 9 issues? If not, you'll skip inputting the agreement.",choices=["Yes","No"])

    data = models.StringField(label="Use of Manipulated Data", choices=["3DTV has a perpetual license to use the data for internal research.","3DTV has a license to use that for internal research during the agreement term.","3DTV cannot use manipulated data for internal research."])
    license_restrictions = models.StringField(label="Data License Restriction",choices=["3DTV can offer the content to their subscribers in 2D or 3D format.","3DTV can offer the content to their subscribers in 3D format only."])
    premium_count = models.IntegerField(label="# of Premium channels licensed",choices=[0,5,10,15,20])
    premium_fees = models.IntegerField(label="Fees for PremiumTV ($/month)", choices=[11000,12000,13000,14000,15000])
    regular_count = models.IntegerField(label="# of OC channels licensed",choices=[60,70,80,90,100])
    regular_fees = models.IntegerField(label="Fees for OC channels ($/month)", choices=[600,700,800,900,1000])
    data_center_fees = models.IntegerField(label="Fees for using 3DTV's data centers ($/month)", choices=[30000,25000,20000,15000,10000])
    length = models.IntegerField(label="Length of Agreement (years)", choices=[8,7,6,5,4])
    termination = models.IntegerField(label="Termination Options (months notice required)", choices=[12,9,6,3,1])

    planning_text = models.LongStringField(label="Describe your plan for this negotiation. In particular, how do intend to approach dealing with team members")

    journaling_text = models.LongStringField(label="Please describe your experience of the negotiation.")


    def role(self):
        try:
            self.name = SUNet_to_name[self.participant.label]
            #self.participant.label = SUNet_to_name[self.participant.label]
        except:
            pass
        if self.id_in_group == 1:
            return '3dtv'
        elif self.id_in_group == 2:
            return 'omni'
        elif self.id_in_group == 3:
            return '3dtv'
        elif self.id_in_group == 4:
            return 'omni'
        elif self.id_in_group == 5:
            return '3dtv'
        else:
            return 'omni'
