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
    READING_TIME = 15
    NEGOTIATION_TIME = 25
    PLANNING_DOC_TIME_MINUTES = 10
    CLASSCODE = 180595
    PLANNING_ASSIGNMENT_CODE = 542292
    REFLECTION_ASSIGNMENT_CODE = 542293
    FEEDBACK_ASSIGNMENT_CODE = 560153


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
    target_points = models.IntegerField(label="What is your target amount of points to get from this negotiation?")
    name = models.StringField()
    grole = models.StringField()
    partner_name = models.StringField()
    feedback = models.BooleanField()
    consent = models.BooleanField(label="Are you willing to RECEIVE constructive feedback from your negotiation partner?")
    review_consent = models.BooleanField(label="Similarly, are you willing to GIVE constructive feedback to your negotiation partner?")

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
    "addachan":"Addie Achan",
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
        total_time = (
            C.READING_TIME
            + C.PLANNING_DOC_TIME_MINUTES
            + C.NEGOTIATION_TIME
            + 5
        )
        return {
            "reading_limit": C.READING_TIME,
            "total_time": total_time,
            "planning_doc_time": C.PLANNING_DOC_TIME_MINUTES,
        }


class Stanfield_materials(Page):
    form_model = "player"
    timeout_seconds= C.READING_TIME * 60
    timer_text = 'Time left for reading the materials'
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
    timeout_seconds= C.READING_TIME * 60
    timer_text = 'Time left for reading the materials'
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "NoCode/Sproles.pdf", "xlsx_file": "NoCode/Sproles Point System.xlsx"}


class Target_input(Page):
    form_model = "player"
    form_fields = ['target_points']

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


class Meeting_wait(WaitPage):
    form_model = "group"
    after_all_players_arrive = 'set_timer'

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": "Waiting...",
            "body_text": "We're waiting for your counterparty to be ready. Once they finish up, you'll learn who it is. You'll then go back to the case materials page and the timed negotiation will begin.",
        }

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


class Stanfield_materials_no_timer(Page):
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


class Sproles_materials_no_timer(Page):
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

        if player.review_consent and player.get_others_in_group()[0].consent:
            player.feedback = True
        else:
            player.feedback = False
        return {"feedback_url":feedback_url, "reflection_url":reflection_url, "Stanfield_pdf_file": "NoCode/Stanfield.pdf", "Sproles_pdf_file": "NoCode/Sproles.pdf","Stanfield_xlsx_file": "NoCode/Stanfield Point System.xlsx", "Sproles_xlsx_file": "NoCode/Sproles Point System.xlsx"}


page_sequence = [
    IntroWaitPage,
    Introduction,
    Sproles_materials,
    Stanfield_materials,
    Planning_doc,
    Target_input,
    Meeting_wait,
    Partner_reveal,
    Sproles_materials_no_timer,
    Stanfield_materials_no_timer,
    Negotiated_outcome_one,
    Negotiated_outcome_two,
    Outcome_wait,
    Feedback_consent,
    ConsentWaitPage,
    Reflection_page
]
