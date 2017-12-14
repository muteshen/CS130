import json

from flask import render_template, session, redirect, url_for, jsonify, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import api
from ..models import User, Profile, Connection, Match, Feedback
from ..sampleDB import *
from .. import db
from random import random

#note all these routes must be prefixed with /api to be accessed
#ie localhost:5000/api/createProfile
defaultGender = 'M'
@api.route('/getUsers/', methods=["GET"])
@login_required
def getUsers():
    print current_user
    #TODO: use current_user to get preferred Gender
    #TODOV2: filter using connections.swiped to only get people you haven't swiped yet
    users = User.objects(profile__gender=defaultGender).only('profile','id')[:5]
    resp = jsonify(result = users.to_json())
    return resp

@api.route('/swipe', methods=["POST"])
@login_required
def swipe():
    """Parameters: {id: [other id], like: [bool]} //also unique
    """
    args = json.loads(request.data) #cuz he passed a string
    # REST {u'id': u'5a31cb3c151a4b11ad8befbd', u'like': False}

    print args['like']
    current_user.cid.swiped.append(args['id'])
    if not args['like']:
        return ('', 204) #empty response

    match = User.objects(id=args['id']
    print "Match profile: match.profile"
    if matchId in current_user.cid.liked_you:
        matchProfile = match.only('profile','id').first()
        return jsonify(matchProfile.to_json())
    else:
        match.cid.liked_you.append(current_user.id)
        return ('', 204) #empty response
        #connection


@api.route('/giveFeedback', methods=["POST"])
def giveFeedback():
    #Parameters
# Matchid: int //the id references to match database
# Feedback: string

    return feedback1

@api.route('/login', methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.objects(email=email)
    if user is None or len(user) == 0:
        return render_template('home.html')
    user = user[0]
    if user.verify_password(password):
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
    form = request.form
    print form


    profile = Profile(first=form['first'], last=form['last'], gender=form['gender'][0], age=form['age'],
                        bio=form['bio'], location=form['location']) #need photo

    file = request.files['profile_image']

    print file
    profile.photo.new_file()
    profile.photo.write(file)
    profile.photo.close()

    answers = [form['q1'], form['q2'], form['q3'], form['q4'], form['q5']]


    current_user.profile = profile
    current_user.interested_in = form['interest'][0]
    current_user.answers = answers

    password = form['pswd']
    print password
    if password != "":
        user.password_hash = generate_password_hash(form['pswd'])

    current_user.save() #need to catch failed authenication

    return redirect(url_for('main.profile'))




@api.route('/createProfile', methods=["POST"])
def createProfile():
    form = request.form
    print form
    profile = Profile(first=form['first'], last=form['last'], gender=form['gender'][0], age=form['age'],

                        bio=form['bio'], location=form['location']) #need photo
    file = request.files['profile_image']

    print file == ""
    print file.filename
    profile.photo.new_file()
    profile.photo.write(file)
    profile.photo.close()

    # photo = profile.photo.read()
    # print photo


    connection = Connection().save()
    answers = [form['q1'], form['q2'], form['q3'], form['q4'], form['q5']]
    user = User(cid=connection, email=form['email'], new_matches=False, profile=profile,
        interested_in=form['interest'][0], answers=answers)
    user.password_hash = generate_password_hash(form['pswd'])
    user.save() #need to catch failed authenication
    login_user(user, True)
    return redirect(url_for('main.profile'))

@api.route('/getPicture', methods=["GET"])
def getPicture():
    photo = current_user.profile.photo.read()
    return photo
