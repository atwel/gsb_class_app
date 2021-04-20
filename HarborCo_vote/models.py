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
    name_in_url = 'Voting'
    players_per_group = 6
    num_rounds = 10

    section_1_participants = names_section1.split(",")
    SUNet_to_name = SUNet_to_name



class Subsession(BaseSubsession):
    def creating_session(self):
        names = Constants.section_1_participants.copy()
        for p in self.get_players():
            p.participant.label = names.pop(0)


class Group(BaseGroup):
    mix = models.StringField(label="Industry Mix", choices=["Primarily dirty","Clean & dirty","All clean"],initial="Primarily dirty")
    eco = models.StringField(label="Ecological Impact",choices=["Some harm","Maintain & repair","Improve"], initial="Some harm")
    union = models.StringField(label="Employment Rules",choices=["Unlimited union preference","Union quota 2:1","Union quota 1:1","No union preference"], initial="No union preference")
    loan = models.StringField(label="Federal Loan", choices=["$3 Billion","$2 Billion","$1 Billion","No federal loan"],initial="$3 Billion")
    comp = models.StringField( label = "Compensation to other ports", choices=["HarborCo pays $600 million","HarborCo pays $450 million","HarborCo pays $300 million","HarborCo pays $150 million","HarborCo pays nothing"],initial="HarborCo pays nothing")

    passed = models.BooleanField()
    high_passed = models.BooleanField()
    vetoed = models.BooleanField()
    no_pass = models.BooleanField()
    pairing = models.StringField()

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
            return 'harborco'
        else:
            return 'gov'
