import random


def random_chance(percentage):
    return random.randrange(100) < percentage


def weighted_choice(weighted_choices):
    population = [val for val, cnt in weighted_choices for i in range(cnt)]
    return random.choice(population)
