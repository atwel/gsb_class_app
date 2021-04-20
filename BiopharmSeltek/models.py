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
Negotatiing BioPharm Seltek with a partner
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
    name_in_url = 'BiopharmSeltek'
    players_per_group = 2
    num_rounds = 1
    reading_time = 10
    planning_doc_length = 150
    planning_doc_time_minutes = 5
    negotiating_time = 25

    link_581_1 = "https://stanford.zoom.us/j/96497241579?pwd=ZzgxeFFDOWQ3ODZxTnZ0OERVK0RMQT09"
    link_581_2 = "https://stanford.zoom.us/j/93359073372?pwd=TjZMTno1MUZUS1d3TUNkUHNERmJvZz09"
    link_581_3 = "https://stanford.zoom.us/j/96451384953?pwd=ZkZmeUllalhQM3JFMzBUNitFaDJoQT09"
    section_1_participants = names_section1
    section_2_participants = names_section2
    section_3_participants = names_section3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    link = models.StringField(label="Stanford Zoom URL")
    link_to_recording = models.StringField(label="Please provide the link to your recording.")
    initial_price = models.CurrencyField(label="What was the price of the first offer in millions of USD (e.g. XX.xx )?")
    made_initial = models.StringField(choices=["BioPharm","Seltek"], widget=widgets.RadioSelectHorizontal, label="Which company made the first offer?")
    deal = models.BooleanField(label="Did the companies reach a deal?",widget=widgets.RadioSelectHorizontal)
    last_Biopharm = models.CurrencyField(label="What was the last offer made by BioPharm in millions of USD (e.g. XX.x)?")
    last_Seltek = models.CurrencyField(label="What was the last offer made by Seltek in millions of USD (e.g. XX.xx)?")
    final_sale_price = models.CurrencyField(label="What was the Final Sale Price in millions of USD (e.g. XX.xx)?")
    batna_BF = models.CurrencyField(label="At what price in millions of USD should you walk away without a deal?")
    target_BF = models.CurrencyField(label="What is your ideal purchase price for the Seltek plant in millions of USD (e.g. XX.xx)?")
    batna_ST = models.CurrencyField(label="At what price in millions of USD should you walk away without a deal?")
    target_ST = models.CurrencyField(label="What is your ideal sale price for your plant in millions of USD (e.g. XX.x)?")
    nego_time = models.IntegerField()

class Player(BasePlayer):
    planning_text = models.LongStringField(label="Describe your plan for this negotiation")
    journaling_text = models.LongStringField(label="Please describe your experience of the negotiation.")
    healthcheck= models.BooleanField(label="Are you in compliance with GSB COVID in-person instruction policies?",widget=widgets.RadioSelectHorizontal)
    inperson = models.BooleanField(label="Are you wanting to negotiate in person today?",widget=widgets.RadioSelectHorizontal)
