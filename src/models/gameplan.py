class Gameplan(object):
    def __init__(self, d_run, o_run):
        self.d_style = "43"
        self.d_run = d_run
        self.d_pass = 100 - d_run
        self.d_aggression = 50
        self.o_run = o_run
        self.o_pass = 100 - o_run
        self.o_rb1 = 75
        self.o_rb2 = 25
        self.o_aggression = 50
        self.fg_try = 35
