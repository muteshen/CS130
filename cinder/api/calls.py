import json

from flask import render_template, session, redirect, url_for, jsonify, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import api
from ..models import User, Profile, Connection, Match, Feedback
from ..sampleDB import *
from .. import db
from random import random
from datetime import *


#note all these routes must be prefixed with /api to be accessed
#ie localhost:5000/api/createProfile
defaultGender = 'M'
@api.route('/getUsers/', methods=["GET"])
@login_required
def getUsers():
    """This functions asks the backend for 5 unseen users with respect to the current user.

    Args: N/A

    Returns:
        JSON.  Represents an array of users each with::
        
            1. id -- String: user's unique id
            2. profile -- JSON: user's public information
    """

    print current_user
    #TODO: use current_user to get preferred Gender
    #TODOV2: filter using connections.swiped to only get people you haven't swiped yet
    users = User.objects(profile__gender=defaultGender).only('profile','id')[:5]
    print users[0].first
    resp = jsonify(result = users.to_json())
    return resp




@api.route('/swipe', methods=["POST"])
@login_required
def swipe():
    """This functions handles user swiping other users. A right swipe implies an
    intended match. A left swipe implies that the user is not interested.

    Args:
        1. id -- String: user id for the user being swiped
        2. like -- Bool: indication of whether current user is interested in
                         the user with corresponding user id

    Returns:
        JSON.  A JSON that contains the swiped user's id and profile if the swipe
        action resulted in a match (bi-directional approval). An empty value
        otherwise::

          1. id -- String: user's unique id
          2. profile -- JSON: user's public information
    """

    args = request.args #cuz he passed a string
    # REST {u'id': u'5a31cb3c151a4b11ad8befbd', u'like': False}


    like = args['like']
    target_id = args['id']



    if not like or target_id == 'None':
        return redirect(url_for('main.meet'))

    target = User.objects(id=target_id)[0]

    if like == 'True':
        my_liked = current_user.cid.liked
        my_liked.append(str(target_id))
        current_user.cid.liked = my_liked

        if str(current_user.id) in target.cid.liked:
            print "MATCHED YEAH!!!!"
            match = Match(uid1=current_user.id, uid2=target_id, match_date=datetime.today(),
                          confirmed1=False, confirmed2=False, feedbacks=[]).save()

    my_swiped = current_user.cid.swiped
    my_swiped.append(str(target_id))
    current_user.cid.swiped = my_swiped

    current_user.cid.save()

    return redirect(url_for('main.meet'))

    # match = User.objects(id=args['id'])
    # print "Match profile: match.profile"
    # if matchId in current_user.cid.liked_you:
    #     matchProfile = match.only('profile','id').first()
    #     return jsonify(matchProfile.to_json())
    # else:
    #     match.cid.liked_you.append(current_user.id)
    #     return ('', 204) #empty response
    #     #connection


@api.route('/giveFeedback', methods=["POST"])
def giveFeedback():
    """This function allows users to submit feedback for one another.

    Args:
        1. matchId -- Int: user id for the user receiving feedback
        2. feedback -- String: feedback message to be delivered to the recipient
                               with the corresponding matchId

    Returns:
        1. feedback -- String: Feedback that was delivered
    """

    return feedback1

@api.route('/login', methods=["POST"])
def login():
    """This functions attempts to log the user in.

    Args:
        1. email -- String: email of user attempting to login
        2. password -- String: encrypted password of user attempting to login

    Returns:
        1. template -- HTML: an html file that tells the browser what page to
                             display. If login was successful, this will be the
                             meet page. If login was unsuccessful, this will be
                             the home page.
    """

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
    """This functions attempts to log the user out.

    Args: N/A

    Returns:
        1. redirect_url -- String: url to main page where user is redirected
    """

    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@api.route('/updateProfile', methods=["POST"])
def updateProfile():
    """This functions attempts to update the current user's profile

    Args:
        1. form -- dictionary: contains new information to update user with the
                   following properties:
            a. first    -- String: first name
            b. last     -- String: last name
            c. gender   -- String: single char indicating gender ('M', 'F', 'O')
            d. age      -- Int: age
            e. bio      -- String: biography
            f. location -- String: city, state zip-code
        2. files -- dictionary: contains new information about profile image
            a. profile_image -- File: profile picture

    Returns:
        1. redirect_url -- String: url to profile page where user is redirected
    """

    form = request.form
    print form

    profile = Profile(first=form['first'], last=form['last'], gender=form['gender'][0], age=form['age'],
                        bio=form['bio'], location=form['location']) #need photo

    file = request.files['profile_image']

    if file.filename!="" and file.filename!="null":
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
        current_user.password_hash = generate_password_hash(form['pswd'])

    current_user.save() #need to catch failed authenication

    return redirect(url_for('main.profile'))




@api.route('/createProfile', methods=["POST"])
def createProfile():
    """This functions attempts to create a new user profile

    Args:
        1. form -- dictionary: contains information to create a new user with
                   the following properties:
            a. first    -- String: first name
            b. last     -- String: last name
            c. gender   -- String: single char indicating gender ('M', 'F', 'O')
            d. age      -- Int: age
            e. bio      -- String: biography
            f. location -- String: city, state zip-code
        2. files -- dictionary: contains new information about profile image
            a. profile_image -- File: profile picture

    Returns:
        1. redirect_url -- String: url to profile page where user is redirected
    """

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
    """This functions attempts get a users profile picture

    Args:
        1. uid -- Int: id of the user that client wants to retrive a photo of

    Returns:
        1. photo -- String: url that client can use to access image
    """

    uid = request.args['uid']
    print uid
    if uid == 'None':
        return '/fakepath'
    if uid == 'curr':
        return current_user.profile.photo.read()
    else:
        photo = User.objects(id=uid).only('profile')[0].profile.photo.read()
    return photo
