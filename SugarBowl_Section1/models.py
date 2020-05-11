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
Negotatiing Sugar Bowl with a partner via email.
"""

with open("_rooms/Sp20_1.txt", "r") as f:
    raw_string = f.read()
    names_section1 = raw_string.replace("\n", ",")

with open("_rooms/Sp20_2.txt", "r") as f:
    raw_string = f.read()
    names_section2 = raw_string.replace("\n", ",")

SUNet_to_name = {'cumminsm':"Matt C","jomohu":"Joshua H","extra_01":"Unknown","extra_02":"Unknown","extra_03":"Unknown","extra_04":"Unknown","extra_05":"Unknown","extra_06":"Unknown",'andreaar': 'Andrea A. R.','kha915': 'Khaled A','rbadlani': 'Rohan B','nellb': 'Nell B','cryer': 'Andrew C','brian644': 'Brian E','jfagan2': 'John F','mkgold': 'Melanie G','mwhabib': 'Marc H','alfredoh': 'Alfredo H','jenn7790': 'Jenn K','casimira': 'Casi K','lkyaw3': 'Lin K','jlopata2': 'Jen L','smacq': 'Spencer M','hmaha': 'Harry M','ymeier': 'Yannick M','jmorcos': 'Joseph M','bhn': 'Bader N','stoneng': 'Stone N','judypark': 'Judy P','apinelli': 'Andrew P','prash20': 'Prashanth P','broch': 'Brett R','dsabada': 'Deepak S','pstiefel': 'Philip S','cszmutko': 'Carl S','dvas': 'David V','joewalt': 'Joseph W','linghanz': 'Michael Z','mxzoller': 'Maximilian Z','dejiabe': 'Deji A','zaxayon7': 'Ankit B','demeng': 'Demeng C','kc7': 'Kyle C','yuriydov': 'Yuriy D','mariaeg': 'Maria E','mgants': 'Michael G','tgerhart': 'Toby G','steveng3': 'Steven G','lawanson': 'Ruth L','zuber': 'Zuber M','jmilch': 'Julia M','ninimoor': 'Nini M','ianp12': 'Ian P','mgreeves': 'Mary-Grace R','lrengifo': 'Luis R','sagastuy': 'Maitane S','asayall': 'Alysha S','susa': 'Susannah S','yanivs': 'Yaniv S','csmurro': 'Clio S','rossv': 'Ross V','tinayyu': 'Tina Y','azehfuss': 'Anja Z',"atwell":"Tommy A","ermeehan":"Erica M","rossv":"Ross V","kaoutar": "Kaoutar Y"}


class Constants(BaseConstants):
    name_in_url = 'Sugar_Bowl_Section_1'
    players_per_group = 2
    num_rounds = 1

    reading_time = 5 #minutes
    material_button_show= .02 #minutes
    material_button_show_no_timer= .02 #minutes
    calculator_time = 5 #minutes
    planning_doc_time= 5 # minutes
    negotiating_time = 25 # minutes

    planning_doc_length = 150 #words

    section_1_participants = names_section1.split(",")
    section_2_participants = names_section2.split(",")
    SUNet_to_name = SUNet_to_name



class Subsession(BaseSubsession):
    def creating_session(self):
        names = Constants.section_1_participants.copy()
        for p in self.get_players():
            p.participant.label = names.pop(0)


class Group(BaseGroup):
    final_price = models.IntegerField(label="What was the final purchase price in USD?")
    who_purchased = models.StringField(choices=["Buyer","Dealer"],label="Which party purchased the sugar bowl?")
    initial_offer = models.IntegerField(label="If you were going to make an offer in your initial email (you might not!), what would the price be (in USD)?")
    reservation_price_dealer = models.IntegerField(label="What is your reservation price in USD for this piece?")
    target_price_dealer = models.IntegerField(label="What is your aspiration price in USD for this piece?")
    reservation_price_buyer = models.IntegerField(label="What is your reservation price in USD for this piece?")

class Player(BasePlayer):

    planning_text = models.LongStringField(label="Describe your plan for this negotiation")
    journaling_text = models.LongStringField(label="Please describe your experience of the negotiation. In what ways was negotiating via email different than through Zoom?")



    def role(self):
        if self.id_in_group == 1:
            return 'buyer'
        else:
            return 'dealer'
