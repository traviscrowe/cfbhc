__author__ = 'traviscrowe'
import random, pdb
from flask import request, Response
from flask_restful import Resource
from models.player import Player
from models.gameplan import Gameplan
from models.team import Team
from models.game import Game
from services.simulation import execute_run_play, completed_pass, run


class SimAPI(Resource):
    def post(self):
        req = request.get_json()

        home = req['home']
        away = req['away']

        home_players = [Player(**player) for player in home['players']]
        away_players = [Player(**player) for player in away['players']]

        home_gameplan = Gameplan(50, 50)
        away_gameplan = Gameplan(50, 50)

        home_team = Team(home_players, home_gameplan, home['team_mod'])
        away_team = Team(away_players, away_gameplan, away['team_mod'])

        game = Game(home_team, away_team, None, None, None)

        game = run(game)

        return game.log

class RunAPI(Resource):
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
            response = execute_run_play(1, 1, 10, random.randint(5, 80),
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


class PassAPI(Resource):
    def post(self):
        req = request.get_json()

        offense = req['offense']
        defense = req['defense']

        game = Game(offense, defense, None, None)

        off_players = [Player(**player) for player in offense['players']]
        def_players = [Player(**player) for player in defense['players']]

        off_gameplan = Gameplan(50, 50)
        def_gameplan = Gameplan(50, 50)

        off_team = Team(off_players, off_gameplan, offense['team_mod'])
        def_team = Team(def_players, def_gameplan, defense['team_mod'])

        results = []
        for x in range(0, random.randint(250, 350)):
            response = completed_pass(1, off_team, def_team, off_team.team_mod - def_team.team_mod, game)
            results.append(response)

        return results
