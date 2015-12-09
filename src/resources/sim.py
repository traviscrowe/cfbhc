__author__ = 'traviscrowe'
import random
from flask import request, Response
from flask_restful import Resource
from models.player import Player
from models.gameplan import Gameplan
from models.team import Team
from services.simulation import run_play, pass_play


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
        touchdowns = 0
        fumbles = 0
        forcers = []
        for x in range(0, random.randint(250, 350)):
            response = run_play(1, 1, 10, random.randint(5, 80),
                            off_team.get_player('RB', 1),
                            off_team.get_player('RB', 2),
                            off_team.get_player('FB', 1),
                            off_team.get_player('TE', 1),
                            off_team,
                            def_team,
                            off_team.team_mod - def_team.team_mod,
                            off_team.run_blocking - def_team.run_defense)
            results.append(int(response[0]))
            touchdowns += response[1]
            fumbles += 1 if response[2] else 0
            if response[3] is not None:
                forcers.append(response[3])

        return Response('Troy White: '
                        + str(len(results))
                        + ' for ' + str(sum(results))
                        + ' yards, '
                        + str(touchdowns)
                        + ' TD for an average of '
                        + str(sum(results) / float(len(results))) + '. Long: '
                        + str(max(results))
                        + ' Fumbles: '
                        + str(fumbles)
                        + ' [%s]' % ', '.join(map(str, forcers)))
