class Gameplan(object):
    def __init__(self, d_run, d_pass):
        self.d_style = "43"
        self.d_run = 50
        self.d_pass = 100 - d_run
        self.d_aggression = 50
        self.o_run = 50
        self.o_pass = 100 - d_pass
        self.o_rb1 = 75
        self.o_rb2 = 25
        self.o_aggression = 50
        self.fg_try = 35
