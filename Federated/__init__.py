import datetime
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
    READING_TIME = 10
    PLANNING_DOC_TIME = 10
    NEGOTIATING_TIME = 30
    CLASSCODE = 180595
    PLANNING_ASSIGNMENT_CODE = 542285
    REFLECTION_ASSIGNMENT_CODE = 542286
    FEEDBACK_ASSIGNMENT_CODE = 560154

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    stockman = models.BooleanField()
    pairing = models.StringField()
    end_time = models.StringField()
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
    group.end_time = (
        datetime.datetime.now() + datetime.timedelta(minutes=C.NEGOTIATING_TIME + 1)
    ).strftime("%H:%M:%S")
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
    "addachan":"Addie Achan",
    "jand271": "Jason Anderson",
    "sbeaton":"Stephen Beaton",
    "lbrito":"Louise Brito",
    "vcharoon":"Victor Charoonsophonsak",
    "rchun1":"Robert Chun",
    "dowlingp":"Patrick Dowling",
    "laurajg":"Laura Griffiths",
    "ruthguan":"Ruth Guan",
    "whooper":"Whitney Hooper",
    "exyhuang":"Eileen Huang",
    "thuang24":"Tony Huang",
    "adrianus":"Adrian Hunggara",
    "shubhij":"Shubhi Jain",
    "noorissa":"Noorissa Khoja",
    "lroberds":"Lia Lilleness",
    "clifflim":"Cliff Lim",
    "amaderoo":"Andrea Madero",
    "mcgarryg":"Gavin McGarry",
    "knyman":"Knut Nyman",
    "jphaneuf":"Jeff Phaneuf",
    "dansegev":"Dan Segev",
    "bsinghla":"Bharti Singhla",
    "smithc52":"Christian Smith",
    "sesuarez":"Sofia Suarez",
    "avaldi":"Adolfo Valdivieso Quiroz",
    "gbreeves":"Bear Vasquez",
    "bwilber":"Bryce Wilberding",
    "ijdelcid":"Imer del Cid",
    "nnandrew":"Nick Andrews",
    "ebendezu":"Edgar Bendezú",
    "darapc":"Dara Canavan",
    "nchedid":"Nicholas Chedid",
    "tdodson":"Trey Dodson III",
    "storeydk":"Storey Dyer Kloman",
    "aevenson":"Austin Evenson",
    "onf":"Oren Fliegelman",
    "asjfu":"Allison Fu",
    "lfunke":"Lennart Funke",
    "dhersh":"Daniel Hersh",
    "cjanis":"Chad Janis",
    "sjonn":"Sarah Jonn",
    "ajow":"Alex Jow",
    "alacey":"Alex Lacey",
    "rlhannah":"Hannah Lee",
    "brlobato":"Breno Lobato",
    "grantmcn":"Grant McNaughton",
    "gaamello":"Gui Mello",
    "hneffa":"Henrique Neffa",
    "rspark":"Rachel Park",
    "pressler":"Sam Pressler",
    "athomp10":"Alexander Thompson",
    "jamesu":"James Underwood",
    "jaw33":"Jelani Williamson",
    "paulyap":"Paul Yap",
    "alexyin":"Alex Yin",
    "sszou ":"Sophia Sun Alex",
    "jdacosta":"James da Costa"}


class IntroWaitPage(WaitPage):
    group_by_arrival_time = True

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": "Waiting for others",
            "body_text": "Please wait a moment while you're assigned to a group.\n\n",
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
    timeout_seconds = C.READING_TIME*60
    timer_text = 'Time left for reading the materials'

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "stockman"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Federated/Stockman.pdf"}


class Stockman_nt(Page):
    form_model = "player"
    template_name = "Federated/Stockman.html"

    timeout_seconds = C.NEGOTIATING_TIME*60
    timer_text = 'Time left for negotiating'
    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "stockman"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Federated/Stockman.pdf"}


class Turbo(Page):
    form_model = "player"
    timeout_seconds = C.READING_TIME*60
    timer_text = 'Time left for reading the materials'

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "turbo"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Federated/Turbo.pdf"}


class Turbo_nt(Page):
    form_model = "player"
    template_name = "Federated/Turbo.html"

    timeout_seconds = C.NEGOTIATING_TIME*60
    timer_text = 'Time left for negotiating'

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "turbo"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Federated/Turbo.pdf"}


class United(Page):
    form_model = "player"
    timeout_seconds = C.READING_TIME*60
    timer_text = 'Time left for reading the materials'

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "united"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Federated/United.pdf"}



class United_nt(Page):
    form_model = "player"
    template_name = "Federated/United.html"

    timeout_seconds = C.NEGOTIATING_TIME*60
    timer_text = 'Time left for negotiating'

    @staticmethod
    def is_displayed(player: Player):
        return role(player) == "united"

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "Federated/United.pdf"}



class Planning_doc(Page):
    form_model = "player"
    timeout_seconds = C.PLANNING_DOC_TIME *60
    timer_text = "Time left to finish the planning document"

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


class Wait_to_negotiate(WaitPage):
    form_model = "group"

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": "Waiting for your counterparts to finish preparing",
            "body_text": "It shouldn't be too long now!\n\n",
        }


class Back_to_class(Page):
    form_model = "player"

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
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


class Feedback_consent(Page):
    form_model = "player"
    form_fields = ["consent", "review_consent"]

class ConsentWaitPage(WaitPage):

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": "Waiting...",
            "body_text": "Please wait while your partner considers whether they want feedback",
        }

class Reflection_page(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player: Player):
        feedback_url = "/{}/assignments/{}".format(C.CLASSCODE, C.FEEDBACK_ASSIGNMENT_CODE)
        reflection_url = "/{}/assignments/{}".format(C.CLASSCODE, C.REFLECTION_ASSIGNMENT_CODE)

        if player.review_consent:
            willing = []
            for p in player.get_others_in_group():
                if p.consent:
                    willing.append(p.name)
            if len(willing)==2:
                fb_str="{} and {} are".format(willing[0], willing[1])
                player.feedback = True
            elif len(willing)==1:
                fb_str = "{} is".format(willing[0])
                player.feedback = True
            else:
                fb_str = ""
                player.feedback = False
        else:
            player.feedback = False
            fb_str=""
        return {"feedback_url":feedback_url, "reflection_url":reflection_url, "feedback_names":fb_str}

class Outro(Page):
    form_model = "group"


page_sequence = [
    Introduction,
    Stockman,
    Turbo,
    United,
    Planning_doc,
    Ready_for_class,
    Wait_to_negotiate,
    Back_to_class,
    Stockman_nt,
    Turbo_nt,
    United_nt,
    Outcome,
    Feedback_consent,
    ConsentWaitPage,
    Reflection_page,
    Outro,
]
