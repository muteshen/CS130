from flask import render_template, session, redirect, url_for, jsonify, request
from flask_login import login_user
from . import api
from ..models import *
from ..sampleDB import *
from .. import db


#note all these routes must be prefixed with /api to be accessed
#ie localhost:5000/api/createProfile

@api.route('/getUsers/', methods=["GET"])
def getUsers():
    defaultGender = 'M'
    users = User.objects(profile__gender=defaultGender).only('profile','id')[:5]
    return jsonify(result = users.to_json())


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
    email = request.form['email']
    password = request.form['password']
    user = User.objects(email=email)
    if user is None or len(user) == 0:
        return render_template('home.html')
    user = user[0]
    if user.password_hash == password:#user.verify_password(password):
        login_user(user, True)
        return redirect(url_for('main.meet'))
    return render_template('home.html')
    #return True

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
