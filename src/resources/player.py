__author__ = 'traviscrowe'
import datetime, pdb, os
from flask import Flask, Response, abort, request
from flask_restful import Resource, fields, reqparse

class PlayerAPI(Resource):
    def get(self, id):
        abort(404)

    def patch(self, id):
        abort(404)

    def delete(self, id):
        abort(404)

class PlayerListAPI(Resource):
    def post(self):
        abort(404)
