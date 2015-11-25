__author__ = 'traviscrowe'
from flask import Flask
from flask_restful import Api
from resources import player, recruit, team

app = Flask(__name__)
api = Api(app)

api.add_resource(recruit.RecruitListAPI, '/api/recruit')
api.add_resource(recruit.RecruitAPI, '/api/recruit/<int:id>')
api.add_resource(team.TeamListAPI, '/api/team')
api.add_resource(team.TeamAPI, '/api/team/<int:id>')
api.add_resource(player.PlayerListAPI, '/api/team/<int:id>/player')
api.add_resource(player.PlayerAPI, '/api/team/<int:id>/player/<int:p_id>')

if __name__ == '__main__':
    app.run(debug=False)
