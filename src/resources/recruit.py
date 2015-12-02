__author__ = 'traviscrowe'
import datetime, pdb, os, random, sys, json
from flask import Flask, Response, abort, request, jsonify
from flask_restful import Resource, fields, reqparse
from services.playerclass import entire_class
from services.skill import generate_skill_pair

class RecruitAPI(Resource):
    def get(self, id):
        abort(404)

    def patch(self, id):
        abort(404)

    def delete(self, id):
        abort(404)

parser = reqparse.RequestParser()
parser.add_argument('generateClass', bool, location='args')
parser.add_argument('classSize', int, location='args')

class RecruitListAPI(Resource):
    def post(self):
        args = parser.parse_args()
        entire_class = args['generateClass']
        class_size = args['classSize']

        if entire_class == True:
            return entire_class(class_size)

        skills = [ ]

        for i in range(500):
            skill = generate_skill_pair(1, 100)
            skills.append(skill)

        return Response(json.dumps(skills),  mimetype='application/json')
