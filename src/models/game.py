

class Game(object):
    def __init__(self, offense, defense, stadium, weather):
        self.offense = offense
        self.defense = defense
        self.stadium = None
        self.weather = None
        self.time = 3600
        self.quarter = 1
        self.down = 1
        self.to_go = 10
        self.yard_line = 35
        self.run_mod = 0.0
        self.pass_mod = 0.0
