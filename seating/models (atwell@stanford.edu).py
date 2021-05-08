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

removals = ["atwell","apaza","extra_01","extra_02","extra_03","extra_04","extra_05","extra_06"]
with open("_rooms/Sp21_01.txt", "r") as f:
    raw_string = f.read().strip()
    names_section1 = raw_string.split("\n")
    for name in removals:
        names_section1.remove(name)
    print("{} names in section 1".format(len(names_section1)))

with open("_rooms/Sp21_02.txt", "r") as f:
    raw_string = f.read().strip()
    names_section2 = raw_string.split("\n")
    for name in removals:
        names_section2.remove(name)
    print("{} names in section 2".format(len(names_section2)))

with open("_rooms/Sp21_03.txt", "r") as f:
    raw_string = f.read().strip()
    names_section3 = raw_string.split("\n")
    for name in removals:
        names_section3.remove(name)
    print("{} names in section 3".format(len(names_section3)))


class Constants(BaseConstants):
    name_in_url = 'seating'
    players_per_group = None
    num_rounds = 1
    names_section1 = names_section1
    names_section2 = names_section2
    names_section3 = names_section3
    eligible = None
    ineligible = None

class Subsession(BaseSubsession):
    def creating_session(self):
        start_index = self.session.config["start_index"]

        if self.session.config["section_number"] == 1:
            section_participants = names_section1
        elif self.session.config["section_number"] == 2:
            section_participants = names_section2
        else:
            section_participants = names_section3

        eligible = section_participants[start_index:start_index+self.session.config["section_seats"]]
        self.session.vars["eligible"] = eligible
        remainder = 23 - len(eligible)
        if remainder >0:
            eligible.extend(section_participants[:remainder])

        ineligible = list(set(section_participants).difference(set(eligible)))
        self.session.vars["ineligible"] = ineligible
        print("eligible", eligible)
        print("ineligible", ineligible)




class Group(BaseGroup):
    pass


class Player(BasePlayer):

    claim_it = models.BooleanField(label="Would you like to claim it?")
    waiting = models.BooleanField(label="You do not have first priority today. Would you like to add yourself to the waitlist?")
