from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

SUNet_to_name = {"oakkurt":"Ozlem Akkurt","sarahand":"Sarah Anderson","sankalpb":"Sankalp Banerjee","abertha":"Andrew Bertha","jhbuchel":"Jason Buchel","daviscm":"Carolyn Davis","mdicou":"Matt Dicou","dhfranks":"David Franks","jigs":"Jose Garcia Suarez","kgea":"Kathy Gea","ehuscher":"Elspeth Huscher","yvj":"Yash Jain","mlamdan":"Matan Lamdan","cdlince":"Carly Lincenberg","asmartin":"Anne-Sophie Martin","kmodukan":"Kesaobaka Modukanele","povalleb":"Pablo Ovalle","spatarca":"Santiago Patarca","leilap":"Leila Pirbay","kpolle":"Karen Polle","pretes":"Paola Petes Pineda","drichey":"Dan Rickey","wrodrig":"Wes Rodriguez","jrowley":"Josh Rowley","nishaad":"Nishaad Ruparel","juansaez":"Juan Saez Vera","talsarig":"Tal Sarig","nschlein":"Nate Schlein","mariasw":"Maria Silva Willson","kstein10":"Kate Steinman","tstone":"Thomas Stone","ianas":"Iana Stoytcheva","tejsun":"Tejas Sundaresan","mtakasak":"Midori Takasaki","stopper":"Sydni Topper","tjwater":"Tanner Waterstreet","eview":"Evie Woodforde","mzxie":"Michelle Xie","cqyuan":"Chris Yuan","edzhai":"Ethan Zhai","jrbz":"Justin Ziegler","taftab":"Taleha Aftab","oyinda":"Oyinda Ajayi","hajmani":"Hannah Ajmani","hrma":"Henrique Albuquerque","lallende":"Luife Allende","dalpuche":"Dominique Alpuche","annesan":"Annes An","casawa":"Chaitanya Asawa","sherb":"Sher Bhullar","jsburns":"James Burn","cc16":"Charlotte Camacho","ecambern":"Emily Cambern","iw1000":"Lucas Cheon","hamzac":"Hamza Choudery","ncole2":"Nyamekye Coleman","pcout":"Peter Coutoulas","adavis29":"Alexa Davis","sef07":"Steven Ferreira","wglick":"Whitney Glick","anna425":"Anna Gurevich","royhage":"Roy Hage","davidh7":"David Harrison","rbhuang":"Richard Huang","jh21":"Jonathan Hurowitz","andyjin":"Andy Jin","mjuzwiak":"Monika Juzwiak","hkling":"Henry Klingenstein","macklee":"Mackenzie Lee","levinelu":"Lucas Levine","natm":"Natalie Meurer","cliffmil":"Cliff Miller","jmorton4":"Jackson Morton","karlyosb":"Karly Osborne","playfair":"Katherine Playfair","yploder":"Yvonne Ploder","eportura":"Eliann Porturas","psaength":"Phanthila Saengthong","jsayadi":"Jamasb Sayadi","jeremycs":"Jeremy Scott","sheldon3":"Casey Sheldon","amys2023":"Amy Marie Slaughter","nsuchato":"Prao Suchato","m2taylor":"Margot Taylor","wilkinsj":"Jonathan Wilkins","kwolsten":"Kyle Wolstencroft","mzincone":"Michael Zincone","anibaldf":"Anibal de Frankenberg","tracycao":"Tracy Cao","amanc2":"Aman Chaudhary","crozelcm":"Claire Crozel","vdivi":"Vasu Divi","fadavi":"Faraz Fadavi","jhamying":"Julien Ham-Ying","shasson":"Sophie Hasson","srkarr":"S Karr","nkasper":"Nolan Kasper","bkhoo":"Bryan Khoo","akiam":"Alex Kiam","albertwj":"Albert Lee","diane8":"Diane Lee","jackylin":"Jacky Lin","samzliu":"Samuel Liu","sliu2022":"Stella Liu","jmunoz8":"Jaime Munoz Jr.","misatonk":"Misato Nakayama","lneise":"Luke Neise","sanvar":"Sanvar Oberoi","sraches":"Steven Rachesky","ramayya":"Sulekha Pamayya","lukeren":"Luke Ren","ninasab":"Nina Sabharwal","kshah1":"Kevin Shah","fsa":"Frances Simpson-Allen","dss93":"David Steiner","sunilrao":"Sunil Sudhakaran","yalew":"Yale Wang","cjmeerst":"Charlotte Meerstadt","atwell":"Prof. Atwell","clide":"Chelsea Lide (CA)","lizixin":"Lambert Li (CA)","extra_01":"Unnamed #1","extra_02":"Unnamed #2","extra_03":"Unnamed #3","extra_04":"Unnamed #4","extra_05":"Unnamed #5","extra_06":"Unnamed #6"}


class IntroWaitPage(WaitPage):
    group_by_arrival_time = True

    def vars_for_template(self):
        return {"title_text": "Waiting for others", "body_text":"Please wait a moment while you're assigned to a group.\n\n"}


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


class Stockman(Page):
    form_model = "player"

    timeout_seconds = Constants.reading_time*60
    timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.role() == "stockman"

    def vars_for_template(self):
        return {"pdf_file": "Federated/Stockman.pdf","End_time":"","show_end_time":False}

    def js_vars(self):
        return dict(button_show=Constants.material_button_show*60000)


class Stockman_nt(Page):
    form_model = "player"

    template_name = "Federated/Stockman.html"


    def is_displayed(self):
        return self.player.role() == "stockman"

    def vars_for_template(self):
        return {"pdf_file": "Federated/Stockman.pdf","End_time":self.group.end_time,"show_end_time":True}

    def js_vars(self):
        return dict(button_show=Constants.material_button_show*60000)


class Turbo(Page):
    form_model = "player"

    timeout_seconds = Constants.reading_time*60
    timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.role() == "turbo"

    def vars_for_template(self):
        return {"pdf_file": "Federated/Turbo.pdf","End_time":"","show_end_time":False}

    def js_vars(self):
        return dict(button_show=Constants.material_button_show*60000)


class Turbo_nt(Page):
    form_model = "player"

    template_name = "Federated/Turbo.html"

    def is_displayed(self):
        return self.player.role() == "turbo"

    def vars_for_template(self):
        return {"pdf_file": "Federated/Turbo.pdf","End_time":self.group.end_time,"show_end_time":True}

    def js_vars(self):
        return dict(button_show=Constants.material_button_show*60000)


class United(Page):
    form_model = "player"

    timeout_seconds = Constants.reading_time*60
    timer_text = 'Time left for reading the materials'

    def is_displayed(self):
        return self.player.role() == "united"

    def vars_for_template(self):
        return {"pdf_file": "Federated/United.pdf","End_time":"","show_end_time":False}

    def js_vars(self):
        return dict(button_show=Constants.material_button_show*60000)


class United_nt(Page):
    form_model = "player"

    template_name = "Federated/United.html"

    def is_displayed(self):
        return self.player.role() == "united"

    def vars_for_template(self):
        return {"pdf_file": "Federated/United.pdf","End_time":self.group.end_time,"show_end_time":True}

    def js_vars(self):
        return dict(button_show=Constants.material_button_show*60000)



class Planning_doc(Page):
    form_model = "player"
    form_fields = ["planning_text"]

    timeout_seconds = Constants.planning_doc_time *60
    timer_text = "Time left to finish the planning document"

    def vars_for_template(self):
        if self.player.role() == "stockman":
            return {"pdf_file": "Federated/Stockman.pdf"}
        elif self.player.role() == "turbo":
            return {"pdf_file": "Federated/Turbo.pdf"}
        elif self.player.role() == "united":
            return {"pdf_file": "Federated/United.pdf"}


class Ready_for_class(Page):
    form_model = "player"

class Wait_to_negotiate(WaitPage):
    form_model = "group"

    def vars_for_template(self):
        return {"title_text": "Waiting for your counterparts to finish preparing", "body_text":"It shouldn't be too long now!\n\n"}


class Back_to_class(Page):
    form_model = "player"

    def before_next_page(self):
        if self.group.end_time == None:
            self.group.set_end_time()

    def vars_for_template(self):
        partners = self.player.get_others_in_group()
        part_1 = partners[0].name
        part_2 = partners[1].name

        if self.group.stockman:
            if self.player.role() == "united":
                return {"rep": "United", "alter":"Stockman", "in_first":True, "partner_1":part_1, "partner_2":part_2}
            elif self.player.role() == "stockman":
                return {"alter": "United", "rep":"Stockman", "in_first":True, "partner_1":part_1, "partner_2":part_2}
            else:
                return {"rep": "Turbo", "alter":"NA", "in_first":False, "partner_1":part_1, "partner_2":part_2}
        else:
            if self.player.role() == "united":
                return {"rep": "United", "alter":"Turbo", "in_first":True, "partner_1":part_1, "partner_2":part_2}
            elif self.player.role() == "turbo":
                return {"alter": "United", "rep":"Turbo", "in_first":True, "partner_1":part_1, "partner_2":part_2}
            else:
                return {"rep": "Stockman", "alter":"NA", "in_first":False, "partner_1":part_1, "partner_2":part_2}



class Outcome(Page):
    form_model = "player"

    form_fields = ["united","stockman","turbo","first_meeting"]



class Journaling_page(Page):
    form_model = "player"

    form_fields = ["journaling_text"]

    #timeout_seconds = Constants.reflection_time*60


class Outro(Page):
    form_model = "group"


page_sequence = [Introduction, Stockman, Turbo, United, Planning_doc, Ready_for_class, Wait_to_negotiate, Back_to_class, Stockman_nt, Turbo_nt, United_nt, Outcome, Journaling_page, Outro]
