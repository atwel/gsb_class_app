import random

from otree.api import *


author = 'Jon Atwell'
doc = """
Negotating OmniChannel with two teams
"""

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


class C(BaseConstants):
    NAME_IN_URL = 'OC'
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 1
    COORDINATING_TIME = 30
    NEGOTIATING_TIME = 75
    CLASSCODE = 190881
    PLANNING_ASSIGNMENT_CODE = 610671
    FEEDBACK_ASSIGNMENT_CODE = 610877

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    name = models.StringField()

def role(player: Player):
    try:
        player.name = SUNet_to_name[player.participant.label]
        # self.participant.label = SUNet_to_name[self.participant.label]
    except:
        pass
    if player.id_in_group == 1:
        return '3dtv'
    elif player.id_in_group == 2:
        return 'omni'
    elif player.id_in_group == 3:
        return '3dtv'
    elif player.id_in_group == 4:
        return 'omni'
    elif player.id_in_group == 5:
        return '3dtv'
    else:
        return 'omni'



class Introduction(Page):
    form_model = "player"

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        try:
            player.name = SUNet_to_name[player.participant.label]
        except:
            player.participant.vars["name"] = "(come see Dr. Atwell)"



class DTV(Page):
    form_model = "player"
    # timeout_seconds= C.READING_TIME * 60
    # timer_text = 'Time left for reading the materials'
    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "3dtv"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "OmniChannel/3DTV.pdf"}


class Omni(Page):
    form_model = "player"
    # timeout_seconds= C.READING_TIME * 60
    # timer_text = 'Time left for reading the materials'
    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "omni"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "OmniChannel/OmniChannel.pdf"}


class Planning_doc(Page):
    form_model = "player"
    # timeout_seconds= C.PLANNING_DOC_TIME * 60
    # timer_text = 'Time left to finish writing your planning document'

    @staticmethod
    def vars_for_template(player: Player):
        url  = "/{}/assignments/{}".format(C.CLASSCODE, C.PLANNING_ASSIGNMENT_CODE)
        if role(player) == "3dtv":
            return {
                "pdf_file": "OmniChannel/3DTV.pdf",
                "assignment_url": url,
                "submission_time": "two hours before class"
            }
        elif role(player) == "omni":
            return {
                "pdf_file": "OmniChannel/OmniChannel.pdf",
                "assignment_url": url,
                "submission_time": "two hours before class"
            }


class Outro(Page):
    form_model = "group"


page_sequence = [
    Introduction,
    DTV,
    Omni,
    Planning_doc,
    Outro
]
