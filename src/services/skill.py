import random

def generate_skill(min, max, min_mean_mod):
    val = 0
    while val < min or val > max:
        val = round(random.gauss((max - min) / min_mean_mod, (max - min) / 5))
    return val

def generate_skill_pair(min, max):
    skill = 0
    potential = 0
    pair = { }

    potential = generate_skill(min, max, 2)
    skill = generate_skill(min, potential, 4)

    pair['skill'] = skill
    pair['potential'] = potential

    return pair

def generate_weighted_value(kvps):
    for kvp in kvps:
        weighted_list += kvp['item'] * kvp['weight']
    random.choice(weighted_list)
