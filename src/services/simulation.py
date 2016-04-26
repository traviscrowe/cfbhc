__author__ = 'traviscrowe'
from enum import Enum
from services.rng import random_chance, random_weighted_choice, random_in_range, random_variability
from engine.clock import calculate_seconds, spend_time
from engine.determinations import determine_
import random, pdb


class RunTypes(Enum):
    NO_PLAY = 0
    RB1_INSIDE = 1
    RB2_INSIDE = 2
    RB1_OUTSIDE = 3
    RB2_OUTSIDE = 4
    FULLBACK = 5


class PassTypes(Enum):
    SLANT = 0
    SHOTGUN = 1
    HAIL_MARY = 2
    PLAY_ACTION = 3
    RB_SCREEN = 4
    QB_KNEEL = 5


def run(game):
    pdb.set_trace()
    if random_chance(50):
        game.offense = game.away
        game.defense = game.home
    else:
        game.offense = game.home
        game.defense = game.away

    game.kicking_team = game.defense

    while game.time > 0:
        if game.overtime is False:
            if game.last_time > 2700 and game.time <= 2700:
                game.quarter = 2
            if game.last_time > 1800 and game.time <= 1800:
                game.quarter = 3
                game.time = 1800

                if game.kicking_team != game.offense:
                    tmp = game.offense
                    game.offense = game.defense
                    game.defense = tmp

                #TODO implement second half kickoff
            if game.last_time > 900 and game.time <= 900:
                game.quarter = 4
        else:
            if game.offense.score != game.defense.score:
                game.time = 0

        if game.down < 4:
            game = determine_play(game)
        elif game.down == 4:
            game = execute_fourth_down(game)
        else:
            game = execute_turnover(game)

        if game.time <= 0:
            foo = False
            #TODO check overtime

    return game

def get_play_mod(game):
    mod = 0
    third_apply = True

    if game.yard_line <= 5:
        mod += 2 * (6 - game.yard_line)

    if game.time <= 1800:
        if game.offense.score >= game.defense.score + 7:
            sev = game.offense.score - game.defense.score
            sev = sev/7
            if sev > 0:
                sev -= 1

            mod += random_in_range(-1 - sev, 0)

    if game.offense.score > game.defense.score:
        third_apply = False
        if game.time <= 300:
            mod += 30
        elif game.time <= 120:
            mod += 40
    elif game.offense.score < game.defense.score:
        if game.time <= 420:
            mod -= 30
        elif game.time <= 180:
            mod -= 40
    elif game.time <= calculate_seconds(4, 13, 0):
        if game.yard_line <= 50:
            mod -= 10
        else:
            third_apply = False
            mod += 10

    if (game.time >= calculate_seconds(3, 0, 0)) and (game.time <= calculate_seconds(2, 10, 0)):
        if game.yard_line <= 50:
            mod -= 10
        else:
            third_apply = False
            mod += 10

    if ((game.down == 3) and third_apply is True) or game.down == 4:
        intensity = -3
        if game.down == 4:
            intensity = -4

        mod += intensity * (game.to_go - 5)

    return mod
