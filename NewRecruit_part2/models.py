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
Negotatiing New Recruit with a partner
"""

locations_1 = ["Campus Dr Grove 1","Campus Dr Grove 2","Campus Dr Grove 3","Campus Dr Lawn 1","Campus Dr Lawn 2","Campus Dr Lawn 3","Community Court 1","Community Court 2","Community Court 3","Community Court 4","Community Court 5","GSB Bowl 1","GSB Bowl 2","GSB Bowl 3","Knight Way 1"]
locations_2 = ["Campus Dr Grove 1","Campus Dr Grove 2","Campus Dr Grove 3","Campus Dr Lawn 1","Campus Dr Lawn 2","Campus Dr Lawn 3","Community Court 1","Community Court 2","Community Court 3","Community Court 4","Community Court 5","GSB Bowl 1","GSB Bowl 2","GSB Bowl 3","Knight Way 1","Knight Way 2","Knight Way 3"]
locations_3 = ["Campus Dr Grove 1 ","Campus Dr Grove 2","Campus Dr Grove 3","Campus Dr Lawn 1","Campus Dr Lawn 2","Campus Dr Lawn 3","Community Court 1","Community Court 2","Community Court 3","Community Court 4","Community Court 5","Knight Way 1","Knight Way 2","Knight Way 3","Knight Way 4","Town Square 1","Town Square 3","GSB Bowl 1","GSB Bowl 2","GSB Bowl 3"]

class Constants(BaseConstants):
    name_in_url = 'New_Recruit_part2'
    players_per_group = 2
    num_rounds = 1

    negotiating_time = 25 # minutes

    planning_doc_length = 100 #words

    salary = { 90000:(-6000,0), 88000:(-4500,-1500), 86000:(-3000,-3000), 84000:(-1500,-4500), 82000:(0,-6000)}
    bonus = { 10:(0,4000), 8:(400,3000), 6:(800,2000), 4:(1200,1000), 2:(1600,0)}
    vacation_time = { 25:(0,1600), 20:(1000,1200), 15:(2000,800), 10:(3000,400), 5:(4000,0)}
    moving_expenses = {100:(0,3200), 90:(200,2400), 80:(400,1600), 70:(600,800), 60:(800,0)}
    location = {"San Francisco":(1200,1200), "Atlanta":(900,900), "Chicago":(600,600),"Boston":(300,300),  "New York":(0,0)}
    insurance_coverage = {"Plan A":(0,800), "Plan B":(800,600), "Plan C":(1600,400), "Plan D":(2400,200), "Plan E":(3200,0)}
    starting_date = {"June 1":(0,2400), "June 15":(600,1800),"July 1":(1200,1200), "July 15":(1800,600), "August 1":(2400,0)}
    job_assignment = {"Division A":(0,0), "Division B":(-600,-600), "Division C":(-1200,-1200), "Division D":(-1800,-1800), "Division E":(-2400,-2400)}


class Subsession(BaseSubsession):

    def set_groups(self):

        if self.session.config["section_number"] == 1:
            locations = locations_1
        elif self.session.config["section_number"] == 2:
            locations = locations_2
        elif self.session.config["section_number"] == 3:
            locations = locations_3
  
        inperson_candidates = []
        inperson_recruiters = []
        zoom_candidates = []
        zoom_recruiters = []
        extra_z = None
        extra_ip = None

        for p in self.get_players():
            if p.participant.vars['inperson']:
                if p.participant.vars["role"] == "candidate":
                    inperson_candidates.append(p)
                else:
                    inperson_recruiters.append(p)
            else:
                if p.participant.vars["role"] == "candidate":
                    zoom_candidates.append(p)
                else:
                    zoom_recruiters.append(p)

        print("LISTS\n\n")
        print(inperson_candidates)
        print(inperson_recruiters)
        print(zoom_candidates)
        print(zoom_recruiters)

        if len(inperson_candidates)  == len(inperson_recruiters) +1:
            extra_ip = inperson_candidates.pop()
        elif len(inperson_candidates)  == len(inperson_recruiters) +1:
            extra_ip = inperson_recruiters.pop()
        inperson_pairs = list(zip(inperson_candidates, inperson_recruiters))

        if len(zoom_candidates) > len(zoom_recruiters) and extra_ip != None:
            extra_z = zoom_candidates.pop(len(zoom_recruiters))
        elif len(zoom_candidates) < len(zoom_recruiters)  and extra_ip != None:
            extra_z = zoom_recruiters.pop(len(zoom_candidates))

        dummies = zoom_recruiters[len(zoom_candidates):]
        zoom_pairs = list(zip(zoom_candidates, zoom_recruiters))

        if extra_z != None and extra_ip != None:
            zoom_pairs.append((extra_z,extra_ip))

        if dummies != []:
            half = int(len(dummies)/2)
            zoom_pairs.extend(list(zip(dummies[:half],dummies[half:])))

        for one, two in inperson_pairs:
            one.partner = two.participant.vars["name"]
            two.partner = one.participant.vars["name"]
            if locations != []:
                loc = locations.pop(0)
                one.meeting_inperson = True
                two.meeting_inperson = True
            else:
                loc = "Zoom breakout"
                one.zoom_group = "{} and {} ({}-{})".format(two.partner,one.partner,one.participant.label, two.participant.label)
            one.location = loc
            two.location = loc
            for p in (one,two):
                print(p.participant.vars["name"], p.participant.label, p.location, p.participant.vars["inperson"], p.partner)
        
        for one, two in zoom_pairs:
            loc = "Zoom breakout"
            one.location = loc
            two.location = loc
            one.partner = two.participant.vars["name"]
            two.partner = one.participant.vars["name"]
            one.zoom_group = "{} and {} ({}-{})".format(two.partner,one.partner,one.participant.label, two.participant.label)
            for p in (one,two):
                print(p.participant.vars["name"], p.participant.label, p.location, p.participant.vars["inperson"], p.partner)
        
        all_pairs = inperson_pairs + zoom_pairs

        self.set_group_matrix(all_pairs)

    def vars_for_admin_report(self):
        zoomies = []
        for player in self.get_players():
            if player.zoom_group != None:
                zoomies.append(player.zoom_group)
        return dict(zoom_groups=",\n".join(zoomies))




class Group(BaseGroup):
    salary = models.IntegerField()
    bonus = models.IntegerField()
    moving_expenses = models.IntegerField()
    vacation_time = models.IntegerField()
    job_assignment = models.StringField()
    location = models.StringField()
    insurance_coverage = models.StringField()
    starting_date = models.StringField()


    def set_timer(self):
        start_time = time.time()
        for player in self.get_players():
            player.participant.vars["sim_timer"] = start_time + Constants.negotiating_time * 60 + 30


class Player(BasePlayer):
    candidate = models.BooleanField()
    location = models.StringField(label="Negotiation location")
    meeting_inperson = models.BooleanField(default=False)
    partner = models.StringField()
    zoom_group = models.StringField()

    salary = models.IntegerField()
    bonus = models.IntegerField()
    moving_expenses = models.IntegerField()
    vacation_time = models.IntegerField()
    job_assignment = models.StringField()
    location = models.StringField()
    insurance_coverage = models.StringField()
    starting_date = models.StringField()

    planning_text = models.LongStringField(label="Describe your plan for this negotiation")
    journaling_text = models.LongStringField(label="Please describe your experience of the negotiation.")
    initial_offer_points = models.IntegerField()
    final_points = models.IntegerField()

    salary_fract = models.FloatField()
    bonus_fract = models.FloatField()
    job_assignment_fract = models.FloatField()
    location_fract =models.FloatField()
    insurance_coverage_fract = models.FloatField()
    vacation_time_fract = models.FloatField()
    starting_date_fract = models.FloatField()
    moving_expenses_fract = models.FloatField()
