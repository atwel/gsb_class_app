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
    NEGOTIATING_TIME = 25
    CLASSCODE = 180595
    PLANNING_ASSIGNMENT_CODE = 542282
    REFLECTION_ASSIGNMENT_CODE = 542283
    FEEDBACK_ASSIGNMENT_CODE = 560007

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):

    initial_price = models.CurrencyField(
        label="What was the price of the first offer? (In millions of USD [e.g. $XX.xx])"
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
        label="What was the last offer made by BioPharm? (In millions of USD [e.g. $XX.xx])"
    )
    last_Seltek = models.CurrencyField(
        label="What was the last offer made by Seltek? (In millions of USD [e.g. $XX.xx])"
    )
    final_sale_price = models.CurrencyField(
        label="What was the Final Sale Price? (In millions of USD [e.g. $XX.xx])"
    )
    batna_BF = models.CurrencyField(
        label="At what price in millions of USD should you walk away without a deal?"
    )
    target_BF = models.CurrencyField(
        label="What is your ideal purchase price for the Seltek plant?  (In millions of USD [e.g. $XX.xx])"
    )
    batna_ST = models.CurrencyField(
        label="At what price in millions of USD should you walk away without a deal?"
    )
    target_ST = models.CurrencyField(
        label="What is your ideal sale price for your plant?  (In millions of USD [e.g. $XX.xx])"
    )
    nego_time = models.IntegerField()


class Player(BasePlayer):
    planning_text = models.LongStringField(label="Describe your plan for this negotiation.")
    journaling_text = models.LongStringField(
        label="Please describe your experience of the negotiation."
    )
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
        player.participant.vars["sim_timer"] = start_time + C.NEGOTIATING_TIME * 60 + 120


class IntroWaitPage(WaitPage):
    group_by_arrival_time = True

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": "Hang tight",
            "body_text": "Please wait a moment to get paired.\n\nIf you've been on this page for a while, try refreshing the page.",
        }


class Introduction(Page):
    form_model = "player"

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        try:
            name =" ".join(player.participant.label.split("_"))
            player.participant.vars["name"] = name
        except:
            try:
                name = player.participant.label.split("_")[0]
                player.participant.vars["name"] = name
            except:
                player.participant.vars["name"] = "NOT PROVIDED"
        player.name = player.participant.vars["name"]

    @staticmethod
    def vars_for_template(player: Player):
        total_time = (
            C.READING_TIME
            + C.PLANNING_DOC_TIME_MINUTES
            + C.NEGOTIATING_TIME
            + 5
        )
        return {"reading_limit": C.READING_TIME, "total_time": total_time}


class Seltek_materials(Page):
    form_model = "player"
    timeout_seconds = C.READING_TIME * 60
    timer_text = 'Time left for reading the materials'

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "BiopharmSeltek/Seltek.pdf"}


class Biopharm_materials(Page):
    form_model = "player"
    timeout_seconds = C.READING_TIME * 60
    timer_text = 'Time left for reading the materials'

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "BiopharmSeltek/BioPharm.pdf"}


class Preferences_input_ST(Page):
    form_model = "group"
    form_fields = ['target_ST', "batna_ST"]
    timeout_seconds = 120
    timer_text = 'Time left to input values'

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "BiopharmSeltek/Seltek.pdf"}


class Preferences_input_BF(Page):
    form_model = "group"
    form_fields = ['target_BF', "batna_BF"]
    timeout_seconds = 120
    timer_text = 'Time left to input values'

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "BiopharmSeltek/BioPharm.pdf"}


class Planning_doc(Page):
    form_model = "player"
    timeout_seconds = C.PLANNING_DOC_TIME_MINUTES * 60
    timer_text = 'Time left for writing your document:'

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


class Partner_reveal(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player: Player):
        partner = player.get_others_in_group()[0]
        player.partner_name = partner.name#participant.vars["name"]
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
            "body_text": "We're waiting for your counterparty to be ready. Once they are done preparing, you'll advance to the next page and learn who they are.",
        }


class Seltek_materials_no_timer(Page):
    form_model = "player"
    template_name = "BiopharmSeltek/Seltek_materials.html"
    timer_text = 'Time left for negotiating the case:'

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.participant.vars["sim_timer"] - time.time()

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {"pdf_file": "BiopharmSeltek/Seltek.pdf"}


class BioPharm_materials_no_timer(Page):
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


class Negotiated_outcome_two(Page):
    form_model = "group"

    @staticmethod
    def get_form_fields(player: Player):
        if player.group.deal:
            return ['final_sale_price']
        else:
            return ["last_Seltek", "last_Biopharm"]

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
                "body_text": "Wait a moment while the BioPharm representative finishes inputting the results.\n\n",
            }
        else:
            return {
                "title_text": "Waiting",
                "body_text": "Wait a moment for the Seltek representative.\n\n",
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
        return {"feedback_url":feedback_url, "reflection_url":reflection_url, "BF_pdf_file": "BiopharmSeltek/BioPharm.pdf", "ST_pdf_file": "BiopharmSeltek/Seltek.pdf"}



page_sequence = [
    IntroWaitPage,
    Introduction,
    Seltek_materials,
    Biopharm_materials,
    Preferences_input_BF,
    Preferences_input_ST,
    Planning_doc,
    Meeting_wait,
    Partner_reveal,
    Seltek_materials_no_timer,
    BioPharm_materials_no_timer,
    Negotiated_outcome_one,
    Negotiated_outcome_two,
    Outcome_wait,
    Feedback_consent,
    ConsentWaitPage,
    Reflection_page
]
