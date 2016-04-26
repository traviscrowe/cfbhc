"""
Execution logic for pass plays
"""
import random
from services.rng import random_chance, random_weighted_choice, random_variability
from engine.determinations import determine_completion_chance, determine_sack_chance

def execute_pass_play(pass_type, offense, defense, play_mod, game, sack_mod):
    """
    Executes a pass play
    """
    pass_type_mod = 0

    if pass_type is 3:
        # if total run plays - 3 >= total pass plays in this game by the offense
        pass_type_mod = 5
        # else pass_type_mod = -5
    if pass_type is 4:
        pass_type_mod = 10

    if random_chance(determine_completion_chance(game, play_mod) + pass_type_mod):
        return execute_completed_pass(pass_type, offense, defense, play_mod, game)
    else:
        incompletion_chance = 85.0 + (game.offense.pass_blocking / 5.0) \
            - (1.5 * (100 - game.defense.gameplan.d_run) / 100.0) \
            + (2.0 * play_mod) \
            + (0.5 * (offense.team_mod - defense.team_mod)) \
            + ((100.0 - offense.gameplan.o_aggression) / 100.0) \
            - (defense.gameplan.d_aggression / 100.0) \
            + random_variability()

        choices = [
            (1, int(determine_sack_chance(game), sack_mod)),
            (2, 0),
            (3, int(incompletion_chance))
        ]
        result = random_weighted_choice(choices)

        if result == 1:
            print('sack!')  # sack()
            #TODO implement sack() method
        elif result == 2:
            print('interception!')  # interception()
            #TODO implement interception() method
        # elif check_scramble():
        else:
            print('incomplete!')  # incompletion()
            #TODO implement incompletion() method


def execute_completed_pass(pass_type, offense, defense, play_mod, game):
    """
    Executes a completed pass
    """
    pass_mod = random.randint(-5, 5)

    max_gain = (3.25
                + (10.0 * (offense.get_player('QB', 1).throw_power / 100.0))
                + (1.5 * play_mod)
                + (0.15 * (offense.team_mod - defense.team_mod))
                + (0.5 * game.pass_mod))

    gain = random.randint(int(1 + pass_mod), int(max_gain + pass_mod))

    if gain > 9:
        foo = 0
        #TODO implement pancacke logic

    if pass_type is 2:
        gain = random.randint(int(offense.get_player('QB', 1).throw_power / 2
                              + pass_mod),
                              int(offense.get_player('QB', 1).throw_power / 2
                              + max_gain + pass_mod))

    receiver = None

    check_down = False

    pass_mod = random.randint(-5, 5)

    ag_play = (72.5 +
               offense.get_player('QB', 1).throw_power / 10
               + ((offense.gameplan.o_aggression - 50) / 50) + ((defense.gameplan.d_aggression - 50) / 50)
               - (defense.get_player('CB', 1).coverage - 50) / 7.5
               - (defense.get_player('CB', 1).coverage - 50) / 7.5
               + pass_mod
               + play_mod
               + random_variability())

    if pass_type is 0:
        ag_play -= 5

    if pass_type is 1:
        ag_play += 5

    if ag_play > 80:
        ag_play = 80
    elif ag_play < 65:
        ag_play = 65

    if pass_type is 3:
        ag_play = 95

    if random_chance(ag_play):
        lb_coverage = (defense.get_player('LOLB', 1).coverage
                       + defense.get_player('ROLB', 1).coverage) - 100

        weighted_choices = [
            (offense.get_player('WR', 1),
            int((offense.get_player('WR', 1).catching * 3.05
            + offense.get_player('WR', 1).acceleration
            - ((defense.get_player('LCB', 1).coverage - 50.0) / 25.0)
            + random_variability()))),
            (offense.get_player('WR', 2),
            int((offense.get_player('WR', 2).catching * 3.05
             + offense.get_player('WR', 2).acceleration
             - ((defense.get_player('RCB', 1).coverage - 50.0) / 25.0)
             + random_variability()))),
            (offense.get_player('WR', 3),
            int((offense.get_player('WR', 3).catching * 3.05
             + offense.get_player('WR', 3).acceleration
             - ((defense.get_player('SS', 1).coverage - 50.0) / 50.0)
             - ((defense.get_player('FS', 1).coverage - 50.0) / 50.0)
             + random_variability()))),
            (offense.get_player('TE', 1),
            int((offense.get_player('TE', 1).catching * 3.05
             - lb_coverage / 50.0
             - ((offense.gameplan.o_aggression - 50.0) / 50.0)
             + offense.get_player('TE', 1).speed / 2.0
             + random_variability())))
        ]

        receiver = random_weighted_choice(weighted_choices)
    else:
        weighted_choices = [
            (offense.get_player('TE', 1), int((offense.get_player('TE', 1).catching * 1.5) + 1)),
            (offense.get_player('RB', 1), offense.get_player('RB', 1).catching),
            (offense.get_player('RB', 2), offense.get_player('RB', 2).catching),
            (offense.get_player('FB', 1), offense.get_player('FB', 1).catching)
        ]

        receiver = random_weighted_choice(weighted_choices)

        if receiver is offense.get_player('RB', 1):
            weighted_choices = [
                (offense.get_player('RB', 1),
                offense.get_player('RB', 1).catching * 2
                + offense.get_player('RB', 2).catching * 2 + 1),
                (offense.get_player('FB', 1),
                int(offense.get_player('FB', 1).catching / 2 + 1))
            ]

            receiver = random_weighted_choice(weighted_choices)

            if receiver is offense.get_player('RB', 1):
                weighted_choices = [
                    (offense.get_player('RB', 1),
                    offense.get_player('RB', 1).catching * 2 + 1),
                    (offense.get_player('RB', 2),
                    offense.get_player('RB', 2).catching * 2 + 1)
                ]

                receiver = random_weighted_choice(weighted_choices)

    if pass_type is 4:
        weighted_choices = [
            (offense.get_player('RB', 1),
            offense.get_player('RB', 1) * 2 + 1),
            (offense.get_player('RB', 2),
            offense.get_player('RB', 2) * 2 + 1)
        ]

        receiver = random_weighted_choice(weighted_choices)

    break_stat = 50

    if receiver is offense.get_player('WR', 1):
        break_stat = receiver.acceleration

        if random_chance(105 - receiver.acceleration):
            check_down = True
    elif receiver is offense.get_player('WR', 2):
        break_stat = receiver.acceleration

        if random_chance(105 - receiver.acceleration):
            check_down = True
    elif receiver is offense.get_player('WR', 3):
        break_stat = receiver.acceleration

        if random_chance(105 - receiver.acceleration):
            check_down = True
    elif receiver is offense.get_player('TE', 1):
        break_stat = receiver.speed

        if random_chance(105 - receiver.speed / 1.5 + random_variability()):
            check_down = True
    elif receiver is offense.get_player('RB', 1) or offense.get_player('RB', 2):
        break_stat = receiver.agility

        if random_chance(105 - receiver.agility / 1.75 + random_variability()):
            check_down = True
    elif receiver is offense.get_player('FB', 1):
        break_stat = receiver.break_tackle

        if random_chance(105 - receiver.speed / 2.0 + random_variability()):
            check_down = True

    pass_mod = random.randint(-3, 3)

    if check_down:
        max_gain = (1.0
                    + (4.0 * (receiver.speed / 100.0))
                    - (0.25 * (defense.get_player('LCB', 1).tackling / 100.0))
                    - (0.25 * (defense.get_player('RCB', 1).tackling / 100.0))
                    - (0.25 * (defense.get_player('SS', 1).tackling / 100.0))
                    - (0.25 * (defense.get_player('FS', 1).tackling / 100.0))
                    + (1.0 * ((offense.gameplan.o_aggression - (100 - defense.gameplan.d_aggression)) / 100.0))
                    - (1.0 * (100 - defense.gameplan.d_run) / 100.0)
                    + pass_mod
                    + random_variability())

        while not random_chance(defense.get_player('SS', 1).tackling + 1)\
            and not random_chance(defense.get_player('FS', 1).tackling + 1)\
                and (max_gain < 200):
            max_gain += 0.25
    else:
        max_gain = (2.0
                    + (12.0 * (receiver.speed / 100.0))
                    - (0.5 * (defense.get_player('LCB', 1).tackling / 100.0))
                    - (0.5 * (defense.get_player('RCB', 1).tackling / 100.0))
                    - (0.5 * (defense.get_player('SS', 1).tackling / 100.0))
                    - (0.5 * (defense.get_player('FS', 1).tackling / 100.0))
                    + (1.0 * ((offense.gameplan.o_aggression - (100 - defense.gameplan.d_aggression)) / 100.0))
                    - (1.0 * (100 - defense.gameplan.d_run) / 100.0) + pass_mod + random_variability())

        while not random_chance(defense.get_player('SS', 1).tackling + 1)\
            and not random_chance(defense.get_player('FS', 1).tackling + 1)\
                and (max_gain < 200):
            max_gain += 0.5

    if max_gain < 0:
        max_gain = 0

    gain += random.randint(0, int(max_gain))

    break_free = (break_stat / 2.5 + random.randint(-5, 5) + random_variability())

    if check_down:
        break_free = (break_stat / 5.0 + random.randint(-5, 5) + random_variability())

    if break_free < 15:
        break_free = 15

    num_free = 0

    while random_chance(break_free + (10 * num_free)) and gain <= 100:
        max_gain = (2.5
                    + (22.5 * (receiver.speed / 100.0))
                    - (3.5 * (defense.get_player('LCB', 1).tackling / 100.0))
                    - (3.5 * (defense.get_player('RCB', 1).tackling / 100.0))
                    - (5.5 * (defense.get_player('SS', 1).tackling / 100.0))
                    - (5.5 * (defense.get_player('FS', 1).tackling / 100.0))
                    + (2.0 * play_mod)
                    + (0.25 * (offense.team_mod - defense.team_mod))
                    + (0.25 * (offense.gameplan.o_aggression / 100.0))
                    + random_variability())

        if max_gain < 1:
            max_gain = 1

        gain += random.randint(0, int(max_gain))

        if random_chance(receiver.speed / 1.5 + random_variability()):
            num_free += 1

        if (break_free + (10 * num_free)) > 100:
            gain = 101

    if gain < -2:
        gain = -2

    td = 0

    fumble = False

    if gain >= game.yard_line:
        gain = game.yard_line
        td = 1
    else:
        td = 0

        fum_chance = ((1.55 * receiver.concentration)
                                 - (0.1 * defense.get_player('LCB', 1).tackling)
                                 - (0.1 * defense.get_player('RCB', 1).tackling)
                                 - (0.15 * defense.get_player('SS', 1).tackling)
                                 - (0.15 * defense.get_player('FS', 1).tackling)
                                 + (0.2 * (((100 - offense.gameplan.o_aggression)
                                 - defense.gameplan.d_aggression))) + random_variability())

        if fum_chance < 5:
            fum_chance = 5

        if int(random.uniform(0, int(fum_chance))) == 0:
            if (game.yard_line - gain) < 100:
                fumble = True

    fumble_forcer = defense.get_player('RDE', 1)

    if fumble:
        if ((gain < 10) and random_chance(95)) or random_chance(5):
            if defense.gameplan.d_style is '43':
                choices = [
                    (defense.get_player('LOLB', 1), defense.get_player('LOLB', 1).tackling + 1),
                    (defense.get_player('MLB', 1), defense.get_player('MLB', 1).tackling + 1),
                    (defense.get_player('ROLB', 1), defense.get_player('ROLB', 1).tackling + 1),
                    (defense.get_player('LCB', 1), defense.get_player('LCB', 1).tackling * 2
                     - defense.get_player('LCB', 1).coverage + 1),
                    (defense.get_player('LCB', 2), defense.get_player('LCB', 2).tackling * 2
                     - defense.get_player('LCB', 2).coverage + 1)
                ]
                fumble_forcer = random_weighted_choice(choices)
            else:
                choices = [
                    (defense.get_player('LOLB', 1), defense.get_player('LOLB', 1).tackling + 1),
                    (defense.get_player('LILB', 1), defense.get_player('LILB', 1).tackling + 1),
                    (defense.get_player('RILB', 1), defense.get_player('RILB', 1).tackling + 1),
                    (defense.get_player('ROLB', 1), defense.get_player('ROLB', 1).tackling + 1),
                    (defense.get_player('LCB', 1), defense.get_player('LCB', 1).tackling + 1),
                    (defense.get_player('RCB', 1), defense.get_player('RCB', 1).tackling + 1)
                ]
                fumble_forcer = random_weighted_choice(choices)
        else:
            choices = [
                (defense.get_player('LCB', 1), defense.get_player('LCB', 1).tackling + 1),
                (defense.get_player('RCB', 1), defense.get_player('RCB', 1).tackling + 1),
                (defense.get_player('SS', 1), defense.get_player('SS', 1).tackling + 1),
                (defense.get_player('FS', 1), defense.get_player('FS', 1).tackling + 1)
            ]
            fumble_forcer = random_weighted_choice(choices)

    return receiver.name, gain, td, fumble
