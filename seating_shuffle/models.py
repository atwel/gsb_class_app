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
    name_in_url = 'seating_shuffle'
    players_per_group = None
    num_rounds = 1
    names_section1 = names_section1
    names_section2 = names_section2
    names_section3 = names_section3


class Subsession(BaseSubsession):
    have_seat = models.StringField(default="None yet")
    no_seat = models.StringField(default="Also none yet")

    def vars_for_admin_report(self):
        return dict(have_seat=self.have_seat,no_seat=self.no_seat)

    def before_session_starts(self):
        self.session.vars["have_seat"] = "None yet"
        self.session.vars["no_seat"] = "None yet"
        start_index = self.session.config["start_index"]
        if self.session.config["section_number"] == 1:
            section_participants = names_section1
        elif self.session.config["section_number"] == 2:
            section_participants = names_section2
        else:
            section_participants = names_section3

        for player, label in zip(self.get_players(), section_participants):
            player.participant.label = label

        eligible = section_participants[start_index:start_index+self.session.config["section_seats"]]
        remainder = self.session.config["section_seats"] - len(eligible)
        if remainder >0:
            eligible.extend(section_participants[:remainder])

        ineligible = list(set(section_participants).difference(set(eligible)))
        print("eligible", eligible)
        print("ineligible", ineligible)
        self.session.vars["eligible"] = eligible
        self.session.vars["ineligible"] = ineligible

        for player in self.get_players():
            if player.participant.label in eligible:
                player.participant.vars["eligible"] = True
            else:
                player.participant.vars["eligible"] = False

class Group(BaseGroup):
    pass


class Player(BasePlayer):

    claim_it = models.BooleanField(label="Would you like to claim it?")
    waiting = models.BooleanField(label="Would you like to add yourself to the waitlist?")
    declined  = models.BooleanField(default=False)
