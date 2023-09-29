from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

SUNet_to_name = {"oakkurt":"Ozlem Akkurt","sarahand":"Sarah Anderson","sankalpb":"Sankalp Banerjee","abertha":"Andrew Bertha","jhbuchel":"Jason Buchel","daviscm":"Carolyn Davis","mdicou":"Matt Dicou","dhfranks":"David Franks","jigs":"Jose Garcia Suarez","kgea":"Kathy Gea","ehuscher":"Elspeth Huscher","yvj":"Yash Jain","mlamdan":"Matan Lamdan","cdlince":"Carly Lincenberg","asmartin":"Anne-Sophie Martin","kmodukan":"Kesaobaka Modukanele","povalleb":"Pablo Ovalle","spatarca":"Santiago Patarca","leilap":"Leila Pirbay","kpolle":"Karen Polle","pretes":"Paola Petes Pineda","drichey":"Dan Rickey","wrodrig":"Wes Rodriguez","jrowley":"Josh Rowley","nishaad":"Nishaad Ruparel","juansaez":"Juan Saez Vera","talsarig":"Tal Sarig","nschlein":"Nate Schlein","mariasw":"Maria Silva Willson","kstein10":"Kate Steinman","tstone":"Thomas Stone","ianas":"Iana Stoytcheva","tejsun":"Tejas Sundaresan","mtakasak":"Midori Takasaki","stopper":"Sydni Topper","tjwater":"Tanner Waterstreet","eview":"Evie Woodforde","mzxie":"Michelle Xie","cqyuan":"Chris Yuan","edzhai":"Ethan Zhai","jrbz":"Justin Ziegler","taftab":"Taleha Aftab","oyinda":"Oyinda Ajayi","hajmani":"Hannah Ajmani","hrma":"Henrique Albuquerque","lallende":"Luife Allende","dalpuche":"Dominique Alpuche","annesan":"Annes An","casawa":"Chaitanya Asawa","sherb":"Sher Bhullar","jsburns":"James Burn","cc16":"Charlotte Camacho","ecambern":"Emily Cambern","iw1000":"Lucas Cheon","hamzac":"Hamza Choudery","ncole2":"Nyamekye Coleman","pcout":"Peter Coutoulas","adavis29":"Alexa Davis","sef07":"Steven Ferreira","wglick":"Whitney Glick","anna425":"Anna Gurevich","royhage":"Roy Hage","davidh7":"David Harrison","rbhuang":"Richard Huang","jh21":"Jonathan Hurowitz","andyjin":"Andy Jin","mjuzwiak":"Monika Juzwiak","hkling":"Henry Klingenstein","macklee":"Mackenzie Lee","levinelu":"Lucas Levine","natm":"Natalie Meurer","cliffmil":"Cliff Miller","jmorton4":"Jackson Morton","karlyosb":"Karly Osborne","playfair":"Katherine Playfair","yploder":"Yvonne Ploder","eportura":"Eliann Porturas","psaength":"Phanthila Saengthong","jsayadi":"Jamasb Sayadi","jeremycs":"Jeremy Scott","sheldon3":"Casey Sheldon","amys2023":"Amy Marie Slaughter","nsuchato":"Prao Suchato","m2taylor":"Margot Taylor","wilkinsj":"Jonathan Wilkins","kwolsten":"Kyle Wolstencroft","mzincone":"Michael Zincone","anibaldf":"Anibal de Frankenberg","tracycao":"Tracy Cao","amanc2":"Aman Chaudhary","crozelcm":"Claire Crozel","vdivi":"Vasu Divi","fadavi":"Faraz Fadavi","jhamying":"Julien Ham-Ying","shasson":"Sophie Hasson","srkarr":"S Karr","nkasper":"Nolan Kasper","bkhoo":"Bryan Khoo","akiam":"Alex Kiam","albertwj":"Albert Lee","diane8":"Diane Lee","jackylin":"Jacky Lin","samzliu":"Samuel Liu","sliu2022":"Stella Liu","jmunoz8":"Jaime Munoz Jr.","misatonk":"Misato Nakayama","lneise":"Luke Neise","sanvar":"Sanvar Oberoi","sraches":"Steven Rachesky","ramayya":"Sulekha Pamayya","lukeren":"Luke Ren","ninasab":"Nina Sabharwal","kshah1":"Kevin Shah","fsa":"Frances Simpson-Allen","dss93":"David Steiner","sunilrao":"Sunil Sudhakaran","yalew":"Yale Wang","mtw693":"Marshall Watkins","atwell":"Prof. Atwell","clide":"Chelsea Lide (CA)","lizixin":"Lambert Li (CA)","extra_01":"Unnamed #1","extra_02":"Unnamed #2","extra_03":"Unnamed #3","extra_04":"Unnamed #4","extra_05":"Unnamed #5","extra_06":"Unnamed #6"}


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



class Candidate(Page):
    form_model = "player"

    #timeout_seconds = Constants.reading_time*60
    #timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return True

    def vars_for_template(self):
        return {"pdf_file": "NewRecruit/Candidate.pdf"}

    def js_vars(self):
        return dict(button_show=0)#Constants.material_button_show*60000)


class Recruiter(Page):
    form_model = "player"

    #timeout_seconds = Constants.reading_time*60
    #timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return True

    def vars_for_template(self):
        return {"pdf_file": "NewRecruit/Recruiter.pdf"}

    def js_vars(self):
        return dict(button_show=0)#Constants.material_button_show*60000)


class Candidate_calculator(Page):
    form_model = "player"
    form_fields = []
    """['bonus',
                            'job_assignment',
                            'location',
                            'insurance_coverage',
                            'vacation_time',
                            'moving_expenses']

    #timeout_seconds = Constants.calculator_time * 60
    #timer_text = "Time left to come up with an initial offer"

    def is_displayed(self):
        return True

    def before_next_page(self):
        if self.timeout_happened:
            self.player.initial_offer_points=0
            self.player.bonus=10
            self.player.job_assignment="Division A"
            self.player.location = "San Francisco"
            self.player.insurance_coverage = "Plan A"
            self.player.vacation_time = 25
            self.player.moving_expenses = 100
            self.player.salary = 90000
            self.player.starting_date = "June 1"

        id = 1
        #self.player.initial_offer_points = Constants.salary[self.player.salary][id]+\
        #                        Constants.bonus[self.player.bonus][id]+\
        #                        Constants.location[self.player.location][id]+\
        #                        Constants.insurance_coverage[self.player.insurance_coverage][id]+\
        #                        Constants.vacation_time[self.player.vacation_time][id]+\
        #                        Constants.moving_expenses[self.player.moving_expenses][id]+\
        #                        Constants.job_assignment[self.player.job_assignment][id]+\
        #                        Constants.starting_date[self.player.starting_date][id]"""

class Recruiter_calculator(Page):
    form_model = "player"
    form_fields = ['bonus',
                            'job_assignment',
                            'location',
                            'insurance_coverage',
                            'vacation_time',
                            'moving_expenses']

    #timeout_seconds = Constants.calculator_time * 60
    #timer_text = "Time left to come up with an initial offer"

    def is_displayed(self):
        return True

    def before_next_page(self):
        if self.timeout_happened:
            self.player.initial_offer_points=0
            self.player.bonus=10
            self.player.job_assignment="Division A"
            self.player.location = "San Francisco"
            self.player.insurance_coverage = "Plan A"
            self.player.vacation_time = 25
            self.player.moving_expenses = 100
            self.player.salary = 90000
            self.player.starting_date = "June 1"
        id = 0
        self.player.initial_offer_points = Constants.salary[self.player.salary][id]+\
                                Constants.bonus[self.player.bonus][id]+\
                                Constants.location[self.player.location][id]+\
                                Constants.insurance_coverage[self.player.insurance_coverage][id]+\
                                Constants.vacation_time[self.player.vacation_time][id]+\
                                Constants.moving_expenses[self.player.moving_expenses][id]+\
                                Constants.job_assignment[self.player.job_assignment][id]+\
                                Constants.starting_date[self.player.starting_date][id]


class Planning_doc(Page):
    form_model = "player"
    form_fields = ["planning_text"]

    #timeout_seconds = Constants.planning_doc_time *60
    #timer_text = "Time left to finish the planning document"


    def vars_for_template(self):
        if self.player.candidate:
            return {"pdf_file": "NewRecruit/Candidate.pdf"}
        else:
            return {"pdf_file": "NewRecruit/Recruiter.pdf"}

class Candidate_submission(Page):
    form_model = "player"
    form_fields = ['bonus',
                            'job_assignment',
                            'location',
                            'insurance_coverage',
                            'vacation_time',
                            'moving_expenses']



class Wait_for_class(Page):
    form_model = "player"





page_sequence = [Introduction, Candidate_calculator, Candidate_submission]
