class Team(object):
    def __init__(self, players, gameplan, team_mod):
        self.players = players
        self.gameplan = gameplan
        self.run_blocking = calculate_run_blocking(players)
        self.pass_blocking = calculate_pass_blocking(players)
        self.team_mod = team_mod
        self.run_defense = calculate_run_defense(players, gameplan.d_style)
        self.pass_rush = calculate_pass_rush(players, gameplan.d_style)

    def get_player_at_dc_pos_and_depth(self, position, dc_position, depth):
        for player in self.players:
            if player.dc_position == dc_position and player.depth == depth:
                return player
        return None


def get_players_at_position(players, position):
    pos_players = []
    for player in players:
        if player.position == position:
            pos_players.append(player)
    return pos_players


def get_player_at_depth(players, position, depth):
    for player in get_players_at_position(players, position):
        if player.depth == depth:
            return player
    return None


def get_player_at_dc_pos_and_depth(players, position, dc_position, depth):
    for player in get_players_at_position(players, position):
        if player.dc_position == dc_position and player.depth == depth:
            return player
    return None


def calculate_run_blocking(players):
    lt = get_player_at_dc_pos_and_depth(players, 'OT', 'LT', 1)
    lg = get_player_at_dc_pos_and_depth(players, 'OG', 'LG', 1)
    c = get_player_at_depth(players, 'C', 1)
    rg = get_player_at_dc_pos_and_depth(players, 'OG', 'RG', 1)
    rt = get_player_at_dc_pos_and_depth(players, 'OT', 'RT', 1)

    run_blocking = (lt.run_blocking +
                    (lg.run_blocking * 1.1) +
                    (c.run_blocking * 1.05) +
                    (rg.run_blocking * 1.1) +
                    rt.run_blocking) / 5.25

    return run_blocking


def calculate_pass_blocking(players):
    lt = get_player_at_dc_pos_and_depth(players, 'OT', 'LT', 1)
    lg = get_player_at_dc_pos_and_depth(players, 'OG', 'LG', 1)
    c = get_player_at_depth(players, 'C', 1)
    rg = get_player_at_dc_pos_and_depth(players, 'OG', 'RG', 1)
    rt = get_player_at_dc_pos_and_depth(players, 'OT', 'RT', 1)

    pass_blocking = ((lt.pass_blocking * 1.1) +
                     lg.pass_blocking +
                     (c.pass_blocking * 1.05) +
                     rg.pass_blocking +
                     (rt.pass_blocking * 1.1) / 5.25)

    return pass_blocking


def calculate_run_defense(players, style):
    if style == '43':
        return calculate_43_run_defense(players)
    elif style == '34':
        return calculate_34_run_defense(players)


def calculate_pass_rush(players, style):
    if style == '43':
        return calculate_43_pass_rush(players)
    elif style == '34':
        return calculate_34_pass_rush(players)


def calculate_43_run_defense(players):
    lde = get_player_at_dc_pos_and_depth(players, 'DE', 'LDE', 1)
    ldt = get_player_at_dc_pos_and_depth(players, 'DT', 'LDT', 1)
    rdt = get_player_at_dc_pos_and_depth(players, 'DT', 'RDT', 1)
    rde = get_player_at_dc_pos_and_depth(players, 'DE', 'RDE', 1)

    run_defense = (lde.run_defense
                   + (ldt.run_defense * 1.2)
                   + (rdt.run_defense * 1.2)
                   + rde.run_defense) / 4.4

    return run_defense


def calculate_43_pass_rush(players):
    lde = get_player_at_dc_pos_and_depth(players, 'DE', 'LDE', 1)
    ldt = get_player_at_dc_pos_and_depth(players, 'DT', 'LDT', 1)
    rdt = get_player_at_dc_pos_and_depth(players, 'DT', 'RDT', 1)
    rde = get_player_at_dc_pos_and_depth(players, 'DE', 'RDE', 1)

    pass_rush = ((lde.pass_rush * 1.2)
                 + ldt.pass_rush
                 + rdt.pass_rush
                 + (rde.pass_rush * 1.2)) / 4.4

    return pass_rush


def calculate_34_run_defense(players):
    lde = get_player_at_dc_pos_and_depth(players, 'DE', 'LDE', 1)
    nt = get_player_at_dc_pos_and_depth(players, 'DT', 'NT', 1)
    rde = get_player_at_dc_pos_and_depth(players, 'DE', 'RDE', 1)

    run_defense = (lde.run_defense
                   + (nt.run_defense * 1.2)
                   + rde.run_defense) / 3.2

    return run_defense


def calculate_34_pass_rush(players):
    lde = get_player_at_dc_pos_and_depth(players, 'DE', 'LDE', 1)
    nt = get_player_at_dc_pos_and_depth(players, 'DT', 'NT', 1)
    rde = get_player_at_dc_pos_and_depth(players, 'DE', 'RDE', 1)

    pass_rush = ((lde.pass_rush * 1.2)
                 + nt.pass_rush
                 + (rde.pass_rush * 1.2)) / 3.2

    return pass_rush
