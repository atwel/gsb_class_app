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
Negotatiing Sugar Bowl with a partner via email.
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
    name_in_url = 'Sugar_Bowl_Section_1'
    players_per_group = 2
    num_rounds = 1

    reading_time = 5 #minutes
    material_button_show= .02 #minutes
    material_button_show_no_timer= .02 #minutes
    calculator_time = 5 #minutes
    planning_doc_time= 5 # minutes
    negotiating_time = 25 # minutes

    planning_doc_length = 150 #words

    section_1_participants = names_section1.split(",")
    section_2_participants = names_section2.split(",")
    SUNet_to_name = SUNet_to_name



class Subsession(BaseSubsession):
    def creating_session(self):
        names = Constants.section_1_participants.copy()
        for p in self.get_players():
            p.participant.label = names.pop(0)


class Group(BaseGroup):
    final_price = models.IntegerField(label="What was the final purchase price in USD?")
    who_purchased = models.StringField(choices=["Buyer","Dealer"],label="Which party purchased the sugar bowl?")
    initial_offer = models.IntegerField(label="If you were going to make an offer in your initial email (you might not!), what would the price be (in USD)?")
    reservation_price_dealer = models.IntegerField(label="What is your reservation price in USD for this piece?")
    target_price_dealer = models.IntegerField(label="What is your aspiration price in USD for this piece?")
    reservation_price_buyer = models.IntegerField(label="What is your reservation price in USD for this piece?")

class Player(BasePlayer):

    planning_text = models.LongStringField(label="Describe your plan for this negotiation")
    journaling_text = models.LongStringField(label="Please describe your experience of the negotiation. In what ways was negotiating via email different than through Zoom?")



    def role(self):
        if self.id_in_group == 1:
            return 'buyer'
        else:
            return 'dealer'
