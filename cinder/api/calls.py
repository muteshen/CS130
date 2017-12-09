from flask import render_template, session, redirect, url_for, jsonify
from . import api
from ..models import *
from ..sampleDB import *
from .. import db

#note all these routes must be prefixed with /api to be accessed
#ie localhost:5000/api/createProfile
@api.route('/getUsers/<uid>', methods=["GET"])
def getUsers(uid):
    return profiles

@api.route('/swipe', methods=["POST"])
def swipe():
    return isMatch

@api.route('/myFeedback', methods=["POST"])
def myFeedback():
    return feedback1

@api.route('/myProfile', methods=["POST"])
def myProfile():
    resp = jsonify(user1)
    return resp

@api.route('/login', methods=["POST"])
def login():
    return True

@api.route('/logout', methods=["POST"])
def logout():
    return True

@api.route('/updateProfile', methods=["POST"])
def updateProfile():
    resp = jsonify(user1)
    return resp

@api.route('/createProfile', methods=["POST"])
def createProfile():
    resp = jsonify(user1)
    return resp
