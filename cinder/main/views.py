from flask import render_template, session, redirect, url_for, jsonify
from . import main
from .. import db
from ..models import *
from ..sampleDB import *

@main.route('/', methods=["GET", "POST"])
def index():
    # for user in User.objects:
    #     print(user.email)
    return render_template("home.html")

@main.route('/profile')
def profile():
    return "<h1>HELLO PROFILE</h1>"

@main.route('/api/getUsers/<uid>', methods=["GET"])
def getUsers(uid):
    return profiles

@main.route('/api/Swipe', methods=["POST"])
def swipe():
    return isMatch

@main.route('/api/myFeedback', methods=["POST"])
def myFeedback():
    return feedback1

@main.route('/api/myProfile', methods=["POST"])
def myProfile():
    resp = jsonify(user1)
    return resp

@main.route('/api/login', methods=["POST"])
def login():
    return True

@main.route('/api/logout', methods=["POST"])
def logout():
    return True

@main.route('/api/updateProfile', methods=["POST"])
def updateProfile():
    resp = jsonify(user1)
    return resp

@main.route('/api/createProfile', methods=["POST"])
def createProfile():
    resp = jsonify(user1)
    return resp
