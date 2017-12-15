import json

from flask import render_template, session, redirect, url_for, jsonify, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import api
from ..models import User, Profile, Connection, Match, Feedback
from ..sampleDB import *
from .. import db
from random import randint
from datetime import *
import base64
import bson


#note all these routes must be prefixed with /api to be accessed
#ie localhost:5000/api/createProfile
defaultGender = 'M'
@api.route('/getUsers/', methods=["GET"])
@login_required
def getUsers():
    """This functions asks the backend for 15 unseen users with respect to the current user.

    Args: N/A

    Returns
        response (list(objects)):  Represents an array of users each with:
            * id (str): user's unique id
            * profile (dict): user's public information
    """

    users = users = User.objects(
        profile__gender=current_user.interested_in,
        id__ne=current_user.id,
        id__nin=current_user.cid.swiped).only('profile','id')[:15]
    resp = jsonify(result = users.to_json())
    return resp




@api.route('/swipe', methods=["POST"])
@login_required
def swipe():
    """This functions handles user swiping other users. A right swipe implies an intended match. A left swipe implies that the user is not interested.

    Args:
        id (str): user id for the user being swiped
        like (bool): indication of whether current user is interested in
                     the user with corresponding user id

    Returns:
        response (dict): A JSON that contains the swiped user's id and
        profile if the swipe action resulted in a match (bi-directional
        approval). An empty value otherwise:
          * id (str): user's unique id
          * profile (dict): user's public information
    """

    args = json.loads(request.data) #convert string to json
    # REST {u'id': u'5a31cb3c151a4b11ad8befbd', u'like': False}

    like = args['like']
    target_id = args['id']

    my_swiped = current_user.cid.swiped
    my_swiped.append(str(target_id))
    current_user.cid.swiped = my_swiped

    if not like or target_id == 'None':
        return

    targets = User.objects(id=target_id)
    target = targets[0]

    if like == 'True':
        my_liked = current_user.cid.liked
        my_liked.append(str(target_id))
        current_user.cid.liked = my_liked

        if str(current_user.id) in target.cid.liked:
            print "MATCHED YEAH!!!!"
            match = Match(uid1=current_user.id,
                          uid2=target_id,
                          match_date=datetime.today(),
                          confirmed1=False,
                          confirmed2=False,
                          feedbacks=[]).save()
            matchProfile = targets.only('profile','id').first()
            return jsonify(matchProfile.to_json())

    current_user.cid.save()

    return ('', 204) #empty response


@api.route('/proposeDate', methods=["POST"])
@login_required
def proposeDate():
    """Allows user to propose a date/time for a date with their Match

    Args:
        matchId (str): id of the match to set a date for
        date (str): string representing the timestamp to set the date for

    Returns:
        match (dict): object describing a match properties between two users:
            * uid1 (str): id of user 1 in match
            * uid2 (str): id of user 2 in match
            * match_date (dateTime): time stamp to schedule date
            * confirmed1 (bool): confirmation of user 1 ready to go on date
            * confirmed2 (bool): confirmation of user 2 ready to go on date
            * feedbacks (List(Feedback)): objects for bidirectional feedback
    """
    #{u'hour': u'17', u'mid': u'5a32ee672f78e6064295afa6', u'month': 12,
    #   u'year': 2017, u'date': 24, u'minute': u'00'}
    data = json.loads(request.data)
    year, month, day, hour, minute = map(int, [data['year'], data['month'], data['date'], data['hour'], data['minute']])
    date = datetime(year, month, day, hour, minute)
    matchId = bson.objectid.ObjectId(data['mid'])
    # matchUser = User.objects(id=matchId)[0]

    if len(Match.objects(uid1=current_user.id, uid2=matchId)) > 0:
        match = Match.objects(uid1=current_user.id, uid2=matchId)[0]
        match.confirmed1 = True
    else:
        match = Match.objects(uid2=current_user.id, uid1=matchId)[0]
        match.confirmed2 = True
    feedback = Feedback(date=date)
    match.feedbacks.append(feedback)
    match.save()
    return jsonify(match)


@api.route('/acceptDate', methods=["POST"])
@login_required
def acceptDate():
    """This function allows user to accept a Date proposed by the other.
    Args: matchId(id of match), accept(bool)"""
    #TODO: actually get matchId fro the request
    potentialPrompts = ["What did you like best about this date?",
            "What did you like least about this date?",
            "How can this person improve?"]
    matchId = Match.objects(uid1=current_user.id)[0].id
    accept = True

    match = Match.objects(id=matchId).first()
    feedback = match.feedbacks[-1]#assume last feedback is the most relevant one
    if accept:
        feedback.prompt = potentialPrompts[randint(0,len(potentialPrompts)-1)]
        match.confirmed1 = False
        match.confirmed2 = False
    else:
        match.confirmed1 = False
        match.confirmed2 = False
    match.save()
    return jsonify(match)

@api.route('/giveFeedback', methods=["POST"])
def giveFeedback():
    """This function allows users to submit feedback for one another.

    Args:
        matchId (int): user id for the user receiving feedback
        feedback (str): feedback message to be delivered to the recipient
                        with the corresponding matchId

    Returns:
        feedback (str): feedback that was delivered
    """
    #TODO: Implement this
    return jsonify(feedback1)

@api.route('/login', methods=["POST"])
def login():
    """This functions attempts to log the user in.

    Args:
        email (str): email of user attempting to login
        password (str): encrypted password of user attempting to login

    Returns:
        template (HTML): an html file that tells the browser what page to
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
        redirect_url (str): url to main page where user is redirected
    """

    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))




@api.route('/updateProfile', methods=["POST"])
def updateProfile():
    """This functions attempts to update the current user's profile

    Args:
        form -- dictionary: contains new information to update user with the
                   following properties:
            * first    -- String: first name
            * last     -- String: last name
            * gender   -- String: single char indicating gender ('M', 'F', 'O')
            * age      -- Int: age
            * bio      -- String: biography
            * location -- String: city, state zip-code
        files -- dictionary: contains new information about profile image
            * profile_image -- File: profile picture

    Returns:
        1. redirect_url -- String: url to profile page where user is redirected
    """


    form = request.form
    #print form

    profile = Profile(first=form['first'], last=form['last'], gender=form['gender'][0], age=form['age'],
                        bio=form['bio'], location=form['location']) #need photo

    file = request.files['profile_image']

    print file.filename


    if file.filename!="" and file.filename!="null":
        print "WHY!?"
        profile.photo.new_file()
        profile.photo.write(file)
        profile.photo.close()
    else:
        profile.photo = current_user.profile.photo

    answers = [form['q1'], form['q2'], form['q3'], form['q4'], form['q5']]

    current_user.profile = profile
    current_user.interested_in = form['interest'][0]
    current_user.answers = answers

    password = form['pswd']
    if password != "":
        current_user.password_hash = generate_password_hash(form['pswd'])

    current_user.save() #need to catch failed authenication

    return redirect(url_for('main.profile'))




@api.route('/createProfile', methods=["POST"])
def createProfile():
    """This functions attempts to create a new user profile.

    Args:
        form (dict): contains information to create a new user with
                   the following properties:
            * first    -- String: first name
            * last     -- String: last name
            * gender   -- String: single char indicating gender ('M', 'F', 'O')
            * age      -- Int: age
            * bio      -- String: biography
            * location -- String: city, state zip-code
        files (dict): contains new information about profile image
            * profile_image -- File: profile picture

    Returns:
        redirect_url (str): url to profile page where user is redirected
    """

    form = request.form
    profile = Profile(first=form['first'], last=form['last'], gender=form['gender'][0], age=form['age'],

                        bio=form['bio'], location=form['location']) #need photo
    file = request.files['profile_image']


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




@api.route('/getPicture', methods=['GET', 'POST'])
def getPicture():
    """This functions attempts get a users profile picture

    Args:
        uid (int): id of the user that client wants to retrive a photo of

    Returns:
        photo (str): url that client can use to access image
    """

    uid = ''
    if request.method == 'POST':
        args = json.loads(request.data)
        uid = args['uid'] #convert string to json
    else:
        uid = request.args['uid']

    if uid == 'None':
        return '/fakepath'
    if uid == 'curr':
        return current_user.profile.photo.read()
    else:
        photo = User.objects(id=uid).only('profile')[0].profile.photo.read()

    if request.method == 'POST':
        return base64.b64encode(photo)
    else:
        return photo


@api.route('/rateDate', methods=['POST'])
def rateDate():
    """This functions allows the current user to rate another that they have been on a date with

    Args:
        id (str): id of the user that rating is about
        date (str): string representing a time stamp for the day/time of date
        feedBackTextArea (str): feedback for the user

    Returns:
        redirect_url -- String: url to main page where user is redirected
    """
    target_id = request.args['id']
    date = request.args['date']
    date = datetime.strptime(date, '%Y-%m-%d').date()
    comment = request.form['feedBackTextArea']

    match = Match.objects(uid1=current_user.id, uid2=target_id)
    if len(match) == 0:
        match = Match.objects(uid2=current_user.id, uid1=target_id)[0]
        feedback = filter(lambda a: a.date.date()==date, match.feedbacks)
        feedback[0].from_uid2 = comment
        match.save()
    else:
        match = match[0]
        feedback = filter(lambda a: a.date.date()==date, match.feedbacks)
        feedback[0].from_uid1 = comment
        match.save()

    return redirect(url_for('main.give_feedback'))
