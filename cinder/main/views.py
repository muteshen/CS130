from flask import render_template, session, redirect, url_for, jsonify, request
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
    matchObjs = Match.objects(uid2=current_user.id)
    matches = []
    for match in matchObjs:
        curProfile = None
        curFeedback = []
        if current_user.is_authenticated:
            _id = match.uid1.id
            curProfile = match.uid1.profile
            for feedback in match.feedbacks:
                curFeedback.append(feedback.from_uid1)
        matches.append({"match": match, "profile": curProfile, "feedbacks": curFeedback, "mate_id": _id})


    matchObjs = Match.objects(uid1=current_user.id)
    for match in matchObjs:
        curProfile = None
        curFeedback = []
        if current_user.is_authenticated:
            _id = match.uid2.id
            curProfile = match.uid2.profile
            for feedback in match.feedbacks:
                curFeedback.append(feedback.from_uid2)
        matches.append({"match": match, "profile": curProfile, "feedbacks": curFeedback, "mate_id": _id})

    return matches

def getTargets():
    users = User.objects(profile__gender=current_user.interested_in, id__ne=current_user.id,
                     id__nin=current_user.cid.swiped).only('profile','id')

    if len(users) == 0:
        name = "No more candidates"
        age = ''
        bio = "Check back later!"
        location = "The place in your heart"
        _id = 'None'
    else:
        u = users[0]
        name = u.profile.first + " " + u.profile.last
        age = u.profile.age
        bio = u.profile.bio
        location = u.profile.location
        _id = str(u.id)
    targets = {"name": name, "age": age, "bio":bio, "location": location, "id":_id}
    return targets



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
    return render_template('yourFeedback.html', matches=matches)

@main.route('/give_feedback')
def your_feedback():
    matches = getMatches()
    return render_template('giveFeedback.html', matches=matches)

@main.route('/profile')# @login_required
def profile():
    return render_template('profile.html')

@main.route('/match_profile')
@login_required
def match_profile():
    #use login_required

    target_id = request.args['uid']
    print target_id

    # matchObjs = Match.objects(uid1=current_user.id, uid2=target_id).extend(Match.objects(uid2=current_user.id, uid1=target_id))
    # matchObjs = matchObjs[0]

    target_id = request.args['uid']
    print target_id

    if len(Match.objects(uid1=current_user.id, uid2=target_id)) >0:
        target = Match.objects(uid1=current_user.id, uid2=target_id)[0].uid2
    else:
        target = Match.objects(uid2=current_user.id, uid1=target_id)[0].uid1

    profile = target.profile
    matches = {"user": target, "profile":profile}


    return render_template('match_profile.html', target=matches)


@main.route('/meet')
@login_required
def meet():
    target = getTargets()
    return render_template("meet.html", target=target)

@main.route('/matches')
@login_required
def matches():
    matches = getMatches()
    return render_template("matches.html", matches=matches)
