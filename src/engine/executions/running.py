"""
Execution logic for run plays
"""
import random
from services.rng import random_chance, random_variability, random_weighted_choice

def execute_run_play(run_type, down, togo, yard_line, rb1, rb2,
                     fb, te, offense, defense, play_mod, run_mod):
    """
    Executes a run play
    """
    rusher = None
    break_stat = 50.0

    if run_type is 0:
        if togo is 1:
            break_stat = fb.speed * 0.75
            rusher = fb
        else:
            break_stat = rb1.agility
            rusher = rb1
    elif run_type is 1 or run_type is 2:
        break_stat = rb1.agility
        rusher = rb1
    elif run_type is 3 or run_type is 4:
        break_stat = rb2.agility
        rusher = rb2
    elif run_type is 5:
        break_stat = fb.speed * 0.75
        rusher = fb

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
                + random_variability()
                + rush_mod)

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
                + (1.25 * ((offense.gameplan.o_aggression
                - (100 - defense.gameplan.d_aggression)) / 100.0))
                + random_variability()) + rush_mod

    if defense.gameplan.d_style is '43':
        max_rush = (max_rush
                    - (8.5 * (defense.run_defense / 100.0))
                    - (3.0 * (defense.get_player('LOLB', 1).tackling / 100.0))
                    - (3.0 * (defense.get_player('MLB', 1).tackling / 100.0))
                    - (3.0 * (defense.get_player('ROLB', 1).tackling / 100.0)))

        if random_chance(100 - rusher.concentration) and random_chance(defense.run_defense / 2):
            min_rush -= 1

    else:
        max_rush = (max_rush
                    - (1.5 * (defense.run_defense / 100.0))
                    - (4.0 * (defense.get_player('LOLB', 1).tackling / 100.0))
                    - (4.0 * (defense.get_player('LILB', 1).tackling / 100.0))
                    - (4.0 * (defense.get_player('RILB', 1).tackling / 100.0))
                    - (4.0 * (defense.get_player('ROLB', 1).tackling / 100.0)))

        if random_chance(rusher.concentration) and random_chance(
                (defense.get_player('LOLB', 1).tackling
                 + defense.get_player('LILB', 1).tackling
                 + defense.get_player('RILB', 1).tackling
                 + defense.get_player('ROLB', 1).tackling)) / 8:
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

    if (gain >= 7
            or random_chance(break_stat / 4.0 + random_variability())
            and random_chance(rusher.speed / 1.5)):
        max_additional = ((22.0 * (rusher.speed / 100.0))
                          - (2.5 * (defense.get_player('LCB', 1).tackling / 100.0))
                          - (2.5 * (defense.get_player('RCB', 1).tackling / 100.0))
                          - (3.5 * (defense.get_player('SS', 1).tackling / 100.0))
                          - (3.5 * (defense.get_player('FS', 1).tackling / 100.0))
                          + (2.0 * play_mod)
                          + (0.5 * run_mod)
                          + (0.25 * (offense.team_mod - defense.team_mod))
                          + random_variability())

        if max_additional < 1:
            max_additional = 1

        gain += random.uniform(0, max_additional)

        big_play_mod = 0

        while random_chance(rusher.speed / 2 + (6 * big_play_mod)):
            max_additional = ((20.0 * (rusher.speed / 100.0))
                              - (2.5 * (defense.get_player('LCB', 1).tackling / 100.0))
                              - (2.5 * (defense.get_player('RCB', 1).tackling / 100.0))
                              - (3.5 * (defense.get_player('SS', 1).tackling / 100.0))
                              - (3.5 * (defense.get_player('FS', 1).tackling / 100.0))
                              + (2.0 * play_mod)
                              + (0.5 * run_mod)
                              + (0.25 * (offense.team_mod - defense.team_mod))
                              + random_variability())

            if max_additional < 1:
                max_additional = 1

            gain += random.uniform(0, max_additional)

            if random_chance(break_stat / 2):
                big_play_mod += 1

            if rusher.speed / 2 + (8 * big_play_mod) > 100:
                gain = 101

    if random_chance(105 - rusher.break_tackle):
        gain -= 1

    if gain < -5 and random_chance(90):
        gain = -5

    if gain < 0:
        weighted_choices = [(offense.get_player('LT', 1), 1),
                            (offense.get_player('LG', 1), 1),
                            (offense.get_player('C', 1), 1),
                            (offense.get_player('RG', 1), 1),
                            (offense.get_player('RT', 1), 1)]

        allowed_loss = random_weighted_choice(weighted_choices)

        # TODO record TFL allowed here
    elif gain > 5:
        foo = 0
        # TODO pancake logic, record pancacke here

    td = 0
    fumble = False

    if gain >= yard_line:
        gain = yard_line
        td = 1
    else:
        if defense.gameplan.d_style is '43':
            fum_chance = ((1.8 * rusher.concentration)
                          - (0.35 * defense.run_defense)
                          - (0.05 * defense.get_player('LOLB', 1).tackling)
                          - (0.05 * defense.get_player('MLB', 1).tackling)
                          - (0.05 * defense.get_player('ROLB', 1).tackling)
                          + (0.2 * (((100 - offense.gameplan.o_aggression)
                                     - defense.gameplan.d_aggression)))
                          + random_variability())
        else:
            fum_chance = ((1.8 * rusher.concentration)
                          - (0.1 * defense.run_defense)
                          - (0.1 * defense.get_player('LOLB', 1).tackling)
                          - (0.1 * defense.get_player('LILB', 1).tackling)
                          - (0.1 * defense.get_player('RILB', 1).tackling)
                          - (0.1 * defense.get_player('ROLB', 1).tackling)
                          + (0.2 * (((100 - offense.gameplan.o_aggression)
                                     - defense.gameplan.d_aggression)))
                          + random_variability())

        if fum_chance < 5:
            fum_chance = 5

        if int(random.uniform(0, int(fum_chance))) == 0:
            if (yard_line - gain) < 100.0:
                fumble = True

    fumble_forcer = defense.get_player('LDE', 1)

    if fumble:
        if gain < 6 and (random_chance(95) or random_chance(5)):
            if defense.gameplan.d_style is '43':
                choices = [
                    (defense.get_player('LOLB', 1), defense.get_player('LOLB', 1).tackling),
                    (defense.get_player('MLB', 1), defense.get_player('MLB', 1).tackling),
                    (defense.get_player('ROLB', 1), defense.get_player('ROLB', 1).tackling)
                ]
                fumble_forcer = random_weighted_choice(choices)
            else:
                choices = [
                    (defense.get_player('LOLB', 1), defense.get_player('LOLB', 1).tackling),
                    (defense.get_player('LILB', 1), defense.get_player('LILB', 1).tackling),
                    (defense.get_player('RILB', 1), defense.get_player('RILB', 1).tackling),
                    (defense.get_player('ROLB', 1), defense.get_player('ROLB', 1).tackling)
                ]
                fumble_forcer = random_weighted_choice(choices)
    else:
        choices = [
            (defense.get_player('LCB', 1), defense.get_player('LCB', 1).tackling),
            (defense.get_player('RCB', 1), defense.get_player('RCB', 1).tackling),
            (defense.get_player('SS', 1), defense.get_player('SS', 1).tackling),
            (defense.get_player('FS', 1), defense.get_player('FS', 1).tackling)
        ]
        fumble_forcer = random_weighted_choice(choices)



    return gain, td, fumble, fumble_forcer.name if fumble else None
