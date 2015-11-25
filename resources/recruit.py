__author__ = 'traviscrowe'
import datetime, pdb, os, random, sys
from flask import Flask, Response, abort, request
from flask_restful import Resource, fields, reqparse

class RecruitAPI(Resource):
    def get(self, id):
        abort(404)

    def patch(self, id):
        abort(404)

    def delete(self, id):
        abort(404)

class RecruitListAPI(Resource):
    def post(self):
        skills = { }

        for i in range(2500):
            potential = generate_skill(1, 100)
            #skills[potential] = skill.generate_skill(1, potential)

        return { 'skills': potential }
