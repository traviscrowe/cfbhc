class Player(object):
    def __init__(self, name, throw_power, throw_accuracy, speed, break_tackle, catching,
               agility, run_blocking, pass_blocking, acceleration, pass_rush, run_defense,
               coverage, tackling, kick_power, kick_accuracy, concentration, position, dc_position, depth):
        self.name = name
        self.throw_power = throw_power
        self.throw_accuracy = throw_accuracy
        self.speed = speed
        self.break_tackle = break_tackle
        self.catching = catching
        self.agility = agility
        self.run_blocking = run_blocking
        self.pass_blocking = pass_blocking
        self.acceleration = acceleration
        self.pass_rush = pass_rush
        self.run_defense = run_defense
        self.coverage = coverage
        self.tackling = tackling
        self.kick_power = kick_power
        self.kick_accuracy = kick_accuracy
        self.concentration = concentration
        self.position = position
        self.dc_position = dc_position
        self.depth = depth
        self.overall = get_overall_by_position(throw_power, throw_accuracy, speed, break_tackle, catching,
                                               agility, run_blocking, pass_blocking, acceleration, pass_rush,
                                               run_defense,
                                               coverage, tackling, kick_power, kick_accuracy, concentration, position,
                                               dc_position, depth)


def get_overall_by_position(throw_power, throw_accuracy, speed, break_tackle, catching,
                            agility, run_blocking, pass_blocking, acceleration, pass_rush, run_defense,
                            coverage, tackle, kick_power, kick_accuracy, concentration, position, dc_position, depth):
    if position is "QB":
        return qb_overall(throw_power, throw_accuracy, speed, concentration)
    if position is "RB":
        return rb_overall(speed, break_tackle, catching, agility, concentration)
    if position is "FB":
        return fb_overall(speed, break_tackle, catching, run_blocking, concentration)
    if position is "TE":
        return te_overall(speed, catching, run_blocking, concentration)
    if position is "WR":
        return wr_overall(speed, catching, acceleration, concentration)
    if position is "OT" or position is "C" or position is "OG":
        return ol_overall(run_blocking, pass_blocking)
    # if position is "DE" or position is "DT": return dl_overall(pass_rush, run_defense)
    # if position is "OLB" or position is "ILB": return lb_overall(pass_rush, tackling, coverage)
    # if position is "CB": return cb_overall(catching, coverage, tackle)
    # if position is "SS" or position is "FS": return s_overall(catching, coverage, tackle)
    # if position is "K" or "P": return st_overall(kick_power, kick_accuracy)


def qb_overall(throw_power, throw_accuracy, speed, concentration):
    overall = (throw_power * 0.4) + (throw_accuracy * 0.4) + (concentration * 0.15) + (speed * 0.05)
    return overall


def rb_overall(speed, break_tackle, catching, agility, concentration):
    overall = (speed * 0.2) + (break_tackle * 0.3) + (agility * 0.3) + (catching * 0.1) + (concentration * 0.1)
    return overall


def fb_overall(speed, break_tackle, catching, run_blocking, concentration):
    overall = (speed * 0.2) + (break_tackle * 0.3) + (catching * 0.05) + (run_blocking * 0.35) + (concentration * 0.1)
    return overall


def te_overall(speed, catching, run_blocking, concentration):
    overall = (speed * 0.2) + (catching * 0.35) + (run_blocking * 0.35) + (concentration * 0.1)
    return overall


def ol_overall(run_blocking, pass_blocking):
    overall = (run_blocking * 0.5) + (pass_blocking * 0.5)
    return overall


def wr_overall(speed, catching, acceleration, concentration):
    overall = (speed * 0.25) + (catching * 0.35) + (acceleration * 0.3) + (concentration * 0.1)
    return overall
