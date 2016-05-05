"""
Execution logic for pass plays
"""
import random
from services.rng import random_chance, random_weighted_choice, random_variability
from engine.determinations import determine_completion_chance, determine_sack_chance

def execute_pass_play(game):
    """
    Executes a pass play
    """
    pass_type_mod = 0
    sack_mod = 0
    #TODO implement sack_mod based on defensive play call
    pass_type = 0
    #TODO implement pass_type calculation

    if pass_type is 3:
        # if total run plays - 3 >= total pass plays in this game by the offense
        pass_type_mod = 5
        # else pass_type_mod = -5
    if game.pass_type is 4:
        pass_type_mod = 10

    if random_chance(determine_completion_chance(game) + pass_type_mod):
        return execute_completed_pass(game, pass_type)
    else:
        incompletion_chance = 85.0 + (game.offense.pass_blocking / 5.0) \
            - (1.5 * (100 - game.defense.gameplan.d_run) / 100.0) \
            + (2.0 * game.play_mod) \
            + (0.5 * (game.offense.team_mod - game.defense.team_mod)) \
            + ((100.0 - game.offense.gameplan.o_aggression) / 100.0) \
            - (game.defense.gameplan.d_aggression / 100.0) \
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


def execute_completed_pass(game, pass_type):
    """
    Executes a completed pass
    """
    pass_mod = random.randint(-5, 5)

    max_gain = (3.25
                + (10.0 * (game.offense.get_player('QB', 1).throw_power / 100.0))
                + (1.5 * game.play_mod)
                + (0.15 * (game.offense.team_mod - game.defense.team_mod))
                + (0.5 * game.pass_mod))

    gain = random.randint(int(1 + pass_mod), int(max_gain + pass_mod))

    if gain > 9:
        foo = 0
        #TODO implement pancacke logic

    if pass_type is 2:
        gain = random.randint(int(game.offense.get_player('QB', 1).throw_power / 2
                                  + pass_mod),
                              int(game.offense.get_player('QB', 1).throw_power / 2
                                  + max_gain + pass_mod))

    receiver = None

    check_down = False

    pass_mod = random.randint(-5, 5)

    ag_play = (72.5 +
               game.offense.get_player('QB', 1).throw_power / 10
               + ((game.offense.gameplan.o_aggression - 50) / 50) + ((game.defense.gameplan.d_aggression - 50) / 50)
               - (game.defense.get_player('CB', 1).coverage - 50) / 7.5
               - (game.defense.get_player('CB', 1).coverage - 50) / 7.5
               + game.pass_mod
               + game.play_mod
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
        lb_coverage = (game.defense.get_player('LOLB', 1).coverage
                       + game.defense.get_player('ROLB', 1).coverage) - 100

        weighted_choices = [
            (game.offense.get_player('WR', 1),
             int((game.offense.get_player('WR', 1).catching * 3.05
                  + game.offense.get_player('WR', 1).acceleration
                  - ((game.defense.get_player('LCB', 1).coverage - 50.0) / 25.0)
                  + random_variability()))),
            (game.offense.get_player('WR', 2),
             int((game.offense.get_player('WR', 2).catching * 3.05
                  + game.offense.get_player('WR', 2).acceleration
                  - ((game.defense.get_player('RCB', 1).coverage - 50.0) / 25.0)
                  + random_variability()))),
            (game.offense.get_player('WR', 3),
             int((game.offense.get_player('WR', 3).catching * 3.05
                  + game.offense.get_player('WR', 3).acceleration
                  - ((game.defense.get_player('SS', 1).coverage - 50.0) / 50.0)
                  - ((game.defense.get_player('FS', 1).coverage - 50.0) / 50.0)
                  + random_variability()))),
            (game.offense.get_player('TE', 1),
             int((game.offense.get_player('TE', 1).catching * 3.05
                  - lb_coverage / 50.0
                  - ((game.offense.gameplan.o_aggression - 50.0) / 50.0)
                  + game.offense.get_player('TE', 1).speed / 2.0
                  + random_variability())))
        ]

        receiver = random_weighted_choice(weighted_choices)
    else:
        weighted_choices = [
            (game.offense.get_player('TE', 1), int((game.offense.get_player('TE', 1).catching * 1.5) + 1)),
            (game.offense.get_player('RB', 1), game.offense.get_player('RB', 1).catching),
            (game.offense.get_player('RB', 2), game.offense.get_player('RB', 2).catching),
            (game.offense.get_player('FB', 1), game.offense.get_player('FB', 1).catching)
        ]

        receiver = random_weighted_choice(weighted_choices)

        if receiver is game.offense.get_player('RB', 1):
            weighted_choices = [
                (game.offense.get_player('RB', 1),
                 game.offense.get_player('RB', 1).catching * 2
                 + game.offense.get_player('RB', 2).catching * 2 + 1),
                (game.offense.get_player('FB', 1),
                 int(game.offense.get_player('FB', 1).catching / 2 + 1))
            ]

            receiver = random_weighted_choice(weighted_choices)

            if receiver is game.offense.get_player('RB', 1):
                weighted_choices = [
                    (game.offense.get_player('RB', 1),
                     game.offense.get_player('RB', 1).catching * 2 + 1),
                    (game.offense.get_player('RB', 2),
                     game.offense.get_player('RB', 2).catching * 2 + 1)
                ]

                receiver = random_weighted_choice(weighted_choices)

    if pass_type is 4:
        weighted_choices = [
            (game.offense.get_player('RB', 1),
             game.offense.get_player('RB', 1) * 2 + 1),
            (game.offense.get_player('RB', 2),
             game.offense.get_player('RB', 2) * 2 + 1)
        ]

        receiver = random_weighted_choice(weighted_choices)

    break_stat = 50

    if receiver is game.offense.get_player('WR', 1):
        break_stat = receiver.acceleration

        if random_chance(105 - receiver.acceleration):
            check_down = True
    elif receiver is game.offense.get_player('WR', 2):
        break_stat = receiver.acceleration

        if random_chance(105 - receiver.acceleration):
            check_down = True
    elif receiver is game.offense.get_player('WR', 3):
        break_stat = receiver.acceleration

        if random_chance(105 - receiver.acceleration):
            check_down = True
    elif receiver is game.offense.get_player('TE', 1):
        break_stat = receiver.speed

        if random_chance(105 - receiver.speed / 1.5 + random_variability()):
            check_down = True
    elif receiver is game.offense.get_player('RB', 1) or game.offense.get_player('RB', 2):
        break_stat = receiver.agility

        if random_chance(105 - receiver.agility / 1.75 + random_variability()):
            check_down = True
    elif receiver is game.offense.get_player('FB', 1):
        break_stat = receiver.break_tackle

        if random_chance(105 - receiver.speed / 2.0 + random_variability()):
            check_down = True

    pass_mod = random.randint(-3, 3)

    if check_down:
        max_gain = (1.0
                    + (4.0 * (receiver.speed / 100.0))
                    - (0.25 * (game.defense.get_player('LCB', 1).tackling / 100.0))
                    - (0.25 * (game.defense.get_player('RCB', 1).tackling / 100.0))
                    - (0.25 * (game.defense.get_player('SS', 1).tackling / 100.0))
                    - (0.25 * (game.defense.get_player('FS', 1).tackling / 100.0))
                    + (1.0 * ((game.offense.gameplan.o_aggression - (100 - game.defense.gameplan.d_aggression)) / 100.0))
                    - (1.0 * (100 - game.defense.gameplan.d_run) / 100.0)
                    + pass_mod
                    + random_variability())

        while not random_chance(game.defense.get_player('SS', 1).tackling + 1)\
            and not random_chance(game.defense.get_player('FS', 1).tackling + 1)\
                and (max_gain < 200):
            max_gain += 0.25
    else:
        max_gain = (2.0
                    + (12.0 * (receiver.speed / 100.0))
                    - (0.5 * (game.defense.get_player('LCB', 1).tackling / 100.0))
                    - (0.5 * (game.defense.get_player('RCB', 1).tackling / 100.0))
                    - (0.5 * (game.defense.get_player('SS', 1).tackling / 100.0))
                    - (0.5 * (game.defense.get_player('FS', 1).tackling / 100.0))
                    + (1.0 * ((game.offense.gameplan.o_aggression - (100 - game.defense.gameplan.d_aggression)) / 100.0))
                    - (1.0 * (100 - game.defense.gameplan.d_run) / 100.0) + pass_mod + random_variability())

        while not random_chance(game.defense.get_player('SS', 1).tackling + 1)\
            and not random_chance(game.defense.get_player('FS', 1).tackling + 1)\
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
                    - (3.5 * (game.defense.get_player('LCB', 1).tackling / 100.0))
                    - (3.5 * (game.defense.get_player('RCB', 1).tackling / 100.0))
                    - (5.5 * (game.defense.get_player('SS', 1).tackling / 100.0))
                    - (5.5 * (game.defense.get_player('FS', 1).tackling / 100.0))
                    + (2.0 * game.play_mod)
                    + (0.25 * (game.offense.team_mod - game.defense.team_mod))
                    + (0.25 * (game.offense.gameplan.o_aggression / 100.0))
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
                      - (0.1 * game.defense.get_player('LCB', 1).tackling)
                      - (0.1 * game.defense.get_player('RCB', 1).tackling)
                      - (0.15 * game.defense.get_player('SS', 1).tackling)
                      - (0.15 * game.defense.get_player('FS', 1).tackling)
                      + (0.2 * (((100 - game.offense.gameplan.o_aggression)
                                 - game.defense.gameplan.d_aggression))) + random_variability())

        if fum_chance < 5:
            fum_chance = 5

        if int(random.uniform(0, int(fum_chance))) == 0:
            if (game.yard_line - gain) < 100:
                fumble = True

    fumble_forcer = game.defense.get_player('RDE', 1)

    if fumble:
        if ((gain < 10) and random_chance(95)) or random_chance(5):
            if game.defense.gameplan.d_style is '43':
                choices = [
                    (game.defense.get_player('LOLB', 1), game.defense.get_player('LOLB', 1).tackling + 1),
                    (game.defense.get_player('MLB', 1), game.defense.get_player('MLB', 1).tackling + 1),
                    (game.defense.get_player('ROLB', 1), game.defense.get_player('ROLB', 1).tackling + 1),
                    (game.defense.get_player('LCB', 1), game.defense.get_player('LCB', 1).tackling * 2
                     - game.defense.get_player('LCB', 1).coverage + 1),
                    (game.defense.get_player('LCB', 2), game.defense.get_player('LCB', 2).tackling * 2
                     - game.defense.get_player('LCB', 2).coverage + 1)
                ]
                fumble_forcer = random_weighted_choice(choices)
            else:
                choices = [
                    (game.defense.get_player('LOLB', 1), game.defense.get_player('LOLB', 1).tackling + 1),
                    (game.defense.get_player('LILB', 1), game.defense.get_player('LILB', 1).tackling + 1),
                    (game.defense.get_player('RILB', 1), game.defense.get_player('RILB', 1).tackling + 1),
                    (game.defense.get_player('ROLB', 1), game.defense.get_player('ROLB', 1).tackling + 1),
                    (game.defense.get_player('LCB', 1), game.defense.get_player('LCB', 1).tackling + 1),
                    (game.defense.get_player('RCB', 1), game.defense.get_player('RCB', 1).tackling + 1)
                ]
                fumble_forcer = random_weighted_choice(choices)
        else:
            choices = [
                (game.defense.get_player('LCB', 1), game.defense.get_player('LCB', 1).tackling + 1),
                (game.defense.get_player('RCB', 1), game.defense.get_player('RCB', 1).tackling + 1),
                (game.defense.get_player('SS', 1), game.defense.get_player('SS', 1).tackling + 1),
                (game.defense.get_player('FS', 1), game.defense.get_player('FS', 1).tackling + 1)
            ]
            fumble_forcer = random_weighted_choice(choices)

    return receiver.name, gain, td, fumble
