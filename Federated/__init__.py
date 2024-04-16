import time
import itertools
import random

from otree.api import *


author = 'Jon Atwell'
doc = """
Negotiating Federated Sciences with two partners
"""


class C(BaseConstants):
    NAME_IN_URL = 'Federated_Sciences'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    NEGOTIATING_TIME = 30
    CLASSCODE = 190881
    PLANNING_ASSIGNMENT_CODE = 610583
    FEEDBACK_ASSIGNMENT_CODE = 610729

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    stockman = models.BooleanField()
    pairing = models.StringField()
    end_time = models.FloatField()
    started = models.BooleanField(initial=False)


class Player(BasePlayer):
    name = models.StringField()
    united = models.IntegerField()
    turbo = models.IntegerField()
    stockman = models.IntegerField()
    first_meeting = models.StringField(
        label="Whom did Turbo start the negotiation with?",
        choices=["Stockman", "United", "Both"],
        widget=widgets.RadioSelectHorizontal,
    )
    partner_name = models.StringField()
    feedback = models.BooleanField()
    consent = models.BooleanField(label="Are you willing to RECEIVE constructive feedback from your negotiation partner?")
    review_consent = models.BooleanField(label="Similarly, are you willing to GIVE constructive feedback to your negotiation partner?")

# FUNCTIONS
def creating_session(subsession: Subsession):
    stock = itertools.cycle([True, False])
    for g in subsession.get_groups():
        g.stockman = next(stock)


def set_end_time(group: Group):

    start_time = time.time()
    for player in group.get_players():
        player.participant.vars["sim_timer"] = start_time + C.NEGOTIATING_TIME * 60
    #).strftime("%H:%M:%S")
    group.started = True


def set_first_meet(group: Group):
    for i, p in enumerate(group.get_players()):
        try:
            p.name = SUNet_to_name[p.participant.label]
        except:
            p.name = "Demo_{}".format(i)
    for p in group.get_players():
        if p.role() == "stockman":
            stockman = p.name
        elif p.role() == "turbo":
            turbo = p.name
        else:
            united = p.name
    if group.stockman:
        group.pairing = ",".join([united, stockman, turbo])
    else:
        group.pairing = ",".join([united, turbo, stockman])


def role(player: Player):
    if player.id_in_group == 1:
        return 'stockman'
    elif player.id_in_group == 2:
        return 'turbo'
    else:
        return 'united'


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


class Introduction(Page):
    form_model = "player"

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        try:
            player.name = SUNet_to_name[player.participant.label]
        except:
            player.name = "(come see Dr. Atwell)"


class Stockman(Page):
    form_model = "player"


    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "stockman"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Federated/Stockman.pdf"}


class Stockman_nt(Page):
    form_model = "player"
    template_name = "Federated/Stockman.html"

    timer_text = 'Time left for negotiating'
    def get_timeout_seconds(player):
        return player.participant.vars["sim_timer"] - time.time()


    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "stockman"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Federated/Stockman.pdf"}


class Turbo(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "turbo"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Federated/Turbo.pdf"}


class Turbo_nt(Page):
    form_model = "player"
    template_name = "Federated/Turbo.html"
    timer_text = 'Time left for negotiating'

    def get_timeout_seconds(player):
        return player.participant.vars["sim_timer"] - time.time()

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "turbo"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Federated/Turbo.pdf"}


class United(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "united"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Federated/United.pdf"}


class United_nt(Page):
    form_model = "player"
    template_name = "Federated/United.html"
    timer_text = 'Time left for negotiating'

    def get_timeout_seconds(player):
        return player.participant.vars["sim_timer"] - time.time()

    timer_text = 'Time left for negotiating'

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "united"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Federated/United.pdf"}



class Planning_doc(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player: Player):
        url  = "/{}/assignments/{}".format(C.CLASSCODE, C.PLANNING_ASSIGNMENT_CODE)
        if role(player) == "stockman":
            return {"pdf_file": "Federated/Stockman.pdf", "assignment_url":url}
        elif role(player) == "turbo":
            return {"pdf_file": "Federated/Turbo.pdf", "assignment_url":url}
        elif role(player) == "united":
            return {"pdf_file": "Federated/United.pdf", "assignment_url":url}


class Ready_for_class(Page):
    form_model = "player"



class Back_to_class(Page):
    form_model = "player"

    @staticmethod
    def before_next_page(player: Player,timeout_happened):
        if not player.group.started:
            set_end_time(player.group)

    @staticmethod
    def vars_for_template(player: Player):
        partners = player.get_others_in_group()
        part_1 = partners[0].name
        part_2 = partners[1].name
        if player.group.stockman:
            if role(player) == "united":
                return {
                    "rep": "United",
                    "alter": "Stockman",
                    "in_first": True,
                    "partner_1": part_1,
                    "partner_2": part_2,
                }
            elif role(player) == "stockman":
                return {
                    "alter": "United",
                    "rep": "Stockman",
                    "in_first": True,
                    "partner_1": part_1,
                    "partner_2": part_2,
                }
            else:
                return {
                    "rep": "Turbo",
                    "alter": "NA",
                    "in_first": False,
                    "partner_1": part_1,
                    "partner_2": part_2,
                }
        else:
            if role(player) == "united":
                return {
                    "rep": "United",
                    "alter": "Turbo",
                    "in_first": True,
                    "partner_1": part_1,
                    "partner_2": part_2,
                }
            elif role(player) == "turbo":
                return {
                    "alter": "United",
                    "rep": "Turbo",
                    "in_first": True,
                    "partner_1": part_1,
                    "partner_2": part_2,
                }
            else:
                return {
                    "rep": "Stockman",
                    "alter": "NA",
                    "in_first": False,
                    "partner_1": part_1,
                    "partner_2": part_2,
                }


class Outcome(Page):
    form_model = "player"
    form_fields = ["united", "stockman", "turbo", "first_meeting"]

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "stockman"

class Feedback_page(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player: Player):
        feedback_url = "/{}/assignments/{}".format(C.CLASSCODE, C.FEEDBACK_ASSIGNMENT_CODE)
        others = player.get_others_in_group()
        fb_str="{} and {} are".format(others[0].name, others[1].name)
        return {"feedback_url":feedback_url, "feedback_names":fb_str}

class Outro(Page):
    form_model = "group"


page_sequence = [
    Introduction,
    Stockman,
    Turbo,
    United,
    Planning_doc,
    Ready_for_class,
    Back_to_class,
    Stockman_nt,
    Turbo_nt,
    United_nt,
    Outcome,
    Feedback_page,
    Outro,
]
