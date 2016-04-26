__author__ = 'traviscrowe'
from flask import Flask
from flask_restful import Api
from resources import player, recruit, team, sim

app = Flask(__name__)
api = Api(app)

api.add_resource(recruit.RecruitListAPI, '/api/recruit')
api.add_resource(recruit.RecruitAPI, '/api/recruit/<int:id>')
api.add_resource(team.TeamListAPI, '/api/team')
api.add_resource(team.TeamAPI, '/api/team/<int:id>')
api.add_resource(player.PlayerListAPI, '/api/team/<int:id>/player')
api.add_resource(player.PlayerAPI, '/api/team/<int:id>/player/<int:p_id>')
api.add_resource(sim.RunAPI, '/api/sim/run')
api.add_resource(sim.PassAPI, '/api/sim/pass')
api.add_resource(sim.SimAPI, '/api/sim/sim')

if __name__ == '__main__':
    app.run(debug=False)
