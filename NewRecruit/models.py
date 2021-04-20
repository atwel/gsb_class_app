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


author = 'Jon Atwell'

doc = """
Negotatiing New Recruit with a partner
"""

with open("_rooms/Sp21_01.txt", "r") as f:
    raw_string = f.read()
    names_section1 = raw_string.replace("\n", ",")

with open("_rooms/Sp21_02.txt", "r") as f:
    raw_string = f.read()
    names_section2 = raw_string.replace("\n", ",")

with open("_rooms/Sp21_03.txt", "r") as f:
    raw_string = f.read()
    names_section3 = raw_string.replace("\n", ",")

SUNet_to_name = {'atwell':"Prof. Atwell","apaza":"Adrian A (CA)","extra_01":"Unknown","extra_02":"Unknown", "extra_03":"Unknown","extra_04":"Unknown","extra_05":"Unknown","extra_06":"Unknown","aguinis":"Martin A","alokikb":"Alokik B","rbinko":"Robert B","meb277":"Mary B","gbrink":"Georgie B","obbrown":"Olivia B","schidamb":"Swathi C","whchu":"Whitney C","kimifaf":"Kimiloluwa F","kfauzie":"Kevin F","cfoote6":"Chas F","wgeorge":"Will G","afkats":"Antonie K","kparanin":"Now K","ericli1":"Eric L","monicaml":"Monica L","qlores":"Quique L","ninalu":"Nina L","roycclu":"Roy L","bencmatt":"Benjamin M","dcnugent":"Dylan N","willo":"Will O","izunna":"Izunna O","hardik":"Hardik P","nmrojas":"Nicole P","bhs":"Branden S","tlscham":"Tamar S","zsharif":"Zakaria S","mirrin":"Mirrin S","asohmshe":"Archana S","nsong":"Nancy S","cku1":"Chinedum  U","award92":"Austin W","dzanchi":"Davide Z","jrzhang1":"Jeff Z","santidb":"Santiago dB","alealvar":"Alejandra A","aanders":"Alisha A","isabel4":"sabel A","babbitt":"Andrew B","bennetta":"Alex B","mackbran":"Mackenzie B","dbujanos":"Daniel B","danranc":"Danran C","jchoi91":"Jesse C","mcreamer":"Mateo C","ndfesh":"Nicole F","nrgandhi":"Neil G","giraldo":"Mariana G","ccgong":"C.C. Gong","dhallman":"Dylan H","sagari":"Sagar I","slehman1":"Sydney L","meluck":"Mary Ellen L","kylemca":"Kyle McA","ajmccrea":"Andrew McC","amejia1":"Aly M","agmendez":"Alex M","eemiller":"Emily M","kiya":"Kiya M","pjm2022":"Peter M","nmullaji":"Nandini M","arnenm":"Arne N","wlross":"Will R","kayjs":"Kayj S","joyceshi":"Joyce S","ats2022":"Alex S","cstromey":"Christopher S","rsuarezm":"Ricky S","ssykes":"Sydney S","kylietan":"Kylie T","ptoth":"Patrick T","twiegand":"Tessa W","jzerker":"Jenna Z","stephz":"Stephanie Z","kamilali":"Kamil A","gelilab":"Gelila B","bboss":"Benjamin B","mcalvano":"Matt C","ejcbrown":"Emily C","gregcaso":"Greg C","achang5":"Alex C","bconrad2":"Ben C","mdenning":"Max D","ellidia":"Ellidia D","aelosua":"Antonio E","dhfranks":"David F","ritijg":"Ritij G","cmgray":"Caroline G","pguerra":"Pilar G","rgupta16":"Ruchi G","alhanna":"Andrew H","meganrh":"Megan H","rhouser":"Rebecca H","lidris":"Lana I","bmj21":"Bianca J","reks":"Roberto K","shilpak2":"Shilpa K","katzmanm":"Mike K","jkoch26":"Jay K","johndk":"John K","koreli":"Georgi K","skku":"Kathy K","abekumar":"Abe K","mkl17":"Miki L","ekjl":"Edward L","georgeli":"George L","hsmangat":"Harpreet M","smaybank":",Susannah M","dmirab":"Dom M","kmulumba":"Yanick M","mnehmad":"Michael N","phannn":"Phan N","mngwenya":"Maka N","juliusn":",Julius N","gparosa":"Grzegorz P","emmract":"Emma R","regramos":"Regina R","bruxin":"Ben R","scheina":"Andrew S","afsch":"Alex S","suwana":"Adeline S","duribe":"Daniel U","onome":"Onome U","sravyav":"Sravya V","bwestbro":"Brent W","ecz":"Eric Z","zifzaf":"Ahmed Z","jzou":"Jessica Z"}


class Constants(BaseConstants):
    name_in_url = 'New_Recruit'
    players_per_group = 2
    num_rounds = 1

    reading_time = 5 #minutes
    material_button_show= 2 #minutes
    material_button_show_no_timer= 2 #minutes
    calculator_time = 5 #minutes
    planning_doc_time= 5 # minutes
    negotiating_time = 25 # minutes

    planning_doc_length = 150 #words

    link_581_1 = "https://stanford.zoom.us/j/98453129717"
    link_581_2 = "https://stanford.zoom.us/j/93410198117"
    section_1_participants = names_section1
    section_2_participants = names_section2
    SUNet_to_name = SUNet_to_name

    salary = { 90000:(-6000,0), 88000:(-4500,-1500), 86000:(-3000,-3000), 84000:(-1500,-4500), 82000:(0,-6000)}
    bonus = { 10:(0,4000), 8:(400,3000), 6:(800,2000), 4:(1200,1000), 2:(1600,0)}
    vacation_time = { 25:(0,1600), 20:(1000,1200), 15:(2000,800), 10:(3000,400), 5:(4000,0)}
    moving_expenses = {100:(0,3200), 90:(200,2400), 80:(400,1600), 70:(600,800), 60:(800,0)}
    location = {"San Francisco":(1200,1200), "Atlanta":(900,900), "Chicago":(600,600),"Boston":(300,300),  "New York":(0,0)}
    insurance_coverage = {"Plan A":(0,800), "Plan B":(800,600), "Plan C":(1600,400), "Plan D":(2400,200), "Plan E":(3200,0)}
    starting_date = {"June 1":(0,2400), "June 15":(600,1800),"July 1":(1200,1200), "July 15":(1800,600), "August 1":(2400,0)}
    job_assignment = {"Division A":(0,0), "Division B":(-600,-600), "Division C":(-1200,-1200), "Division D":(-1800,-1800), "Division E":(-2400,-2400)}


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    salary = models.IntegerField()
    bonus = models.IntegerField()
    moving_expenses = models.IntegerField()
    vacation_time = models.IntegerField()
    job_assignment = models.StringField()
    location = models.StringField()
    insurance_coverage = models.StringField()
    starting_date = models.StringField()


class Player(BasePlayer):
    salary = models.IntegerField()
    bonus = models.IntegerField()
    moving_expenses = models.IntegerField()
    vacation_time = models.IntegerField()
    job_assignment = models.StringField()
    location = models.StringField()
    insurance_coverage = models.StringField()
    starting_date = models.StringField()

    planning_text = models.LongStringField(label="Describe your plan for this negotiation")
    journaling_text = models.LongStringField(label="Please describe your experience of the negotiation.")
    initial_offer_points = models.IntegerField()
    final_points = models.IntegerField()

    salary_fract = models.FloatField()
    bonus_fract = models.FloatField()
    job_assignment_fract = models.FloatField()
    location_fract =models.FloatField()
    insurance_coverage_fract = models.FloatField()
    vacation_time_fract = models.FloatField()
    starting_date_fract = models.FloatField()
    moving_expenses_fract = models.FloatField()



    def role(self):
        if self.id_in_group == 1:
            return 'candidate'
        else:
            return 'recruiter'
