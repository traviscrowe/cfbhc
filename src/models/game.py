

class Game(object):
    def __init__(self, home_team, stadium, weather):
        self.home_team = home_team
        self.away_team = away_team
        self.stadium = stadium
        self.weather = weather
        self.time = 3600
        self.quarter = 1
        self.down = 1
        self.to_go = 10
