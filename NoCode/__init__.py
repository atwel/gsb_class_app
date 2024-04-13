import time

from otree.api import *


author = 'Jon Atwell'
doc = """
Negotatiing No Code, Inc with a partner
"""


class C(BaseConstants):
    NAME_IN_URL = 'NoCode'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    NEGOTIATION_TIME = 35
    CLASSCODE = 190881
    PLANNING_ASSIGNMENT_CODE = 610576
    FEEDBACK_ASSIGNMENT_CODE = 610723


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    deal = models.BooleanField(
        label="Did Stanfield and Sproles reach a deal?", widget=widgets.RadioSelectHorizontal
    )
    Salary = models.CurrencyField(label="What is the salary?")
    Bonus = models.CurrencyField(label="What is the bonus?")
    Equity = models.FloatField(label="What is the equity amount (%)?")
    Days = models.StringField(
        label="How many days a week can be remote?",
        choices=["Zero", "One", "Two or Three"],
        widget=widgets.RadioSelectHorizontal,
    )
    Start = models.IntegerField(
        label="When will Stanfield start?",
        choices=[[1, "Immediately"], [2, "Three Months"], [3, "Fifteen Months"], [4, "No Start"]],
        widget=widgets.RadioSelectHorizontal,
    )
    last_Salary_Stanfield = models.CurrencyField(
        label="What was the last salary Stanfield asked for?"
    )
    last_Bonus_Stanfield = models.CurrencyField(
        label="What was the last bonus Stanfield asked for?"
    )
    last_Equity_Stanfield = models.FloatField(
        label="What was the last equity amount Stanfield asked for?"
    )
    last_Days_Stanfield = models.StringField(
        label="How many remote days did Stanfield last ask for?",
        choices=["Zero", "One", "Two or Three"],
        widget=widgets.RadioSelectHorizontal,
    )
    last_Start_Stanfield = models.IntegerField(
        label="In what timeframe did Stanfield last ask to start?",
        choices=[[1, "Immediately"], [2, "Three Months"], [3, "Fifteen Months"], [4, "No Start"]],
        widget=widgets.RadioSelectHorizontal,
    )
    last_Salary_Sproles = models.CurrencyField(label="What was the last salary Sproles proposed?")
    last_Bonus_Sproles = models.CurrencyField(label="What was the last bonus Sproles proposed?")
    last_Equity_Sproles = models.FloatField(
        label="What was the last equity amount Sproles proposed?"
    )
    last_Days_Sproles = models.StringField(
        label="How many remote days did Sproles last propose?",
        choices=["Zero", "One", "Two or Three"],
        widget=widgets.RadioSelectHorizontal,
    )
    last_Start_Sproles = models.IntegerField(
        label="What timeframe for Stanfield's start did Sproles last propose?",
        choices=[[1, "Immediately"], [2, "Three Months"], [3, "Fifteen Months"], [4, "No Start"]],
        widget=widgets.RadioSelectHorizontal,
    )

class Player(BasePlayer):
    name = models.StringField()
    grole = models.StringField()
    partner_name = models.StringField()

    most_important = models.StringField(
            label="Which issue is most important to you?",
            choices=["Start date", "Salary", "Bonus", "Equity", "Remote work options"],
        )
    second_important = models.StringField(
                label="Which issue is second most important to you?",
                choices=["Start date", "Salary", "Bonus", "Equity", "Remote work options"],
            )
    least_important = models.StringField(
                label="Which issue is least important to you?",
                choices=["Start date", "Salary", "Bonus", "Equity", "Remote work options"],
            )


# FUNCTIONS
def set_timer(group: Group):
    start_time = time.time()
    for player in group.get_players():
        player.participant.vars["sim_timer"] = start_time + C.NEGOTIATION_TIME * 60 + 120

# PAGES
SUNet_to_name = {
"Extra_1": "Unnamed #1",
"Extra_2": "Unnamed #2",
"Extra_3": "Unnamed #3",
"Extra_4": "Unnamed #4",
"Extra_5": "Unnamed #5",
"Extra_6": "Unnamed #6",
"Extra_7": "Unnamed #7",
"Extra_8": "Unnamed #8",
"Extra_9": "Unnamed #9",
"Extra_10": "Unnamed #10",
'jpbda':'Joao Almeida',
'rbayne':'Ryan Bayne',
'cblanck':'Caroline Blanck',
'oliviacn':'Olivia Somerlyn Hollins Christensen',
'vfanelle':'Valerie Fanelle',
'afatsche':'Andreas Fatschel',
'cgonzal':'Cayo Alexander Gonzalez',
'yaqi':'Yaqi Grover',
'jonhoey':'Jon W. L. Hoey',
'vkanodia':'Vikram Kanodia',
'dongsukl':'Paul Lee',
'levinez':'Zach James Levine',
'lexielin':'Lexie Lin',
'raachini':'Anthony Mattar El Raachini',
'lmaymar':'Lauren Maymar',
'sashan':'Sasha Nanda',
'kdnelson':'Kyle DeVille Nelson',
'fnkameni':'Floriane Ngako Kameni',
'oke':'Oke Osevwe',
'suppapat':'Suppapat Ken Pattarasittiwate',
'peniston':'Olivia Lyerly Peniston',
'petrichp':'Petra Petrich',
'joshpick':'Josh Pickering',
'mpierce':'Melanie Pierce',
'rcquinn':'Riley Christopher Quinn',
'annarowe':'Anna Rowe',
'nsvan':'Natia Svanidze',
'isabelvg':'Isabel Vallina Garcia',
'bgward':'Brad Ward',
'jyao10':'Julia Yao',
'nazerke':'Naza Aibar',
'mfahim':'Maha Al Fahim',
'mansell':'Mark Garo Ansell',
'dabacci':'Diego Bacci',
'wilclark':'Will Clark',
'rakiyac':'Rakiya Cunningham',
'tylererb':'Tyler Tyler Erb',
'irvhsu':'Irving Hsu',
'kwjk':'Katharine Jessiman-Ketcham',
'dkurup':'Deepika Kurup',
'clevy25':'Caroline Levy',
'bmaina':'Ndirangu Bryan Maina',
'marwanga':'Moraa Marwango',
'alexjmcc':'Alex Justin McCarthy',
'akm24':'Adam Merrill',
'mmoiz':'Munim Moiz',
'arinze':'Arinze Nwagbata',
'gloriao':'Gloria Ijeoma Odoemelam',
'pparas37':'Paulina Paras',
'arushis':'Arushi Sharma',
'zstiles':'Zane Stiles',
'cavarres':'Camila Vargas Restrepo',
'wangjess':'Jessica Wang',
'cmweiner':'Charlotte Weiner',
'capujol':'Claudia Álvarez Pujol',
'niranja9':'Niranjan Balachandar',
'cbeckma3':'Chris Beckmann',
'jhcohen':'Josh Harrison Cohen',
'emduarte':'Emily Duarte',
'mandygao':'Mandy Gao',
'sgarciav':'Santiago Garcia Vargas',
'krjindal':'Kripanshi Jindal',
'estherk1':'Esther Kamgaing',
'aklee33':'Alexander Keith Lee',
'helenjlu':'Helen Lu',
'mmont':'Mason Montgomery',
'hmurdoch':'Hannah Murdoch',
'gyutae95':'Terry Park',
'npatel21':'Neal Atul Patel',
'atpims':'Alan Tomás Pimstein',
'orosen':'Olivia Ellen Rosen',
'erubini':'Eduardo Rubini',
'willzhou':'Will Zhou'
}


class IntroWaitPage(WaitPage):
    group_by_arrival_time = True

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": "Hang tight",
            "body_text": "Please wait a moment to get paired.\n\nIf you've been on this page for a while, try refreshing the page or flagging down Dr. Atwell.",
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
        total_time = (C.NEGOTIATION_TIME+ 5)

        return {"total_time": total_time}


class Stanfield_materials(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "pdf_file": "NoCode/Stanfield.pdf",
            "xlsx_file": "NoCode/Stanfield Point System.xlsx",
        }


class Sproles_materials(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "NoCode/Sproles.pdf", "xlsx_file": "NoCode/Sproles Point System.xlsx"}


class Target_input(Page):
    form_model = "player"
    form_fields = ['most_important', 'second_important', 'least_important']

    @staticmethod
    def vars_for_template(player: Player):
        if player.id_in_group == 1:
            return {
                "pdf_file": "NoCode/Stanfield.pdf",
                "xlsx_file": "NoCode/Stanfield Point System.xlsx",
            }
        if player.id_in_group == 2:
            return {
                "pdf_file": "NoCode/Sproles.pdf",
                "xlsx_file": "NoCode/Sproles Point System.xlsx",
            }


class Planning_doc(Page):
    form_model = "player"
    # timeout_seconds= C.PLANNING_DOC_TIME_MINUTES * 60
    # timer_text = 'Time left for writing your document:'
    @staticmethod
    def vars_for_template(player: Player):
        if player.id_in_group == 1:
            return {
                "pdf_file": "NoCode/Stanfield.pdf",
                "xlsx_file": "NoCode/Stanfield Point System.xlsx",
                "assignment_url":"/{}/assignments/{}".format(C.CLASSCODE, C.PLANNING_ASSIGNMENT_CODE)
                }
        if player.id_in_group == 2:
            return {
                "pdf_file": "NoCode/Sproles.pdf",
                "xlsx_file": "NoCode/Sproles Point System.xlsx",
                "assignment_url":"/{}/assignments/{}".format(C.CLASSCODE, C.PLANNING_ASSIGNMENT_CODE)
            }

class Prep_done(Page):
    form_model = "player"



class Partner_reveal(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player: Player):
        partner = player.get_others_in_group()[0]
        player.partner_name = partner.participant.vars["name"]
        if player.id_in_group == 1:
            player.grole = "Stanfield"
        else:
            player.grole = "Sproles"
        return {
            "negotiating_time": C.NEGOTIATION_TIME,
            "partner": partner.participant.vars["name"],
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.vars["sim_timer"] = time.time() + C.NEGOTIATION_TIME * 60


class Stanfield_materials_timer(Page):
    form_model = "player"
    template_name = "NoCode/Stanfield_materials.html"
    timer_text = 'Time left to negotiate the case'

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.participant.vars["sim_timer"] - time.time()

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "pdf_file": "NoCode/Stanfield.pdf",
            "xlsx_file": "NoCode/Stanfield Point System.xlsx",
        }


class Sproles_materials_timer(Page):
    form_model = "player"
    template_name = "NoCode/Sproles_materials.html"
    timer_text = 'Time left to negotiate the case'

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.participant.vars["sim_timer"] - time.time()

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "NoCode/Sproles.pdf", "xlsx_file": "NoCode/Sproles Point System.xlsx"}


class Negotiated_outcome_one(Page):
    form_model = "group"
    form_fields = ["deal"]

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2


class Negotiated_outcome_two(Page):
    form_model = "group"

    @staticmethod
    def get_form_fields(player: Player):
        if player.group.deal:
            return ["Salary", "Bonus", "Equity", "Days", "Start"]
        else:
            return [
                "last_Salary_Stanfield",
                "last_Bonus_Stanfield",
                "last_Equity_Stanfield",
                "last_Days_Stanfield",
                "last_Start_Stanfield",
                "last_Salary_Sproles",
                "last_Bonus_Sproles",
                "last_Equity_Sproles",
                "last_Days_Sproles",
                "last_Start_Sproles",
            ]

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2


class Outcome_wait(WaitPage):
    form_model = "group"

    @staticmethod
    def vars_for_template(player: Player):
        if player.id_in_group == 1:
            return {
                "title_text": "Reporting the outcome",
                "body_text": "Wait a moment while Sproles finishes inputting the results.\n\n",
            }
        else:
            return {
                "title_text": "Waiting",
                "body_text": "Wait a moment for both parties to advance.\n\n",
            }


class Feedback_page(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player: Player):
        feedback_url = "/{}/assignments/{}".format(C.CLASSCODE, C.FEEDBACK_ASSIGNMENT_CODE)

        return {"feedback_url":feedback_url, "Stanfield_pdf_file": "NoCode/Stanfield.pdf", "Sproles_pdf_file": "NoCode/Sproles.pdf","Stanfield_xlsx_file": "NoCode/Stanfield Point System.xlsx", "Sproles_xlsx_file": "NoCode/Sproles Point System.xlsx"}


page_sequence = [
    Introduction,
    Sproles_materials,
    Stanfield_materials,
    Planning_doc,
    Target_input,
    Prep_done,
    Partner_reveal,
    Sproles_materials_timer,
    Stanfield_materials_timer,
    Negotiated_outcome_one,
    Negotiated_outcome_two,
    Outcome_wait,
    Feedback_page
]
