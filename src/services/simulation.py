__author__ = 'traviscrowe'
from enum import Enum
from services.rng import random_chance, random_weighted_choice, random_in_range, random_variability
from engine.clock import Clock
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


def run(game):
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
                    game.offense = game.defense;
                    game.defense = tmp;

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
            #TODO check overtime

    return game;


def determine_play(game):
    if determine_premature_fg(game):
        return execute_field_goal(game)
    elif determine_qb_kneel(game):
        return execute_qb_kneel(game)
    elif determine_run_play(game):
        return execute_run_play(game)
    else:
        if determine_qb_scramble(game):
            return execute_qb_scramble(game);
        else:
            return execute_pass_play(game)


def execute_fourth_down(game):
    desperation_time = 160 + (game.offense.gameplan.o_aggression / 2)

    if (game.offense.score < game.defense.score) and (game.time <= 900) and (time <= (desperation_time * ((game.defense.score - game.offense.score) / 8) + 1):
        if (game.offense.score) + 3 >= game.defense.score or time > (desperation_time (game.defense.score - game.offense.score - 3) / 9:
            if game.yard_line <= game.offense.gameplan.fg_try:
                return execute_field_goal(game)
        return determine_play(game)
    else:
        to_go_mod = game.yard_line
        go_chance = (100 - game.offense.gameplan.o_aggression) +
            (4 * (game.yard_line - 40)) +
            (to_go_mod * (game.to_go - 1)

        if game.yard_line <= game.offense.gameplan.fg_try:
            return execute_field_goal(game)
        else if game.yard_line <= 55 and random_in_range(-1, go_chance) <= 10 and go_chance <= 500 and game.to_go <= 6
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


def execute_field_goal(game):
    chance_mod = random_in_range(-10, 10)
    chance = ((100 * (game.offense.get_player('K', 1).kick_accuracy) / 100.0)
        + (60 * (game.offense.get_player('K', 1).kick_power) / 100.0)
        - (2.5 * game.yard_line)
        + (3 * chance_mod)
        + game.kick_mod
        + random_variability()

    if chance > 100:
        chance = 100

    if chance < 1 and random_chance(1):
        chance = 1

    if random_chance(chance):
        game.offense.score += 3

    game = Clock.spend_time(3, 7, 3, False)

    return game


def execute_punt(game):
    punter = game.offense.get_player('P', 1)
    returner = game.defense.get_player('KR', 1)
    punt_mod = random_in_range(-7, 7)
    max_punt = 15.0
        + (45.0 * (punter.kick_power) / 100.0)
        + game.kick_mod
        + random_variability()
    min_punt = 10.0
        + (35.0 * (punter.kick_power) / 100.0)
        + game.kick_mod
        + random_variability()
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
    else if punt_type == 2:
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
        defense.score = defense.score += 6
        game = Clock.spend_time(10, 15, 10, False)
        game = execute_turnover()
        if game.last_time < 1800 and game.time >= 1800 and (game.overtime is False or game.offense.score == game.defense.score):
            game = execute_kickoff(game)
    else:
        if punt_type == 3:
            game = Clock.spend_time(5, 15, 5, False)
        else:
            game = Clock.spend_time(3, 8, 3, False)
        game = execute_turnover()

    #TODO log play results with returns, touchdown, offense

    return game


def execute_kickoff(game):
    return game


def execute_onside_kickoff(game):
    return game


def execute_qb_kneel(game):
    return game


def determine_premature_fg(game):
    return game


def determine_qb_kneel(game):
    return (game.offense.score > game.defense.score) and
        (game.time <= (40 * (4 - game.down))) and
        (game.yard_line < 99) and
        (game.time <= 120)


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
    elif game.time <= Clock.calculate_seconds(4, 13, 0):
        if game.yard_line <= 50:
            mod -= 10
        else:
            third_apply = False
            mod += 10

    if (game.time >= Clock.calculate_seconds(3, 0, 0)) and (game.time <= Clock.calculate_seconds(2, 10, 0)):
        if game.yard_line <= 50:
            mod -= 10
        else:
            third_apply = false
            mod += 10

    if ((game.down == 3) and third_apply is True) or game.down = 4:
        intensity = -3
        if down == 4:
            intensity = -4

        mod += intensity * (game.to_go - 5)

    return mod


def execute_run_play(run_type, down, togo, yard_line, rb1, rb2, fb, te, offense, defense, play_mod, run_mod):
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

    if gain >= 7 or random_chance(break_stat / 4.0 + random.random()) and random_chance(rusher.speed / 1.5):
        max_additional = ((22.0 * (rusher.speed / 100.0))
                          - (2.5 * (defense.get_player('LCB', 1).tackling / 100.0))
                          - (2.5 * (defense.get_player('RCB', 1).tackling / 100.0))
                          - (3.5 * (defense.get_player('SS', 1).tackling / 100.0))
                          - (3.5 * (defense.get_player('FS', 1).tackling / 100.0))
                          + (2.0 * play_mod)
                          + (0.5 * run_mod)
                          + (0.25 * (offense.team_mod - defense.team_mod))
                          + random.random())

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
                              + random.random())

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
                          + random.random())
        else:
            fum_chance = ((1.8 * rusher.concentration)
                          - (0.1 * defense.run_defense)
                          - (0.1 * defense.get_player('LOLB', 1).tackling)
                          - (0.1 * defense.get_player('LILB', 1).tackling)
                          - (0.1 * defense.get_player('RILB', 1).tackling)
                          - (0.1 * defense.get_player('ROLB', 1).tackling)
                          + (0.2 * (((100 - offense.gameplan.o_aggression)
                                     - defense.gameplan.d_aggression)))
                          + random.random())

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


def pass_play(pass_type, offense, defense, play_mod, game, sack_mod):
    pass_type_mod = 0

    if pass_type is 3:
        # if total run plays - 3 >= total pass plays in this game by the offense
        pass_type_mod = 5
        # else pass_type_mod = -5
    if pass_type is 4:
        pass_type_mod = 10

    if random_chance(get_completion_chance(game, play_mod) + pass_type_mod):
        return completed_pass(pass_type, offense, defense, play_mod, game)
    else:
        incompletion_chance = 85.0 + (game.offense.pass_blocking / 5.0) \
            - (1.5 * (100 - game.defense.gameplan.d_run) / 100.0) \
            + (2.0 * play_mod) \
            + (0.5 * (offense.team_mod - defense.team_mod)) \
            + ((100.0 - offense.gameplan.o_aggression) / 100.0) \
            - (defense.gameplan.d_aggression / 100.0) \
            + random.random()

        choices = [
            (1, int(get_sack_chance(game), sack_mod)),
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


def completed_pass(pass_type, offense, defense, play_mod, game):
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
        gain = random.randint(int(offense.get_player('QB', 1).throw_power / 2 + pass_mod),
                              int(offense.get_player('QB', 1).throw_power / 2 + max_gain + pass_mod))

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
               + random.random())

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
             + random.random()))),
            (offense.get_player('WR', 2),
            int((offense.get_player('WR', 2).catching * 3.05
             + offense.get_player('WR', 2).acceleration
             - ((defense.get_player('RCB', 1).coverage - 50.0) / 25.0)
             + random.random()))),
            (offense.get_player('WR', 3),
            int((offense.get_player('WR', 3).catching * 3.05
             + offense.get_player('WR', 3).acceleration
             - ((defense.get_player('SS', 1).coverage - 50.0) / 50.0)
             - ((defense.get_player('FS', 1).coverage - 50.0) / 50.0)
             + random.random()))),
            (offense.get_player('TE', 1),
            int((offense.get_player('TE', 1).catching * 3.05
             - lb_coverage / 50.0
             - ((offense.gameplan.o_aggression - 50.0) / 50.0)
             + offense.get_player('TE', 1).speed / 2.0
             + random.random())))
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

        if random_chance(105 - receiver.speed / 1.5 + random.random()):
            check_down = True
    elif receiver is offense.get_player('RB', 1) or offense.get_player('RB', 2):
        break_stat = receiver.agility

        if random_chance(105 - receiver.agility / 1.75 + random.random()):
            check_down = True
    elif receiver is offense.get_player('FB', 1):
        break_stat = receiver.break_tackle

        if random_chance(105 - receiver.speed / 2.0 + random.random()):
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
            - (1.0 * (100 - defense.gameplan.d_run) / 100.0) + pass_mod + random.random())

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
            - (1.0 * (100 - defense.gameplan.d_run) / 100.0) + pass_mod + random.random())

        while not random_chance(defense.get_player('SS', 1).tackling + 1)\
            and not random_chance(defense.get_player('FS', 1).tackling + 1)\
                and (max_gain < 200):
            max_gain += 0.5

    if max_gain < 0:
        max_gain = 0

    gain += random.randint(0, int(max_gain))

    break_free = (break_stat / 2.5 + random.randint(-5, 5) + random.random())

    if check_down:
        break_free = (break_stat / 5.0 + random.randint(-5, 5) + random.random())

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
            + random.random())

        if max_gain < 1:
            max_gain = 1

        gain += random.randint(0, int(max_gain))

        if random_chance(receiver.speed / 1.5 + random.random()):
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
                       - defense.gameplan.d_aggression))) + random.random())

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


def get_completion_chance(game, play_mod):
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
        + chance_mod + random.random())

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


def get_sack_chance(game):
    chance_mod = random.randint(-3, 3)

    chance = (0.0
        - (20.0 * (game.offense.pass_blocking / 100.0))
        - (0.75 * (game.offense.get_player('QB', 1).speed / 100.0))
        - (0.75 * (game.offense.get_player('QB', 1).throw_power / 100.0))
        - (1.0 * (game.offense.get_player('FB', 1).pass_protect / 100.0))
        - (0.75 * (game.offense.get_player('TE', 1).pass_protect / 100.0))
        + chance_mod + random.random())

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


def get_interception_chance():
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
        + chance_mod + random.random())

        if chance < 0.0:
            chance = 0.0

        return chance
