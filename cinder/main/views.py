from flask import render_template, session, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import *
from ..sampleDB import *
from datetime import *


def getMatches():
    """Returns all the matches of the user """
    #matchObjs = Match.objects(uid1=current_user.id).extend(Match.objects(uid2=current_user.id))
    #only call for login_required

    matchObjs = Match.objects[:2]
    matches = []
    for match in matchObjs:
        curProfile = None
        curFeedback = []
        if current_user.is_authenticated and match.uid1 == current_user.id:
            curProfile = match.uid2.profile
            for feedback in match.feedbacks:
                curFeedback.append(feedback.from_uid2)
        else: #assumes you are definitely part of this match
            curProfile = match.uid1.profile
            for feedback in match.feedbacks:
                curFeedback.append(feedback.from_uid1)
        matches.append({"match": match, "profile": curProfile, "feedbacks": curFeedback})
    return matches

@main.route('/', methods=["GET", "POST"])
def index():

    # p = Profile(first="Solomon", last="Wang", gender="M", age=23, photo="www.google.com", bio="haha")
    # u1 = User(cid=c, email="sw@gmail.com", profile=p, new_matches=False, interested_in="F",
    #         location="Los Angeles", answers=[])
    # u1.password = "password123" #needed to hash password
    # u1.save()
    # users = []
    # f = Feedback(date=datetime.today(), from_uid1="I LOVE YOU", from_uid2="I HATE YOU")
    # m = Match(uid1=User.objects[0], uid2=User.objects[1], match_date=datetime.today(), feedbacks=[f]).save()

    # for m in Match.objects:
    #     print(m.match_date)

    # print(users[0])

    # User.objects(email="sw@gmail.com").delete()

    if current_user.is_authenticated:
        return render_template("meet.html")
    else:
        return render_template("home.html")

@main.route('/your_feedback')
def give_feedback():
    matches = getMatches()
    return render_template('giveFeedback.html', matches=matches)

@main.route('/give_feedback')
def your_feedback():
    matches = getMatches()
    return render_template('yourFeedback.html', matches=matches)

@main.route('/profile')# @login_required
def profile():
    return render_template('profile.html')

@main.route('/match_profile')
def match_profile():
    #use login_required

    #matchObjs = Match.objects(uid1=current_user.id).extend(Match.objects(uid2=current_user.id))

    matchObjs = Match.objects[:2]
    print matchObjs
    matches = []
    for match in matchObjs:
        curProfile = None
        if current_user.is_authenticated and match.uid1 == current_user.id:
            curProfile = match.uid2.profile
        else: #assumes you are definitely part of this match
            curProfile = match.uid1.profile
        matches.append({"match": match, "profile": curProfile})
    return render_template('match_profile.html', matches=matches)



@main.route('/meet')
@login_required
def meet():
    return render_template("meet.html")

@main.route('/matches')
@login_required
def matches():
    matches = getMatches()
    return render_template("matches.html", matches=matches)
