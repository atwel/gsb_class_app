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

SUNet_to_name = {'atwell':"Prof. Atwell","apaza":"Adrian A (CA)","extra_01":"Unknown","extra_02":"Unknown", "extra_03":"Unknown","extra_04":"Unknown","extra_05":"Unknown","extra_06":"Unknown","aguinis":"Martin A","alokikb":"Alokik B","rbinko":"Robert B","meb277":"Mary B","gbrink":"Georgie B","obbrown":"Olivia B","schidamb":"Swathi C","whchu":"Whitney C","kimifaf":"Kimiloluwa F","kfauzie":"Kevin F","cfoote6":"Chas F","wgeorge":"Will G","afkats":"Antonie K","kparanin":"Now K","ericli1":"Eric L","monicaml":"Monica L","qlores":"Quique L","ninalu":"Nina L","roycclu":"Roy L","bencmatt":"Benjamin M","dcnugent":"Dylan N","willo":"Will O","izunna":"Izunna O","hardik":"Hardik P","nmrojas":"Nicole P","bhs":"Branden S","tlscham":"Tamar S","zsharif":"Zakaria S","mirrin":"Mirrin S","asohmshe":"Archana S","nsong":"Nancy S","cku1":"Chinedum  U","award92":"Austin W","dzanchi":"Davide Z","jrzhang1":"Jeff Z","santidb":"Santiago dB","alealvar":"Alejandra A","aanders":"Alisha A","isabel4":"sabel A","babbitt":"Andrew B","bennetta":"Alex B","mackbran":"Mackenzie B","dbujanos":"Daniel B","danranc":"Danran C","jchoi91":"Jesse C","mcreamer":"Mateo C","ndfesh":"Nicole F","nrgandhi":"Neil G","giraldo":"Mariana G","ccgong":"C.C. Gong","dhallman":"Dylan H","sagari":"Sagar I","slehman1":"Sydney L","meluck":"Mary Ellen L","kylemca":"Kyle McA","ajmccrea":"Andrew McC","amejia1":"Aly M","agmendez":"Alex M","eemiller":"Emily M","kiya":"Kiya M","pjm2022":"Peter M","nmullaji":"Nandini M","arnenm":"Arne N","wlross":"Will R","kayjs":"Kayj S","joyceshi":"Joyce S","ats2022":"Alex S","cstromey":"Christopher S","rsuarezm":"Ricky S","ssykes":"Sydney S","kylietan":"Kylie T","ptoth":"Patrick T","twiegand":"Tessa W","jzerker":"Jenna Z","stephz":"Stephanie Z","kamilali":"Kamil A","gelilab":"Gelila B","bboss":"Benjamin B","mcalvano":"Matt C","ejcbrown":"Emily C","gregcaso":"Greg C","achang5":"Alex C","bconrad2":"Ben C","mdenning":"Max D","ellidia":"Ellidia D","aelosua":"Antonio E","dhfranks":"David F","ritijg":"Ritij G","cmgray":"Caroline G","pguerra":"Pilar G","rgupta16":"Ruchi G","alhanna":"Andrew H","meganrh":"Megan H","rhouser":"Rebecca H","lidris":"Lana I","bmj21":"Bianca J","reks":"Roberto K","shilpak2":"Shilpa K","katzmanm":"Mike K","jkoch26":"Jay K","johndk":"John K","koreli":"Georgi K","skku":"Kathy K","abekumar":"Abe K","mkl17":"Miki L","ekjl":"Edward L","georgeli":"George L","hsmangat":"Harpreet M","smaybank":",Susannah M","dmirab":"Dom M","kmulumba":"Yanick M","mnehmad":"Michael N","phannn":"Phan N","mngwenya":"Maka N","juliusn":",Julius N","gparosa":"Grzegorz P","emmract":"Emma R","regramos":"Regina R","bruxin":"Ben R","scheina":"Andrew S","afsch":"Alex S","suwana":"Adeline S","duribe":"Daniel U","onome":"Onome U","sravyav":"Sravya V","bwestbro":"Brent W","ecz":"Eric Z","zifzaf":"Ahmed Z","jzou":"Jessica Z"}


class Constants(BaseConstants):
    name_in_url = 'HarborCo'
    players_per_group = 6
    num_rounds = 1
    reading_time = 400
    negotiating_time = 80 # minutes
    reflection_time  = 5 # minutes

    planning_doc_length = 100 #words
    planning_doc_time = 40


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    name = models.StringField()
    hc_role = models.StringField(default="Unassigned")
    planning_text = models.LongStringField(label="Describe your plan for this negotiation. In particular, how do intend to approach dealing with coalitions?")
    journaling_text = models.LongStringField(label="Please describe your experience of the negotiation.")
