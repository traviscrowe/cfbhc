"""
Execution logic for special teams plays
"""
from engine.determinations import determine_play
from engine.clock import spend_time
from services.rng import random_in_range, random_variability, random_weighted_choice, random_chance

def execute_fourth_down(game):
    desperation_time = 160 + (game.offense.gameplan.o_aggression / 2)

    if (game.offense.score < game.defense.score) and (game.time <= 900) and (time <= (desperation_time * ((game.defense.score - game.offense.score) / 8) + 1)):
        if (game.offense.score) + 3 >= game.defense.score or time > (desperation_time (game.defense.score - game.offense.score - 3) / 9):
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
        elif game.yard_line <= 55 and random_in_range(-1, go_chance) <= 10 and go_chance <= 500 and game.to_go <= 6:
            return determine_play(game)
        else:
            return execute_punt(game)

def execute_turnover(game):
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
        defense.score += 6
        game = spend_time(10, 15, 10, False)
        game = execute_turnover()
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


def execute_onside_kickoff(game):
    return game

def execute_extra_point(game):
    return game


def execute_qb_kneel(game):
    return game
