import time

from otree.api import *


author = 'Jon Atwell'
doc = """
Negotating BioPharm Seltek with a partner
"""


class C(BaseConstants):
    NAME_IN_URL = 'BiopharmSeltek'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    READING_TIME = 10
    PLANNING_DOC_LENGTH = 75
    PLANNING_DOC_TIME_MINUTES = 5
    NEGOTIATING_TIME = 30
    CLASSCODE = 190881
    PLANNING_ASSIGNMENT_CODE = 610574
    FEEDBACK_ASSIGNMENT_CODE = 610719

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):

    initial_price = models.CurrencyField(
        label="What was the price of the first offer? (In millions of USD [e.g. $XX.xx])",
    )
    made_initial = models.StringField(
        choices=["BioPharm", "Seltek"],
        widget=widgets.RadioSelectHorizontal,
        label="Which company made the first offer?",
    )
    deal = models.BooleanField(
        label="Did the companies reach a deal?", widget=widgets.RadioSelectHorizontal
    )
    last_Biopharm = models.CurrencyField(
        label="What was the last offer made by BioPharm? (In millions of USD [e.g. $XX.xx])",
    )
    last_Seltek = models.CurrencyField(
        label="What was the last offer made by Seltek? (In millions of USD [e.g. $XX.xx])",
    )
    final_sale_price = models.CurrencyField(
        label="What was the Final Sale Price? (In millions of USD [e.g. $XX.xx])",
    )
    batna_BF = models.CurrencyField(
        label="At what price should you walk away without a deal? (In millions of USD [e.g. $XX.xx])",
    )
    target_BF = models.CurrencyField(
        label="What is your ideal purchase price for the Seltek plant? (In millions of USD [e.g. $XX.xx])",
    )
    batna_ST = models.CurrencyField(
        label="At what price should you walk away without a deal? (In millions of USD [e.g. $XX.xx])"
    )
    target_ST = models.CurrencyField(
        label="What is your ideal sale price for your plant?  (In millions of USD [e.g. $XX.xx])"
    )
    nego_time = models.IntegerField()


class Player(BasePlayer):
    name = models.StringField()
    grole = models.StringField()
    partner_name = models.StringField()


# FUNCTIONS
def set_timer(group: Group):
    start_time = time.time()
    for player in group.get_players():
        player.participant.vars["sim_timer"] = start_time + C.NEGOTIATING_TIME * 60 + 120

SUNet_to_name = {
'wagathis':'Will Agathis',
'jpbda':'Joao Almeida',
'dabacci':'Diego Bacci',
'rbayne':'Ryan Bayne',
'cblanck':'Caroline Blanck',
'anicarte':'Anisha Carter',
'oliviacn':'Olivia Somerlyn Hollins Christensen',
'sejdavis':'Sarah Davis',
'hobdu':'Hob Du',
'vfanelle':'Valerie Fanelle',
'afatsche':'Andreas Fatschel',
'cgonzal':'Cayo Alexander Gonzalez',
'yaqi':'Yaqi Grover',
'cguardad':'Claudio Guardado',
'jonhoey':'Jon W. L. Hoey',
'vkanodia':'Vikram Kanodia',
'dongsukl':'Paul Lee',
'levinez':'Zach James Levine',
'lexielin':'Lexie Lin',
'raachini':'Anthony Mattar El Raachini',
'lmaymar':'Lauren Maymar',
'harshi':'Harshi Murthy',
'nmartha':'Martha Nabukeera',
'sashan':'Sasha Nanda',
'fnkameni':'Floriane Ngako Kameni',
'oke':'Oke Osevwe',
'suppapat':'Suppapat Ken Pattarasittiwate',
'kellip':'Kelli Pedersen',
'peniston':'Olivia Lyerly Peniston',
'petrichp':'Petra Petrich',
'joshpick':'Josh Pickering',
'mpierce':'Melanie Pierce',
'rcquinn':'Riley Christopher Quinn',
'drivera1':'Diego Rivera',
'danshep':'Daniel Sheppard',
'renatas':'Renata Stewart',
'nsvan':'Natia Svanidze',
'isabelvg':'Isabel Vallina Garcia',
'bgward':'Brad Ward',
'cmweid':'Colin Weidmann',
'jjwise':'Joseph Wise',
'awyner':'Andrew Wyner',
'padelson':'Peter Adelson',
'nazerke':'Naza Aibar',
'mfahim':'Maha Al Fahim',
'mansell':'Mark Garo Ansell',
'ekb6ee':'Erin Kelley Barrett',
'mbodek':'Mira Bodek',
'georgiac':'Georgia Carroll',
'wilclark':'Will Clark',
'ccordara':'Camila Cordara',
'rakiyac':'Rakiya Cunningham',
'ndurkin':'Noelle Durkin',
'tylererb':'Tyler Tyler Erb',
'hfarrukh':'Hamza Farrukh',
'irvhsu':'Irving Hsu',
'klhuang':'Kevin Liu Huang',
'kwjk':'Katharine Jessiman-Ketcham',
'hoct109':'Hokuto Kikuchi',
'bkoba':'Bruno Koba',
'dkurup':'Deepika Kurup',
'clevy25':'Caroline Levy',
'bmaina':'Ndirangu Bryan Maina',
'zmaslia':'Zac Maslia',
'alexjmcc':'Alex Justin McCarthy',
'akm24':'Adam Merrill',
'mmoiz':'Munim Moiz',
'arinze':'Arinze Nwagbata',
'gloriao':'Gloria Ijeoma Odoemelam',
'pparas37':'Paulina Paras',
'arushis':'Arushi Sharma',
'zstiles':'Zane Stiles',
'cau25':'Christian Antonio Urrutia',
'cavarres':'Camila Vargas Restrepo',
'wangjess':'Jessica Wang',
'cmweiner':'Charlotte Weiner',
'joohoyeo':'Joo Ho Yeo',
'capujol':'Claudia Álvarez Pujol',
'mballiyu':'Mubarak Gbolahan Alliyu',
'niranja9':'Niranjan Balachandar',
'savbaum':'Savannah Baum',
'cbeckma3':'Chris Beckmann',
'dani2025':'Dani Camargo Carrillo',
'jhcohen':'Josh Harrison Cohen',
'emduarte':'Emily Duarte',
'nico3':'Nico Enriquez',
'mandygao':'Mandy Gao',
'sgarciav':'Santiago Garcia Vargas',
'cargos':'Carlton Gossett',
'jguerci':'John Guerci',
'krjindal':'Kripanshi Jindal',
'ankita25':'Ankita Kodavoor',
'nlangdon':'Norma Kate Langdon',
'aklee33':'Alexander Keith Lee',
'helenjlu':'Helen Lu',
'mmont':'Mason Montgomery',
'hmurdoch':'Hannah Murdoch',
'mdober':'Matias Daniel Oberpaur',
'paretzky':'Michael Paretzky',
'gyutae95':'Terry Park',
'kayanp':'Kayan Patel',
'npatel21':'Neal Atul Patel',
'npetrie':'Nathan Petrie',
'atpims':'Alan Tomás Pimstein',
'pines':'Sasha Pines',
'erubini':'Eduardo Rubini',
'vsahoo':'Vishal Sahoo',
'alines':'Aline Paula Schechter',
'ryotarot':'Ryotaro Takanashi',
'oliviav':'Olivia Volkel',
'jyao10':'Julia Yao',
'kevinsz':'Kevin Sterling Zhang',
'willzhou':'Will Zhou',
'orzolty':'Or Zolty'
}


class Introduction(Page):
    form_model = "player"

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        try:
            player.participant.vars["SUNet"] = player.participant.label
            player.participant.vars["name"] = SUNet_to_name[player.participant.label]
        except:
            player.participant.vars["SUNet"] = "none"
            player.participant.vars["name"] = "(come see Dr. Atwell)"
        player.name = player.participant.vars["name"]

    @staticmethod
    def vars_for_template(player: Player):
        return {"total_time": C.NEGOTIATING_TIME}


class Seltek_materials(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "BiopharmSeltek/Seltek.pdf"}


class Biopharm_materials(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "BiopharmSeltek/BioPharm.pdf"}


class Preferences_input_ST(Page):
    form_model = "group"
    form_fields = ['target_ST', "batna_ST"]

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "BiopharmSeltek/Seltek.pdf"}

    @staticmethod
    def error_message(player, values):
        if  not ((1<=values['target_ST']<=100)  and (1<=values['batna_ST']<=100)):
            return 'The values need to be inputted in millions of dollars (i.e., no trail of zeros).'


class Preferences_input_BF(Page):
    form_model = "group"
    form_fields = ['target_BF', "batna_BF"]

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "BiopharmSeltek/BioPharm.pdf"}

    @staticmethod
    def error_message(player, values):
        if  not ((1<=values['target_BF']<=100)  and (1<=values['batna_BF']<=100)):
            return 'The values need to be inputted in millions of dollars (i.e., no trail of zeros).'


class Planning_doc(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player: Player):
        if player.id_in_group == 1:
            return {
                "return_link": "BiopharmSeltek/Seltek_materials.html",
                "assignment_url":"/{}/assignments/{}".format(C.CLASSCODE, C.PLANNING_ASSIGNMENT_CODE),
                "max_word_limit": C.PLANNING_DOC_LENGTH,
            }
        if player.id_in_group == 2:
            return {
                "return_link": "BiopharmSeltek/Biopharm_materials.html",
                "assignment_url":"/{}/assignments/{}".format(C.CLASSCODE, C.PLANNING_ASSIGNMENT_CODE),
                "max_word_limit": C.PLANNING_DOC_LENGTH,
            }

class Prep_done(Page):
    form_model = "player"


class Partner_reveal(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player: Player):
        partner = player.get_others_in_group()[0]
        player.partner_name = partner.name
        return {
            "negotiating_time": C.NEGOTIATING_TIME,
            "partner": player.partner_name,
        }


class Meeting_wait(WaitPage):
    form_model = "group"
    after_all_players_arrive = 'set_timer'

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": "Waiting...",
            "body_text": "We're waiting for your counterparty to log into the app. Once they do, the timer will start.",
        }


class Seltek_materials_timer(Page):
    form_model = "player"
    template_name = "BiopharmSeltek/Seltek_materials.html"

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.participant.vars["sim_timer"] - time.time()

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "BiopharmSeltek/Seltek.pdf"}


class BioPharm_materials_timer(Page):
    form_model = "player"
    template_name = "BiopharmSeltek/Biopharm_materials.html"
    timer_text = 'Time left for negotiating the case:'

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.participant.vars["sim_timer"] - time.time()

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "BiopharmSeltek/BioPharm.pdf"}


class Negotiated_outcome_one(Page):
    form_model = "group"
    form_fields = ["made_initial", "initial_price", "deal"]

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def error_message(player, values):
        if  not (1<=values['initial_price']<=100):
            return 'The values need to be inputted in millions of dollars (i.e., no trail of zeros).'



class Negotiated_outcome_deal(Page):
    form_model = "group"
    form_fields = ["final_sale_price"]

    @staticmethod
    def is_displayed(player: Player):
        return (player.id_in_group == 2 and player.group.deal)

    @staticmethod
    def error_message(player, values):
        if  not (1<=values['final_sale_price']<=100) :
            return 'The values need to be inputted in millions of dollars (i.e., no trail of zeros).'

class Negotiated_outcome_nodeal(Page):
    form_model = "group"
    form_fields =  ["last_Seltek", "last_Biopharm"]

    @staticmethod
    def is_displayed(player: Player):
        return (player.id_in_group == 2 and not player.group.deal)

    @staticmethod
    def error_message(player, values):
        if  not ((1<=values['last_Seltek']<=100) and (1<=values['last_Biopharm']<=100)) :
            return 'The values need to be inputted in millions of dollars (i.e., no trail of zeros).'


class Outcome_wait(WaitPage):
    form_model = "group"

    @staticmethod
    def vars_for_template(player: Player):
        if player.id_in_group == 1:
            return {
                "title_text": "Reporting the outcome",
                "body_text": "Wait a moment while the BioPharm representative finishes inputting the results.\n\n",
            }
        else:
            return {
                "title_text": "Waiting",
                "body_text": "Wait a moment for the Seltek representative.\n\n",
            }


class Reflection_page(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player: Player):
        feedback_url = "/{}/assignments/{}".format(C.CLASSCODE, C.FEEDBACK_ASSIGNMENT_CODE)

        return {"feedback_url":feedback_url, "BF_pdf_file": "BiopharmSeltek/BioPharm.pdf", "ST_pdf_file": "BiopharmSeltek/Seltek.pdf"}



page_sequence = [
    Introduction,
    Seltek_materials,
    Biopharm_materials,
    Preferences_input_BF,
    Preferences_input_ST,
    Planning_doc,
    Prep_done,
    Meeting_wait,
    Partner_reveal,
    Seltek_materials_timer,
    BioPharm_materials_timer,
    Negotiated_outcome_one,
    Negotiated_outcome_deal,
    Negotiated_outcome_nodeal,
    Outcome_wait,
    Reflection_page
]
