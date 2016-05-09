"""
Execution logic for special teams plays
"""
from engine.determinations import determine_play, determine_onside_kick
from engine.clock import spend_time
from services.rng import random_in_range, random_variability, random_weighted_choice, random_chance

def execute_fourth_down(game):
    """
    Executes a fourth down play, returns game state via a specific execution
    """
    desperation_time = 160 + (game.offense.gameplan.o_aggression / 2)

    if ((game.offense.score < game.defense.score)
            and (game.time <= 900)
            and (game.time <= (desperation_time * ((game.defense.score - game.offense.score) / 8) + 1))):
        if ((game.offense.score) + 3 >= game.defense.score
                or game.time > (desperation_time (game.defense.score - game.offense.score - 3) / 9)):
            if game.yard_line <= game.offense.gameplan.fg_try:
                return execute_field_goal(game)
        return determine_play(game)
    else:
        to_go_mod = game.yard_line
        go_chance = ((100 - game.offense.gameplan.o_aggression)
                     + (4 * (game.yard_line - 40))
                     + (to_go_mod * (game.to_go - 1)))

        if game.yard_line <= game.offense.gameplan.fg_try:
            return execute_field_goal(game)
        elif (game.yard_line <= 55
              and random_in_range(-1, go_chance) <= 10
              and go_chance <= 500
              and game.to_go <= 6):
            return determine_play(game)
        else:
            return execute_punt(game)

def execute_turnover(game):
    """
    Executes a turnover against the game state
    """
    tmp = game.offense
    game.offense = game.defense
    game.defense = tmp

    game.yard_line = 100 - game.yard_line
    game.to_go = 10
    if game.to_go > game.yard_line:
        game.to_go = game.yard_line
    game.down = 1

    return game


def execute_punt(game):
    """
    Executes a punt play
    """
    punter = game.offense.get_player('P', 1)
    returner = game.defense.get_player('KR', 1)
    punt_mod = random_in_range(-7, 7)
    max_punt = 15.0 + (45.0 * (punter.kick_power) / 100.0) + game.kick_mod + random_variability()
    min_punt = 10.0 + (35.0 * (punter.kick_power) / 100.0) + game.kick_mod + random_variability()

    #TODO implement st_mod (based on special teams blocking/coverage)
    punt = random_in_range(min_punt + punt_mod, max_punt + punt_mod) + 1

    #TODO implement great_blocking based on special teams blocking/coverage
    return_mod = random_in_range(-5, 5)

    choices = [
        (1, punter.kick_accuracy),
        (2, punter.kick_accuracy + 50 + punt_mod),
        (3, 200)
    ]
    punt_type = random_weighted_choice(choices)

    if punt >= game.yard_line - 5:
        punt_type = 1

    if punt >= game.yard_line + 5:
        punt = game.yard_line + 5

    touchback = False
    touchdown = False
    returns = 0
    net_punt = punt
    original_int = game.yard_line

    if punt_type == 1:
        game.yard_line = game.yard_line - punt
    elif punt_type == 2:
        punt = punt - random_in_range(5, 15)
        net_punt = punt
        game.yard_line = game.yard_line - punt
    else:
        return_stat = returner.agility if returner.agility > returner.concentration else returner.concentration
        min_return = 0.1 * return_stat + random_variability() + return_mod
        max_return = 0.25 * returner.speed + random_variability() + return_mod

        returns = random_in_range(min_return + return_mod, max_return + return_mod)

        #TODO if great_blocking (ln 4924)

        yl_togo = 100 - (game.yard_line - punt)
        game.yard_line = game.yard_line - punt + returns

        if game.yard_line > 99:
            touchdown = True
            returns = yl_togo
            game.yard_line = 100

    if game.yard_line < 1:
        game.yard_line = 20
        touchback = True
        net_punt = original_int - 20

    in_20 = False
    if game.yard_line < 20:
        in_20 = True

    if touchdown:
        game. defense.score += 6
        game = spend_time(10, 15, 10, False)
        game = execute_turnover(game)
        if (game.last_time < 1800
                and game.time >= 1800
                and (game.overtime is False
                     or game.offense.score == game.defense.score)):
            game = execute_kickoff(game)
    else:
        if punt_type == 3:
            game = spend_time(5, 15, 5, False)
        else:
            game = spend_time(3, 8, 3, False)
        game = execute_turnover(game)

    #TODO log play results with returns, touchdown, offense

    return game


def execute_field_goal(game):
    """
    Executes a field goal play
    """
    chance_mod = random_in_range(-10, 10)
    chance = ((100
               * (game.offense.get_player('K', 1).kick_accuracy) / 100.0)
              + (60 * (game.offense.get_player('K', 1).kick_power) / 100.0)
              - (2.5 * game.yard_line)
              + (3 * chance_mod)
              + game.kick_mod
              + random_variability())

    if chance > 100:
        chance = 100

    if chance < 1 and random_chance(1):
        chance = 1

    if random_chance(chance):
        game.offense.score += 3

    game = spend_time(3, 7, 3, False)

    return game


def execute_kickoff(game):
    """
    Executes a kickoff play
    """
    kicker = game.offense.get_player('K', 1)
    returner = game.defense.get_player('KR', 1)
    onside = determine_onside_kick(game)

    if onside:
        return execute_onside_kickoff(game)

    chance_mod = random_in_range(-10, 10)
    #TODO great blocking implementation
    great_blocking = False
    return_mod = random_in_range(-5, 5)

    #TODO if great blocking

    back_of_endzone = False
    out_of_bounds = False

    max_kick = (35
            + 25
            + (65 * (kicker.kick_power / 100.0))
            + (2 * chance_mod)
            + game.kick_mod
            + random_variability())

    min_kick = (35
            + 20
            + (55 * (kicker.kick_power / 100.0))
            + (2 * chance_mod)
            + game.kick_mod
            + random_variability())

    #TODO implement st_mod
    st_mod = 0.0
    return_stat = returner.agility
    if (returner.agility < returner.concentration):
        return_stat = returner.concentration

    min_return = ((0.2 * return_stat + random_variability())
            - st_mod
            + return_mod)

    max_return = ((0.35 * returner.speed + random_variability())
            - st_mod
            + return_mod)

    returns = random_in_range((min_return + return_mod), max_return + return_mod)
    kick = random_in_range((min_kick + chance_mod), (max_kick + chance_mod))

    #TODO if great blocking breakaway

    if kick > 105:
        kick = 105
        if random_chance(kicker.kick_power / 4 + kick_mod):
            back_of_endzone = True
            returns = 0
    elif random_chance((100 - kicker.kick_accuracy) / 2 - kick_mod + 1):
        out_of_bounds = True
        kick = 60
        returns = 0

    if (kick >= 100) and great_blocking is False and random_chance(return_stat - 30):
        returns = 0

    if (kick >= 100) and great_blocking is False and returns < 15:
        returns = 0

    kick_return = kick - returns
    touchback = False
    touchdown = False
    if kick_return > 99:
        kick_return = 80
        tocuhback = True

    if kick_return < 1:
        touchdown = True
        returns = kick
        kick_return = 0

    if touchback is False and out_of_bounds is False:
        log_kr = True
        #TODO log KR to returner

    game.yard_line = 100 - kick_return

    if touchback:
        log_tb = True
        #TODO log touchback to kicker

    if touchdown:
        game.defense.score += 6
        game = spend_time(10, 20, 10, False)
        game = execute_turnover(game)
        if game.overtime is False:
            return execute_extra_point(game)

    #TODO clean up post kickoff possession change logic

    return game


def execute_onside_kickoff(game):
    """
    Executes an onside kickoff play
    """
    recover = random_weighted_choice(
            1, game.offense.calculate_special_teams_rating(game.offense.players),
            2, game.defense.calculate_special_teams_rating(game.defense.players) + 100)

    recovering_team = game.offense if recover == 1 else game.defense

    game.yard_line = 100 - 35 - 10 - random_in_range(0, 3)

    game = spend_time(2, 5, 5, False)

    #TODO log onside kick attempt and update game state

    if recovering_team is game.defense:
        return execute_turnover(game)

    game.down = 1
    game.to_go = game.yard_line if 10 > game.yard_line else 10
    return game


def execute_extra_point(game):
    """
    Executes an extra point play
    """
    return game


def execute_qb_kneel(game):
    """
    Executes a QB kneel play
    """
    return game
