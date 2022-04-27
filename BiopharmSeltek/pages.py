from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import time

SUNet_to_name = {'klipcsei':"Chris L","giraldo":"Mariana",'atwell':"Prof. Atwell","apaza":"Adrian A (CA)","extra_01":"Unnamed #1","extra_02":"Unnamed #2", "extra_03":"Unnamed #3","extra_04":"Unnamed #4","extra_05":"Unnamed #5","extra_06":"Unnamed #6","aguinis":"Martin A","cbegleit":"Caroline B","alokikb":"Alokik B","rbinko":"Robert B","meb277":"Mary B","gbrink":"Georgie B","obbrown":"Olivia B","schidamb":"Swathi C","kimifaf":"Kimiloluwa F","kfauzie":"Kevin F","afehmiu":"Andra F","wgeorge":"Will G","afkats":"Antonie K","kparanin":"Now K","ericli1":"Eric L","monicaml":"Monica L","qlores":"Quique L","ninalu":"Nina L","roycclu":"Roy L","bencmatt":"Benjamin M","dcnugent":"Dylan N","willo":"Will O","izunna":"Izunna O","hardik":"Hardik P","nmrojas":"Nicole P","bhs":"Branden S","tlscham":"Tamar S","zsharif":"Zakaria S","mirrin":"Mirrin S","asohmshe":"Archana S","nsong":"Nancy S","cku1":"Chinedum  U","award92":"Austin W","dzanchi":"Davide Z","jrzhang1":"Jeff Z","santidb":"Santiago dB","alealvar":"Alejandra A","aanders":"Alisha A","isabel4":"Sabel A","babbitt":"Andrew B","bennetta":"Alex B","mackbran":"Mackenzie B","dbujanos":"Daniel B","danranc":"Danran C","jchoi91":"Jesse C","mcreamer":"Mateo C","ndfesh":"Nicole F","nrgandhi":"Neil G","giraldo":"Mariana G","ccgong":"C.C. Gong","dhallman":"Dylan H","sagari":"Sagar I","slehman1":"Sydney L","meluck":"Mary Ellen L","kylemca":"Kyle McA","ajmccrea":"Andrew McC","amejia1":"Aly M","agmendez":"Alex M","eemiller":"Emily M","kiya":"Kiya M","pjm2022":"Peter M","nmullaji":"Nandini M","arnenm":"Arne N","wlross":"Will R","kayjs":"Kayj S","joyceshi":"Joyce S","ats2022":"Alex S","cstromey":"Christopher S","rsuarezm":"Ricky S","ssykes":"Sydney S","kylietan":"Kylie T","ptoth":"Patrick T","twiegand":"Tessa W","jzerker":"Jenna Z","stephz":"Stephanie Z","kamilali":"Kamil A","gelilab":"Gelila B","bboss":"Benjamin B","mcalvano":"Matt C","ejcbrown":"Emily C","gregcaso":"Greg C","achang5":"Alex C","bconrad2":"Ben C","mdenning":"Max D","ellidia":"Ellidia D","aelosua":"Antonio E","dhfranks":"David F","ritijg":"Ritij G","cmgray":"Caroline G","pguerra":"Pilar G","rgupta16":"Ruchi G","alhanna":"Andrew H","meganrh":"Megan H","rhouser":"Rebecca H","lidris":"Lana I","bmj21":"Bianca J","reks":"Roberto K","shilpak2":"Shilpa K","katzmanm":"Mike K","jkoch26":"Jay K","johndk":"John K","koreli":"Georgi K","skku":"Kathy K","abekumar":"Abe K","mkl17":"Miki L","ekjl":"Edward L","georgeli":"George L","hsmangat":"Harpreet M","smaybank":",Susannah M","dmirab":"Dom M","kmulumba":"Yanick M","mnehmad":"Michael N","phannn":"Phan N","mngwenya":"Maka N","juliusn":",Julius N","gparosa":"Grzegorz P","emmract":"Emma R","regramos":"Regina R","bruxin":"Ben R","scheina":"Andrew S","afsch":"Alex S","suwana":"Adeline S","duribe":"Daniel U","onome":"Onome U","sravyav":"Sravya V","bwestbro":"Brent W","ecz":"Eric Z","zifzaf":"Ahmed Z","jzou":"Jessica Z","shafi":"Mohammed S","edwinq":"Edwin Q","jelzinga":"Jack E"}

class IntroWaitPage(WaitPage):
    group_by_arrival_time = True

    def vars_for_template(self):
        return {"title_text": "Hang tight", "body_text":"Please wait a moment to get paired.\n\nIf you've been on this page for a while, try refreshing the page."}


class Introduction(Page):
    form_model = "player"

    def before_next_page(self):
        try:
            self.participant.vars["SUNet"] = self.participant.label
            self.participant.vars["name"] = SUNet_to_name[self.participant.label]
        except:
            self.participant.vars["SUNet"] = "none"
            self.participant.vars["name"] = "(come see Dr. Atwell)"

        self.player.name = self.participant.vars["name"]

    def vars_for_template(self):
        total_time = Constants.reading_time + Constants.planning_doc_time_minutes + Constants.negotiating_time + 10
        return {"reading_limit":Constants.reading_time,"total_time":total_time}


class Meeting_location(Page):
    form_model = "player"

    def vars_for_template(self):
            return {"zoom_link":self.participant.vars["zoom_link"], "pdf_file":"global/OutdoorMap.pdf"}


class Seltek_materials(Page):
    form_model = "player"

    timeout_seconds= Constants.reading_time * 60
    timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return {"pdf_file": "BiopharmSeltek/Seltek.pdf"}


class Biopharm_materials(Page):
    form_model = "player"

    timeout_seconds= Constants.reading_time * 60
    timer_text = 'Time left for reading the materials'


    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        return {"pdf_file": "BiopharmSeltek/BioPharm.pdf"}


class Preferences_input_ST(Page):
    form_model = "group"
    form_fields = ['target_ST', "batna_ST"]

    timeout_seconds= 120
    timer_text = 'Time left to input values'
    def is_displayed(self):
            return self.player.id_in_group == 1

    def vars_for_template(self):
        return {"pdf_file": "BiopharmSeltek/Seltek.pdf"}


class Preferences_input_BF(Page):
    form_model = "group"
    form_fields = ['target_BF', "batna_BF"]

    timeout_seconds= 120
    timer_text = 'Time left to input values'
    def is_displayed(self):
            return self.player.id_in_group == 2

    def vars_for_template(self):
        return {"pdf_file": "BiopharmSeltek/BioPharm.pdf"}


class Planning_doc(Page):
    form_model = "player"
    form_fields = ["planning_text"]

    timeout_seconds= Constants.planning_doc_time_minutes * 60
    timer_text = 'Time left for writing your document:'

    def vars_for_template(self):
        if self.player.id_in_group == 1:
            return {"return_link": "BiopharmSeltek/Seltek_materials.html","max_word_limit":Constants.planning_doc_length}
        if self.player.id_in_group == 2:
            return {"return_link": "BiopharmSeltek/Biopharm_materials.html","max_word_limit":Constants.planning_doc_length}


class Meeting_location_reminder(Page):
    form_model = "player"

    def vars_for_template(self):
            partner = self.player.get_others_in_group()[0]
            self.player.partner = partner.participant.vars["name"]
            if self.player.id_in_group ==1:
                self.player.grole = "Seltek"
            else:
                self.player.grole = "BioPharm"

            return {"negotiating_time":Constants.negotiating_time,"partner":partner.participant.vars["name"] }

            #return {"zoom_link":self.participant.vars["zoom_link"], "pdf_file":"global/OutdoorMap.pdf"}


class Meeting_wait(WaitPage):
    form_model = "group"
    after_all_players_arrive = 'set_timer'

    def vars_for_template(self):
            return {"title_text":"Waiting...","body_text":"We're waiting for your counterparty to be ready. Once they finish up, you'll go back to the case materials page and the timed negotiation will begin."}


class Seltek_materials_no_timer(Page):
    form_model = "player"

    template_name = "BiopharmSeltek/Seltek_materials.html"

    timer_text = 'Time left for negotiating the case:'

    def get_timeout_seconds(self):
        return Constants.negotiating_time*60 #self.participant.vars["sim_timer"] - time.time()

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return {"pdf_file": "BiopharmSeltek/Seltek.pdf"}


class BioPharm_materials_no_timer(Page):
    form_model = "player"
    template_name = "BiopharmSeltek/Biopharm_materials.html"

    timer_text = 'Time left for negotiating the case:'

    def get_timeout_seconds(self):
        return Constants.negotiating_time*60 #self.participant.vars["sim_timer"] - time.time()

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        return {"pdf_file": "BiopharmSeltek/BioPharm.pdf"}


class Negotiated_outcome_one(Page):

    form_model = "group"
    form_fields = ["made_initial","initial_price","deal"]

    def is_displayed(self):
        return self.player.id_in_group == 2


class Negotiated_outcome_two(Page):

    form_model = "group"

    def get_form_fields(self):
        if self.group.deal:
            return ['final_sale_price']
        else:
            return ["last_Seltek","last_Biopharm"]

    def is_displayed(self):
        return self.player.id_in_group == 2


class Outcome_wait(WaitPage):
    form_model = "group"

    form_fields = ["nego_time"]

    def vars_for_template(self):
        if self.player.id_in_group == 1:
            return {"title_text": "Reporting the outcome", "body_text":"Wait a moment while the BioPharm representative finishes inputting the results.\n\n"}
        else:
            return {"title_text": "Waiting", "body_text":"Wait a moment for the Seltek representative.\n\n"}


class Sign_off_page(Page):
    form_model = "group"

    def before_next_page(self):
        bio = self.group.get_player_by_id(2)
        self.group.nego_time = int(time.time() - bio.participant.vars["sim_start"])

class Finished_case(Page):
    form_model = "group"


class Journaling_page(Page):
    form_model = "player"

    form_fields = ["journaling_text"]

    #timeout_seconds = 180

    def vars_for_template(self):
        if self.player.id_in_group == 1:
            return {"pdf_file": "BiopharmSeltek/Seltek.pdf"}
        if self.player.id_in_group == 2:
            return {"pdf_file": "BiopharmSeltek/BioPharm.pdf"}


class Outro(Page):
    form_model = "group"





page_sequence = [IntroWaitPage, Introduction, Seltek_materials, Biopharm_materials, Preferences_input_BF, Preferences_input_ST, Planning_doc, Meeting_wait, Meeting_location_reminder, Seltek_materials_no_timer, BioPharm_materials_no_timer, Negotiated_outcome_one, Negotiated_outcome_two, Outcome_wait,Finished_case, Journaling_page, Outro]
