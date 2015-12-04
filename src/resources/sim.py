__author__ = 'traviscrowe'
import random
from flask import request, Response
from flask_restful import Resource
from models.player import Player
from models.gameplan import Gameplan
from models.team import Team, get_player_at_dc_pos_and_depth
from services.simulation import rush


class SimAPI(Resource):
    def post(self):
        req = request.get_json()

        offense = req['offense']
        defense = req['defense']

        off_players = [Player(**player) for player in offense['players']]
        def_players = [Player(**player) for player in defense['players']]

        off_gameplan = Gameplan(50, 50)
        def_gameplan = Gameplan(50, 50)

        off_team = Team(off_players, off_gameplan, offense['team_mod'])
        def_team = Team(def_players, def_gameplan, defense['team_mod'])

        results = []
        for x in range(0, 25):
            results.append(rush(1, 1, 10, 80,
                            get_player_at_dc_pos_and_depth(off_players, "RB", "RB", 1),
                            get_player_at_dc_pos_and_depth(off_players, "RB", "RB", 2),
                            get_player_at_dc_pos_and_depth(off_players, "FB", "FB", 1),
                            get_player_at_dc_pos_and_depth(off_players, "TE", "TE", 1),
                            off_team,
                            def_team,
                            off_team.team_mod - def_team.team_mod,
                            off_team.run_blocking - def_team.run_defense))

        return Response("Troy White: "
                        + str(len(results))
                        + " for " + str(sum(results))
                        + " yards for an average of "
                        + str(sum(results) / float(len(results))) + ". Long: "
                        + str(max(results)))
