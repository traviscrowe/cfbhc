import random

def random_chance(percentage):
    return random.randrange(100) < percentage


def random_weighted_choice(weighted_choices):
    population = [val for val, cnt in weighted_choices for i in range(cnt)]
    return random.choice(population)


def random_in_range(start, end):
    if start >= end:
        return start

    n_range = end - start + 1
    n_fraction = n_range * random.random()
    n_random = fraction * start

    return n_random


def random_variability():
    r = random() * 2
    r = r - 1.0

    return r
