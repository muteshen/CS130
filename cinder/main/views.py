from flask import render_template, session, redirect, url_for
from . import main
from .. import db
from ..models import *

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
    return sampleDB.profiles

@main.route('/api/Swipe', methods=["GET", "POST"])
def swipe():
    return sampleDB.isMatch

@main.route('/api/myFeedback', methods=["GET", "POST"])
def myFeedback():
    return sampleDB.feedback

@main.route('/api/myProfile', methods=["GET", "POST"])
def myProfile():
    return sampleDB.myprofile

@main.route('/api/login', methods=["GET", "POST"])
def login():
    return sampleDB.login

@main.route('/api/logout', methods=["GET", "POST"])
def logout():
    return sampleDB.Logout

@main.route('/api/updateProfile', methods=["GET", "POST"])
def updateProfile():
    return sampleDB.profile
