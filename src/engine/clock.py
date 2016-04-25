from service.rng import random_in_range

class Clock:
    def calculate_seconds(quarter, minutes, seconds):
        return 3600 - ((900 * (quarter - 1)) + (60 * minutes) + seconds)

    def time_modifier(game):
        mod = 0

        if game.overtime:
            mod = -10
        else if game.offense.score > game.defense.score:
            mod = 40 + random_in_range(1, 7)
            if game.time <= calculate_seconds(4, 5, 0):
                mod += 3
            if game.time <= calculate_seconds(4, 10, 0):
                mod += 6
        else if game.defense.score > game.offense.score:
            mod = random_in_range(-10, -1)
            if game.time <= calculate_seconds(4, 5, 0):
                mod -= 6
            if game.time <= calculate_seconds(4, 10, 0):
                mod -= 12
        else if game.time <= calculate_seconds(4, 13, 0):
            if game.yard_line <= 50:
                mod -= 10
            else:
                mod +=10

        if game.time >= calculate_seconds(3, 0, 0) and game.time <= calculate_seconds(2, 10, 0):
            if yard_line <= 50:
                mod -= 10
            else
                mod = 10

        #TODO if touchdown == true then mod = -25
        if mod < -25:
            mod = -25

        if mod > 20:
            mod = 20

        return mod


def spend_time(game, min_time, max_time, true_min, modify):
    time_used = random_in_range(min_time, max_time) + time_modifier(game)

    if modify:
        if time_used < true_min:
            time_used = true_min + random_in_range(0, 3)
        if time_used > 40:
            time_used = 40
    else:
        time_used = random_in_range(min_time, max_time)

    new_time = game.time - time_used
    if game.overtime is False:
        if game.time > 2700 and new_time <= 2700:
            time_used = game.time - 2700
        else if game.time > 1800 and new_time <= 1800:
            time_used = game.time - 1800
        else if game.time > 900 and new_time <= 900:
            time_used = game.time - 900
        else:
            if game.time > (1800 + 120) and new_time <= (1800 + 120):
                time_used = time - (1800 + 120)
                if time_used < 8:
                    time_used = random_in_range(5, 7)
            if game.time > 120 and new_time <= 120:
                time_used = game.time - 120
                if time_used < 8:
                    time_used = random_in_range(5, 7)
    else:
        if game.time > 120 and new_time <= 120:
            time_used = game.time - 120
            if time.used < 8:
                time_used = random_in_range(5, 7)

    game.time = game.time - time_used

    return game
