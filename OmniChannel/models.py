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
Negotatiing Federated Sciences with two partners
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
    name_in_url = 'OmniChannel'
    players_per_group = 2
    num_rounds = 1
    reflection_time  = 5 # minutes
    coordinating_time = 20

    planning_doc_length = 150 #words


class Subsession(BaseSubsession):
    pass

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
    length = models.IntegerField(label="Length of Agreement", choices=[8,7,6,5,4])
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
