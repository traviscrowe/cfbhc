"""
Contains functions to determine specific outcomes given game state
"""
import random
from services.rng import random_chance, random_variability
from engine.executions.running import execute_run_play, execute_qb_scramble
from engine.executions.passing import execute_pass_play
from engine.executions.special_teams import execute_field_goal, execute_qb_kneel

def determine_play(game):
    """
    Determines the outcome of a given play
    """
    if determine_premature_fg(game):
        return execute_field_goal(game)
    elif determine_qb_kneel(game):
        return execute_qb_kneel(game)
    elif determine_run_play(game):
        return execute_run_play(game)
    else:
        if determine_qb_scramble(game):
            return execute_qb_scramble(game)
        else:
            return execute_pass_play(game)

def determine_completion_chance(game, play_mod):
    """
    Return the chance of pass completion from passed game state
    """
    chance_mod = random.randint(-3, 3)

    chance = (27.5
              + (30.0 * (game.offense.get_player('QB', 1).throw_accuracy / 100.0))
              + (2.5 * (game.offense.get_player('QB', 1).throw_power / 100.0))
              + (20.0 * (game.offense.pass_blocking / 100.0))
              + (2.5 * (game.offense.get_player('TE', 1).run_blocking / 100.0))
              + (2.5 * (game.offense.get_player('FB', 1).run_blocking / 100.0))
              + (4.5 * (game.offense.get_player('TE', 1).catching / 100.0))
              + (0.5 * (game.offense.get_player('WR', 1).concentration / 100.0))
              + (0.5 * (game.offense.get_player('WR', 2).concentration / 100.0))
              + (0.5 * (game.offense.get_player('WR', 3).concentration / 100.0))
              + (4.0 * (game.offense.get_player('WR', 1).acceleration / 100.0))
              + (4.0 * (game.offense.get_player('WR', 2).acceleration / 100.0))
              + (4.0 * (game.offense.get_player('WR', 3).acceleration / 100.0))
              + (6.0 * (game.offense.get_player('WR', 1).catching / 100.0))
              + (6.0 * (game.offense.get_player('WR', 2).catching / 100.0))
              + (6.0 * (game.offense.get_player('WR', 3).catching / 100.0))
              + (0.5 * (game.offense.get_player('RB', 1).catching / 100.0))
              + (0.5 * (game.offense.get_player('RB', 2).catching / 100.0))
              + (0.05 * (game.offense.get_player('FB', 1).catching / 100.0))
              - (8.5 * (game.defense.get_player('LCB', 1).coverage / 100.0))
              - (8.5 * (game.defense.get_player('RCB', 1).coverage / 100.0))
              - (7.0 * (game.defense.get_player('SS', 1).coverage / 100.0))
              - (7.0 * (game.defense.get_player('FS', 1).coverage / 100.0))
              + (0.5 * (game.offense.get_player('QB', 1).speed / 100.0))
              + (2.0 * (game.offense.get_player('QB', 1).concentration / 100.0))
              + (3.0 * play_mod)
              + (0.25 * (game.offense.team_mod - game.defense.team_mod))
              + (1.0 * game.pass_mod)
              - (1.25 * (100 - game.defense.drun) / 100.0)
              + (1.0 * ((100.0 - game.offense.gameplan.o_aggression) / 100.0))
              - (1.0 * ((100.0 - game.defense.gameplan.d_aggression) / 100.0))
              + chance_mod
              + random_variability())

    if game.defense.style is '43':
        chance += (0
                   - (20.0 * (game.defense.pass_rush / 100.0))
                   - (2.5 * (game.defense.get_player('LOLB', 1).pass_rush / 100.0))
                   - (2.5 * (game.defense.get_player('MLB', 1).pass_rush / 100.0))
                   - (2.5 * (game.defense.get_player('ROLB', 1).pass_rush / 100.0))
                   - (2.0 * (game.defense.get_player('LOLB', 1).coverage / 100.0))
                   - (2.0 * (game.defense.get_player('MLB', 1).coverage / 100.0))
                   - (2.0 * (game.defense.get_player('ROLB', 1).coverage / 100.0)))
    else:
        chance += (0
                   - (6.5 *  (game.defense.pass_rush / 100.0))
                   - (4.75 * (game.defense.get_player('LOLB', 1).pass_rush / 100.0))
                   - (4.75 * (game.defense.get_player('LILB', 1).pass_rush / 100.0))
                   - (4.75 * (game.defense.get_player('RILB', 1).pass_rush / 100.0))
                   - (4.75 * (game.defense.get_player('ROLB', 1).pass_rush / 100.0))
                   - (2.0 * (game.defense.get_player('LOLB', 1).coverage / 100.0))
                   - (2.0 * (game.defense.get_player('LILB', 1).coverage / 100.0))
                   - (2.0 * (game.defense.get_player('RILB', 1).coverage / 100.0))
                   - (2.0 * (game.defense.get_player('ROLB', 1).coverage / 100.0)))

    while (chance < 60) and not random_chance(game.defense.get_player('RCB', 1).coverage + 1) \
            and not random_chance(game.defense.get_player('FS', 1) + 1):
        chance += 0.25
        if chance > 60:
            chance = 60

    if chance < 52:
        chance += (52 - chance) / 1.5

    if chance > 62:
        chance += (chance - 62) / 1.5

    if game.yard_line <= 10:
        chance -= 3

    return chance

def determine_sack_chance(game):
    """
    Determines the chance for a sack to occur
    """
    chance_mod = random.randint(-3, 3)

    chance = (0.0
              - (20.0 * (game.offense.pass_blocking / 100.0))
              - (0.75 * (game.offense.get_player('QB', 1).speed / 100.0))
              - (0.75 * (game.offense.get_player('QB', 1).throw_power / 100.0))
              - (1.0 * (game.offense.get_player('FB', 1).pass_protect / 100.0))
              - (0.75 * (game.offense.get_player('TE', 1).pass_protect / 100.0))
              + chance_mod
              + random_variability())

    if game.defense.style is '43':
        chance += ((35.0 * (game.defense.pass_rush / 100.0))
                   + (3.0 * (game.defense.get_player('LOLB', 1).pass_rush / 100.0))
                   + (3.0 * (game.defense.get_player('MLB', 1).pass_rush / 100.0))
                   + (3.0 * (game.defense.get_player('ROLB', 1).pass_rush / 100.0)))
    else:
        chance += ((9.0 * (game.defense.pass_rush / 100.0))
                   + (9.0 * (game.defense.get_player('LOLB', 1).pass_rush / 100.0))
                   + (8.5 * (game.defense.get_player('LILB', 1).pass_rush / 100.0))
                   + (8.5 * (game.defense.get_player('RILB', 1).pass_rush / 100.0))
                   + (9.0 * (game.defense.get_player('ROLB', 1).pass_rush / 100.0)))

    if chance < 0.0:
        chance = 0.0

    return chance

def determine_interception_chance(game):
    """
    Determines the chance for an interception to occur
    """
    chance_mod = random.randint(-3, 3)

    chance = (0.0
              + (6.5 * (game.defense.get_player('CB', 1).catching / 100.0))
              + (6.5 * (game.defense.get_player('CB', 2).catching / 100.0))
              + (0.5 * (game.defense.get_player('CB', 1).coverage / 100.0))
              + (0.5 * (game.defense.get_player('CB', 2).coverage / 100.0))
              + (7.0 * (game.defense.get_player('FS', 1).catching / 100.0))
              + (7.0 * (game.defense.get_player('SS', 1).catching / 100.0))
              - (3.0 * (game.offense.get_player('QB', 1).throw_accuracy / 100.0))
              - (0.0 * (game.defense.get_player('QB', 1).throw_accuracy / 100.0))
              - (15.5 * (game.defense.get_player('CB', 1).concentration / 100.0))
              - (6.5 * (game.defense.get_player('CB', 1).catching / 100.0))
              - (0.0 * (game.defense.pass_blocking / 100.0))
              - (0.5 * (game.defense.get_player('WR', 1).concentration / 100.0))
              - (0.5 * (game.defense.get_player('WR', 2).concentration / 100.0))
              - (0.5 * (game.defense.get_player('WR', 3).concentration / 100.0))
              + chance_mod + random_variability())

    if chance < 0.0:
        chance = 0.0

    return chance


def determine_qb_kneel(game):
    """
    Determines liklihood of a QB kneel
    """
    return ((game.offense.score > game.defense.score)
            and (game.time <= (40 * (4 - game.down)))
            and (game.yard_line < 99)
            and (game.time <= 120))


def determine_premature_fg(game):
    """
    Determines the chance for the offense to kick an early FG
    """
    return game


def determine_run_play(game):
    """
    Determines the chance for the offense to execute a run play
    """
    return game


def determine_pass_play(game):
    """
    Determines the chance for the offense to execute a pass play
    """
    return game


def determine_qb_scramble(game):
    """
    Determines the chance for the QB to scramble on a pass play
    """
    return game
