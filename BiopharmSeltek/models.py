from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)



author = 'Jon Atwell'

doc = """
Negotatiing BioPharm Seltek with a partner
"""


class Constants(BaseConstants):
    name_in_url = 'BiopharmSeltek'
    players_per_group = 2
    num_rounds = 1
    reading_time = 6
    planning_doc_length = 150
    planning_doc_time_minutes = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    link = models.StringField(initial="https://stanford.zoom.us/j/4340648848",label="Stanford Zoom URL")
    initial_price = models.CurrencyField(label="What was the price of the first offer in millions of USD (e.g. XX.xx )?")
    made_initial = models.StringField(choices=["BioPharm","Seltek"], widget=widgets.RadioSelectHorizontal, label="Which company made the first offer?")
    deal = models.BooleanField(label="Did the companies reach a deal?",widget=widgets.RadioSelectHorizontal)
    last_Biopharm = models.CurrencyField(label="What was the last offer made by BioPharm in millions of USD (e.g. XX.x)?")
    last_Seltek = models.CurrencyField(label="What was the last offer made by Seltek in millions of USD (e.g. XX.xx)?")
    final_sale_price = models.CurrencyField(label="What was the Final Sale Price in millions of USD (e.g. XX.xx)?")
    batna_BF = models.CurrencyField(label="At what price in millions of USD should you walk away without a deal?")
    target_BF = models.CurrencyField(label="What is your ideal purchase price for the Seltek plant in millions of USD (e.g. XX.xx)?")
    batna_ST = models.CurrencyField(label="At what price in millions of USD should you walk away without a deal?")
    target_ST = models.CurrencyField(label="What is your ideal sale price for your plant in millions of USD (e.g. XX.x)?")

class Player(BasePlayer):
    planning_text = models.LongStringField(label="Describe your plan for this negotiation")
