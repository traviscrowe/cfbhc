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
        self.type = get_type_by_position(throw_power, throw_accuracy, speed, break_tackle, catching,
                                      agility, run_blocking, pass_blocking, acceleration, pass_rush,
                                      run_defense,
                                      coverage, tackling, kick_power, kick_accuracy, concentration, position,
                                      dc_position, depth)


def get_overall_by_position(throw_power, throw_accuracy, speed, break_tackle, catching,
                            agility, run_blocking, pass_blocking, acceleration, pass_rush, run_defense,
                            coverage, tackle, kick_power, kick_accuracy, concentration, position, dc_position, depth):
    if position is 'QB':
        return qb_overall(throw_power, throw_accuracy, speed, concentration)
    if position is 'RB':
        return rb_overall(speed, break_tackle, catching, agility, concentration)
    if position is 'FB':
        return fb_overall(speed, break_tackle, catching, run_blocking, concentration)
    if position is 'TE':
        return te_overall(speed, catching, run_blocking, concentration)
    if position is 'WR':
        return wr_overall(speed, catching, acceleration, concentration)
    if position is 'OT' or position is 'C' or position is 'OG':
        return ol_overall(run_blocking, pass_blocking)
    # if position is 'DE' or position is 'DT': return dl_overall(pass_rush, run_defense)
    # if position is 'OLB' or position is 'ILB': return lb_overall(pass_rush, tackling, coverage)
    # if position is 'CB': return cb_overall(catching, coverage, tackle)
    # if position is 'SS' or position is 'FS': return s_overall(catching, coverage, tackle)
    # if position is 'K' or 'P': return st_overall(kick_power, kick_accuracy)


def get_type_by_position(throw_power, throw_accuracy, speed, break_tackle, catching,
                                      agility, run_blocking, pass_blocking, acceleration, pass_rush,
                                      run_defense,
                                      coverage, tackling, kick_power, kick_accuracy, concentration, position,
                                      dc_position, depth):
    if position is 'QB':
        return qb_type(throw_power, throw_accuracy, speed)
    if position is 'RB':
        return rb_type(speed, break_tackle, agility)
    if position is 'FB':
        return fb_type(catching, run_blocking)
    if position is 'TE':
        return te_type(catching, run_blocking)
    if position is 'WR':
        return wr_type(speed, catching)
    if position is 'OT' or position is 'C' or position is 'OG':
        return ol_type(run_blocking, pass_blocking)
    if position is 'DE' or position is 'DT':
        return dl_type(pass_rush, run_defense)
    if position is 'OLB' or position is 'ILB':
        return lb_type(pass_rush, tackling, coverage)
    if position is 'CB' or position is 'SS' or position is 'FS':
        return cb_s_type(catching, coverage, tackling)
    if position is 'K' or 'P':
        return st_type(kick_power, kick_accuracy)


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


def qb_type(throw_power, throw_accuracy, speed):
    if speed >= 90 or throw_accuracy >= 90 or throw_power >= 90:
        if (speed > throw_power and speed > throw_accuracy) or speed > 95:
            return 'Scrambler'
        if throw_power > speed and throw_power > throw_accuracy:
            return 'Pocket'
        if throw_accuracy > speed and throw_accuracy > throw_power:
            return 'Field General'
    return 'Balanced'


def rb_type(speed, break_tackle, agility):
    if speed >= 85 or break_tackle >= 85 or agility >= 85:
        if speed > break_tackle and speed > agility:
            return 'Speed'
        if break_tackle > speed and break_tackle > agility:
            return 'Power'
        if agility > speed and agility > break_tackle:
            return 'One Cut'
    return 'Balanced'


def fb_type(catching, run_blocking):
    if catching >= 85 or run_blocking >= 85:
        return 'Receiving' if catching > run_blocking else 'Blocker'
    return 'Balanced'


def te_type(catching, run_blocking):
    if catching >= 85 or run_blocking >= 85:
        return 'Receiving' if catching > run_blocking else 'Blocker'
    return 'Balanced'
    
    
def wr_type(speed, catching):
    if speed >= 85 or catching >= 85:
        return 'Possession' if catching > speed else 'Speed'
    return 'Balanced'


def ol_type(run_blocking, pass_blocking):
    if run_blocking >= 85 or pass_blocking >= 85:
        return 'Run Blocker' if run_blocking > pass_blocking else 'Pass Blocker'
    return 'Balanced'


def dl_type(run_defense, pass_rush):
    if run_defense >= 85 and pass_rush >= 85:
        return 'Run Stopper' if run_defense > pass_rush else 'Pass Rusher'
    return 'Balanced'


def lb_type(pass_rush, tackle, coverage):
    if pass_rush >= 85 and tackle >= 85 and coverage >= 85:
        if pass_rush > tackle and pass_rush > coverage:
            return 'Pass Rusher'
        if tackle > pass_rush and  tackle > coverage:
            return 'Run Stopper'
        if coverage > tackle and coverage > pass_rush:
            return 'Coverage'
    return 'Balanced'


def cb_s_type(catching, coverage, tackling):
    if catching >= 85 and coverage >= 85 and tackling >= 85:
        if catching > coverage and catching > tackling:
            return 'Playmaker'
        if coverage > catching and coverage > tackling:
            return 'Coverage'
        if tackling > coverage and tackling > catching:
            return "Hard Hitter"


def st_type(kick_power, kick_accuracy):
    if kick_power >= 85 and kick_accuracy >= 85:
        return 'Power' if kick_power > kick_accuracy else 'Accuracy'
    return 'Balanced'
