

class Game(object):
    def __init__(self, home, away, stadium, weather, stats):
        self.home = home
        self.away = away
        self.stadium = None
        self.weather = None
        self.kicking_team = None
        self.offense = None
        self.defense = None
        self.last_time = 3600
        self.time = 3600
        self.quarter = 1
        self.minutes = 15
        self.seconds = 0
        self.down = 1
        self.to_go = 10
        self.yard_line = 35
        self.overtime = False
        self.play_mod = 0.0
        self.run_mod = 0.0
        self.pass_mod = 0.0
        self.kick_mod = 0.0
        self.stats = stats
        self.log = []
