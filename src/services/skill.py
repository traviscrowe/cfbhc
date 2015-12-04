import random


def generate_skill(min_val, max_val, min_mean_mod):
    val = 0
    while val < min_val or val > max_val:
        val = round(random.gauss((max_val - min_val) / min_mean_mod, (max_val - min_val) / 5))
    return val


def generate_skill_pair(min_val, max_val):
    skill = 0
    potential = 0
    pair = {}

    potential = generate_skill(min_val, max_val, 2)
    skill = generate_skill(min_val, potential, 4)

    pair['skill'] = skill
    pair['potential'] = potential

    return pair


def generate_weighted_value(kvps):
    weighted_list = {}
    for kvp in kvps:
        weighted_list += kvp['item'] * kvp['weight']
    return random.choice(weighted_list)
