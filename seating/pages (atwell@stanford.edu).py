from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants

import time

SUNet_to_name = {'atwell':"Prof. Atwell","apaza":"Adrian A (CA)","extra_01":"Unknown","extra_02":"Unknown", "extra_03":"Unknown","extra_04":"Unknown","extra_05":"Unknown","extra_06":"Unknown","aguinis":"Martin A","alokikb":"Alokik B","rbinko":"Robert B","meb277":"Mary B","gbrink":"Georgie B","obbrown":"Olivia B","schidamb":"Swathi C","whchu":"Whitney C","kimifaf":"Kimiloluwa F","kfauzie":"Kevin F","cfoote6":"Chas F","wgeorge":"Will G","afkats":"Antonie K","kparanin":"Now K","ericli1":"Eric L","monicaml":"Monica L","qlores":"Quique L","ninalu":"Nina L","roycclu":"Roy L","bencmatt":"Benjamin M","dcnugent":"Dylan N","willo":"Will O","izunna":"Izunna O","hardik":"Hardik P","nmrojas":"Nicole P","bhs":"Branden S","tlscham":"Tamar S","zsharif":"Zakaria S","mirrin":"Mirrin S","asohmshe":"Archana S","nsong":"Nancy S","cku1":"Chinedum  U","award92":"Austin W","dzanchi":"Davide Z","jrzhang1":"Jeff Z","santidb":"Santiago dB","alealvar":"Alejandra A","aanders":"Alisha A","isabel4":"sabel A","babbitt":"Andrew B","bennetta":"Alex B","mackbran":"Mackenzie B","dbujanos":"Daniel B","danranc":"Danran C","jchoi91":"Jesse C","mcreamer":"Mateo C","ndfesh":"Nicole F","nrgandhi":"Neil G","giraldo":"Mariana G","ccgong":"C.C. Gong","dhallman":"Dylan H","sagari":"Sagar I","slehman1":"Sydney L","meluck":"Mary Ellen L","kylemca":"Kyle McA","ajmccrea":"Andrew McC","amejia1":"Aly M","agmendez":"Alex M","eemiller":"Emily M","kiya":"Kiya M","pjm2022":"Peter M","nmullaji":"Nandini M","arnenm":"Arne N","wlross":"Will R","kayjs":"Kayj S","joyceshi":"Joyce S","ats2022":"Alex S","cstromey":"Christopher S","rsuarezm":"Ricky S","ssykes":"Sydney S","kylietan":"Kylie T","ptoth":"Patrick T","twiegand":"Tessa W","jzerker":"Jenna Z","stephz":"Stephanie Z","kamilali":"Kamil A","gelilab":"Gelila B","bboss":"Benjamin B","mcalvano":"Matt C","ejcbrown":"Emily C","gregcaso":"Greg C","achang5":"Alex C","bconrad2":"Ben C","mdenning":"Max D","ellidia":"Ellidia D","aelosua":"Antonio E","dhfranks":"David F","ritijg":"Ritij G","cmgray":"Caroline G","pguerra":"Pilar G","rgupta16":"Ruchi G","alhanna":"Andrew H","meganrh":"Megan H","rhouser":"Rebecca H","lidris":"Lana I","bmj21":"Bianca J","reks":"Roberto K","shilpak2":"Shilpa K","katzmanm":"Mike K","jkoch26":"Jay K","johndk":"John K","koreli":"Georgi K","skku":"Kathy K","abekumar":"Abe K","mkl17":"Miki L","ekjl":"Edward L","georgeli":"George L","hsmangat":"Harpreet M","smaybank":",Susannah M","dmirab":"Dom M","kmulumba":"Yanick M","mnehmad":"Michael N","phannn":"Phan N","mngwenya":"Maka N","juliusn":",Julius N","gparosa":"Grzegorz P","emmract":"Emma R","regramos":"Regina R","bruxin":"Ben R","scheina":"Andrew S","afsch":"Alex S","suwana":"Adeline S","duribe":"Daniel U","onome":"Onome U","sravyav":"Sravya V","bwestbro":"Brent W","ecz":"Eric Z","zifzaf":"Ahmed Z","jzou":"Jessica Z"}


class Introduction(Page):
    form_model = "player"

    def before_next_page(self):
        if self.participant.label in self.session.vars["eligible"]:
            self.participant.vars["eligible"] = True
        elif self.participant.label in self.session.vars["ineligible"]:
            self.participant.vars["eligible"] = False
        else:
            print("Label not found", self.participant.label)


class Seating_query(Page):
    form_model = 'player'
    form_fields = ['claim_it']

    def is_displayed(self):
        if self.participant.vars["eligible"]:
            return True
        else:
            return False

    def vars_for_template(self):
        return {"name":SUNet_to_name[self.participant.label]}



class Waitlist_self(Page):
    form_model = 'player'
    form_fields = ['waiting']

    def is_displayed(self):
        if self.participant.vars["eligible"]:
            return False
        else:
            return True

    def vars_for_template(self):
        return {"name":SUNet_to_name[self.participant.label]}

    def before_next_page(self):
        self.participant.vars["time_started"] = time.time()



class Exit_eligible(Page):
    form_model = 'player'

    def is_displayed(self):
        if self.participant.vars["eligible"]:
            return True
        else:
            return False

    def vars_for_template(self):
        return {"attending":self.player.claim_it, "name":SUNet_to_name[self.participant.label]}



class Exit_ineligible(Page):
    form_model = 'player'

    def is_displayed(self):
        if self.participant.vars["eligible"]:
            return False
        else:
            return True

    def vars_for_template(self):
        return {"name":SUNet_to_name[self.participant.label]}



class Final_calculation(WaitPage):
    form_model = "player"

    def after_all_players_arrive(self):
        waiting = []
        accepted = []

        for p in self.get_players():
            if p.claim_it:
                accepted.append(p)
            elif p.waiting:
                waiting.append((p.participant.label,p.participant.vars["time_started"]))

        remaining_spots = Constants.available_seats - len(accepted)

        if remaining_spots == 0:
            print("No one off the waitlist")
        else:
            srted = sorted(waiting,key=itemgetter(1), reverse=True)[:remaining_spots]
            print("Add the following:")
            for name in srted[:remaining_spots]:
                print("{}@stanford.edu".format(name[0]))
            print("Reject the following:")
            for name in srted[remaining_spots:]:
                print("{}@stanford.edu".format(name[0]))


page_sequence = [Introduction, Seating_query, Waitlist_self, Exit_eligible, Exit_ineligible, Final_calculation]
