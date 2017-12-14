from flask import render_template, session, redirect, url_for, jsonify, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import api
from ..models import User, Profile, Connection, Match, Response, Feedback
from ..sampleDB import *
from .. import db
from random import random

#note all these routes must be prefixed with /api to be accessed
#ie localhost:5000/api/createProfile
defaultGender = 'M'
@api.route('/getUsers/', methods=["GET"])
def getUsers():
    print current_user
    #TODO: use current_user to get preferred Gender
    #TODOV2: filter using connections.swiped to only get people you haven't swiped yet
    users = User.objects(profile__gender=defaultGender).only('profile','id')[:5]
    resp = jsonify(result = users.to_json())
    return resp

@api.route('/swipe', methods=["POST"])
def swipe():
    #in is the other user's id and a bool of liked
    if random() < 0.5: #TODO: Check user connections to see if he was swiped back
        return ('', 204) #empty response
    else:
        users = User.objects(profile__gender=defaultGender).only('profile','id')[0]
        return jsonify(users.to_json())

@api.route('/myFeedback', methods=["GET"])
def myFeedback():
    #allFeedback = Feedback.objects(uid1=current_user.id).extend(Feedback.objects(uid2=current_user.id))
    return feedback1

@api.route('/giveFeedback', methods=["POST"])
def giveFeedback():
    return feedback1

@api.route('/myMatches', methods=["POST"])
def myMatches():
    #get list of matches from
    # Match.objects[0].only('match_date')
    # x.update(y)
    return jsonify(Match.objects[0])

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
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@api.route('/updateProfile', methods=["POST"])
def updateProfile():
    resp = jsonify(user1)
    return resp

@api.route('/createProfile', methods=["POST"])
def createProfile():
    form = request.form
    print form
    profile = Profile(first=form['first'], last=form['last'], gender=form['gender'][0], age=form['age'],
                        bio=form['bio'], location=form['location']) #need photo
    connection = Connection().save()
    answers = [form['q1'], form['q2'], form['q3'], form['q4'], form['q5']]
    user = User(cid=connection, email=form['email'], new_matches=False, profile=profile,
        interested_in=form['interest'][0], answers=answers)
    user.password_hash = generate_password_hash(form['pswd'])
    user.save() #need to catch failed authenication
    login_user(user, True)
    return redirect(url_for('main.profile'))
