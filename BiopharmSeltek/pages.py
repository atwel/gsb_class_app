from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import time

SUNet_to_name = {'ipshita9':'Ipshita Agarwal','qurrat':'Qurrat Ahmad','shaden':'Shaden Alsheik','aamdekar':'Atharva Amdekar','beattymg':'Matt Beatty','zachboy':'Zach Boyette','lbrito':'Louise Celine Badcock de Brito','decarlos':'Iñigo de Carlos Artajo','ijdelcid':'Imer J del Cid','rdensley':'Rachel Densley','elaine24':'Elaine Fang','alisdair':'Alisdair Ferguson','madisonc':'Madison Freeman','tgerrard':'Tye Gerrard','ghasemi':'Ehsan Ghasemi','jguerci':'John Guerci','whazard':'Whitney Keene Hazard','whoran':'Wyatt Horan','jchwang':'Jennifer C. Hwang','moizimam':'Moiz Imam','swjacobs':'Stephen Jacobs','jenkinsa':'Alexandra Jenkins','nitikaj':'Nitika Johri','amykim':'Amy Kim','kotov':'Sonya Kotov','diegollm':'Diego Lloreda Martín','luolaura':'Laura Pai Luo','mmadding':'Michael Madding','lmulyani':'Linda Mulyani','amurtlan':'Andrew Murtland','nakamasa':'Masahiro Nakanishi','thuyanhn':'Anh Nguyen','knyman':'Knut Olov Viking Nyman','patelsm':'Shivam Patel','mikepeng':'Mike Peng','danpil':'Dan Pilewski','epowers2':'Emily Powers','jruben':'James Arthur Ruben','csapan':'Claire Sapan','mschein':'Mara Gabrielle Schein','jserra':'Julian Jaime Serra','nishsham':'Nishanth Shamanna','jsharma3':'Jigyasa Sharma','socarras':'Esteban Socarras','zstiles':'Zane Stiles','samuelvp':'Samuel Veloso','nycwang':'Christina Wang','wangjess':'Jessica Wang','gwatsham':'Ginny Watsham','lgwhite':'Louise White','fangting':'Angela Wu','lisaye':'Yuying Ye','joohoyeo':'Joo Ho Yeo','yuchenz':'Yuchen Zou','ioannaa':'Ioanna Aguilar','salarifi':'Salman Alarifi','obabin':'Olivier Babin','sebq':'Sebastian Rodolfo Baquerizo Queirolo','piali':'Piali Bopanna','jordanby':'Jordan Byers','cycampos':'Cheryl Campos','schang63':'Samuel C Chang','amanc2':'Aman Chaudhary','julietc1':'Juliet Choi','ccranmer':'Caitlin Cranmer','ccunn':'Caleb Cunningham','jdumiak':'Jen Dumiak','sdunau':'Shane Nicole Dunau','nfewel':'Nathan Fewel','cegarcia':'Catalina Eugenia Garcia Gajardo','egetty':'Erin Getty','mngratz':'Maggie Gratz','ashenkel':'Lexi Henkel','amholt':'Mandy Holt','irvhsu':'Irving Hsu','blaireym':'Blaire Huang','neerajj':'Neeraj Jaisinghani','harshitk':'Harshit Kohli','jkubert':'Jon Kubert','alacey':'Alex Lacey','mliamos':'Michael Charles Liamos','slif':'Sandra Lifshits','ivolima':'Ivo Paulo Lima','brlobato':'Breno Lobato','jdlorenz':'Jonathon Lorenz','mattmad3':'Mathew Madsen','irfanx':'Irfan Mahmud','mmallah':'Mariama Mallah','mhmann':'Myles Mann','fmcunha':'Flávia Medina da Cunha','krishm':'Krish Mehta','jonpeder':'Jonathan Pedersen','woodsrp':'Woods Preechawit','craiff':'Clay Raiff','juromero':'Julieta Aldana Romero','hectorsj':'Hector Rolando Sandoval Juarez','msauvage':'Michael Sauvage','jhstyles':'John Henry Styles','darrenjt':'Darren Tan','darrylt':'Darryl Tan','emwaxman':'Emily Waxman','liawe':'Lia Michal Weiner','jwijn':'Jacob Wijnberg','awyner':'Andrew Wyner','fangfeiy':'Fangfei Yin','aleksz':'Aleksandar Zdravkovski','amygzhao':'Amy Zhao','orzolty':'Or Zolty','fredaddy':'Fred Addy','zakb':'Zak Budden','connorca':'Connor Callaway','acohen22':'Adam Scott Cohen','lydiad':'Lydia Deng','katieliz':'Katie Dickinson','allanfan':'Allan Fan','annafilo':'Anna Filochowska','gforter':'Gabriela Forter','cguardad':'Claudio Guardado','lhaffer':'Lukas Haffer','drharris':'david harris','sehughes':'Sarah Hughes','ajacks03':'Allen Shannon Jackson','rrjia':'Rebecca Ran Jia','gautamgk':'Gautam Kapur','skawatra':'Srishti Kawatra','urikedem':'Uri Kedem','dkhar22':'David Kharatishvili','yooekim':'Yoo Eun Kim','nskolber':'Natalie Sarah Kolber','kompalla':'Julia Franziska Kompalla','lask1952':'Alexis Misha Laskowski','qixuanli':'Qixuan Li','ptlin84':'Kyle Lin','alvarom':'Alvaro Marin Melero','amedina8':'Antonio Rafael Medina Perez','jackfm':'Jack Francis Michaels','aaronjm':'Aaron Miller','minali':'Minali Mohindra','emuco':'Evi Muco','jamunoz':'Jocelyne Arlette Munoz','joshpick':'Josh Pickering','traje':'Tanvi Nikita Vikas Raje','cregan7':'Connor Regan','tomrose':'Tom Stern Rosenblatt','juanr94':'Juan Rosenkrantz','albarr':'Alba Rubio Rodriguez','isabate':'Ignacio Sabaté','nschlein':'Nate Schlein','ben4':'Ben Liad Schwartz','skrobach':'Mykhailo Skrobach','jiawent':'Jiawen Tang','suwimana':'Sandy Uwimana','nachov':'Nacho Vidri','dwagura':'David Wangombe Wagura','markwhit':'Mark Robert Whittaker','grayy':'Gray Scott Young',"extra1":"Unnamed #1 (see Pr. Atwell)","extra2":"Unnamed #2 (see Pr. Atwell)","extra3":"Unnamed #3 (see Pr. Atwell)","extra4":"Unnamed #4 (see Pr. Atwell)","extra5":"Unnamed #5 (see Pr. Atwell)","extra6":"Unnamed #6 (see Pr. Atwell)"
}

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


    #timeout_seconds = 180

    def vars_for_template(self):
        if self.player.id_in_group == 1:
            return {"pdf_file": "BiopharmSeltek/Seltek.pdf"}
        if self.player.id_in_group == 2:
            return {"pdf_file": "BiopharmSeltek/BioPharm.pdf"}


class Outro(Page):
    form_model = "group"





page_sequence = [IntroWaitPage, Introduction, Seltek_materials, Biopharm_materials, Preferences_input_BF, Preferences_input_ST, Planning_doc, Meeting_wait, Meeting_location_reminder, Seltek_materials_no_timer, BioPharm_materials_no_timer, Negotiated_outcome_one, Negotiated_outcome_two, Outcome_wait,Finished_case, Journaling_page, Outro]
