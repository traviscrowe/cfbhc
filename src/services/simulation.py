from enum import Enum
from services.rng import random_chance
import random


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


def rush(run_type, down, togo, yard_line, rb1, rb2, fb, te, offense, defense, play_mod, run_mod):
    rusher = None
    direction = ''
    break_stat = 50.0

    if run_type is 0:
        direction = 'inside'
        if togo is 1:
            break_stat = fb.speed * 0.75
            rusher = fb
        else:
            break_stat = rb1.agility
            rusher = rb1
    elif run_type is 1 or run_type is 2:
        break_stat = rb1.agility
        rusher = rb1
        direction = 'inside'
    elif run_type is 3 or run_type is 4:
        break_stat = rb2.agility
        rusher = rb2
        direction = 'outside'
    elif run_type is 5:
        break_stat = fb.speed * 0.75
        rusher = fb
        direction = 'inside'

    rush_mod = random.randint(-4, 3)
    min_rush = (-3.0
        + (5.0 * (offense.run_blocking / 100.0))
        + (3.25 * (rusher.break_tackle / 100.0))
        + (0.5 * (break_stat / 100.0))
        + (1.25 * (fb.run_blocking / 100.0))
        + (0.25 * (te.run_blocking / 100.0))
        - (5.0 * (defense.run_defense / 100.0))
        + (1.0 * play_mod)
        + (0.1 * (offense.team_mod - defense.team_mod))
        + (0.25 * run_mod)
        - (0.5 * defense.gameplan.d_run / 100.0)
        + (1.25 * (((100 - offense.gameplan.o_aggression)
        - defense.gameplan.d_aggression) / 100.0))
        + random.random()) + rush_mod

    if (yard_line > 95) and (min_rush < -1):
        min_rush = -1

    if (yard_line >= 99) and (min_rush < 0):
        if random_chance(rusher.break_tackle - 20):
            min_rush = 0

    rush_mod = random.randint(-3, 4)
    max_rush = (3.0
        + (6.25 * (offense.run_blocking / 100.0))
        + (7.5 * (rusher.break_tackle / 100.0))
        + (2.5 * (break_stat / 100.0))
        + (0.5 * (rusher.speed / 100.0))
        + (2.5 * (fb.run_blocking / 100.0))
        + (1.5 * (te.run_blocking / 100.0))
        + (1.0 * play_mod)
        + (0.1 * (offense.team_mod - defense.team_mod))
        + (0.25 * run_mod)
        - (0.5 * defense.gameplan.d_run / 100.0)
        + (1.25 * ((offense.gameplan.o_aggression - (100 - defense.gameplan.d_aggression)) / 100.0))
        + random.random()) + rush_mod

    if defense.gameplan.d_style is '43':
        max_rush = (max_rush
                    - (8.5 * (defense.run_defense / 100.0))
                    - (3.0 * (defense.get_player_at_dc_pos_and_depth('OLB', 'LOLB', 1).tackling / 100.0))
                    - (3.0 * (defense.get_player_at_dc_pos_and_depth('ILB', 'MLB', 1).tackling / 100.0))
                    - (3.0 * (defense.get_player_at_dc_pos_and_depth('OLB', 'ROLB', 1).tackling / 100.0)))

        if random_chance(100 - rusher.concentration) and random_chance(defense.run_defense / 2):
            min_rush -= 1

    else:
        max_rush = (max_rush
                    - (1.5 * (defense.run_defense / 100.0))
                    - (4.0 * (defense.get_player_at_dc_pos_and_depth('OLB', 'LOLB', 1).tackling / 100.0))
                    - (4.0 * (defense.get_player_at_dc_pos_and_depth('ILB', 'LILB', 1).tackling / 100.0))
                    - (4.0 * (defense.get_player_at_dc_pos_and_depth('ILB', 'RILB', 1).tackling / 100.0))
                    - (4.0 * (defense.get_player_at_dc_pos_and_depth('OLB', 'ROLB', 1).tackling / 100.0)))

        if random_chance(rusher.concentration) and random_chance(
                (defense.get_player_at_dc_pos_and_depth('OLB', 'LOLB', 1).tackling
                     + defense.get_player_at_dc_pos_and_depth('ILB', 'LILB', 1).tackling
                     + defense.get_player_at_dc_pos_and_depth('ILB', 'RILB', 1).tackling
                     + defense.get_player_at_dc_pos_and_depth('OLB', 'ROLB', 1).tackling)) / 8:
            max_rush -= 1

    if run_type is 1 or run_type is 3:
        min_rush += rusher.break_tackle / 100
        max_rush -= 0.8
    if run_type is 2 or run_type is 4:
        min_rush -= 0.8
        max_rush += rusher.speed / 100

    if min_rush > max_rush:
        min_rush = max_rush

    gain = random.randint(int(min_rush), int(max_rush))

    resp = rusher.name + " runs " + direction + " for a gain of " + str(gain) + "\n"
    return gain
