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
        if current_user.is_authenticated:
            _id = match.uid1.id
            curProfile = match.uid1.profile

            matches.append({"match": match, "profile": curProfile, "mate_id": _id})

    matchObjs = Match.objects(uid1=current_user.id)
    for match in matchObjs:
        curProfile = None
        if current_user.is_authenticated:
            _id = match.uid2.id
            curProfile = match.uid2.profile
            matches.append({"match": match, "profile": curProfile, "mate_id": _id})



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
        return redirect(url_for("main.meet"))
    else:
        return render_template("home.html")

@main.route('/your_feedback')
def your_feedback():

    all_feedbacks = []
    matches = Match.objects(uid1=current_user.id)
    for match in matches:
        target = match.uid2
        for feedback in match.feedbacks:
            if feedback.from_uid2 and feedback.from_uid1:
                all_feedbacks.append({"name": target.profile.first + " " + target.profile.last, 
                                      "date": feedback.date, 
                                      "prompt": feedback.prompt,
                                      "feedback": feedback.from_uid2,
                                      "mate_id": match.uid2.id})

    matches = Match.objects(uid2=current_user.id)
    for match in matches:
        target = match.uid1
        for feedback in match.feedbacks:
            if feedback.from_uid1 and feedback.from_uid2:
                all_feedbacks.append({"name": target.profile.first + " " + target.profile.last, 
                                      "date": feedback.date, 
                                      "prompt": feedback.prompt,
                                      "feedback": feedback.from_uid1,
                                      "mate_id": match.uid1.id})

    return render_template('yourFeedback.html', feedbacks=all_feedbacks)

@main.route('/give_feedback')
def give_feedback():
    all_dates = []
    

    matches = Match.objects(uid1=current_user.id, feedbacks__not__size=0)
    for match in matches:
        target = match.uid2
        for feedback in match.feedbacks:
            if feedback.date < datetime.now() and (not feedback.from_uid1) and feedback.prompt:
                all_dates.append({"name": target.profile.first + " " + target.profile.last,
                                  "date": feedback.date.date(),
                                  "prompt": feedback.prompt,
                                  "mate_id": target.id,
                                  })


    matches = Match.objects(uid2=current_user.id, feedbacks__not__size=0)
    for match in matches:
        target = match.uid1
        for feedback in match.feedbacks:
            if feedback.date < datetime.now() and (not feedback.from_uid2) and feedback.prompt:
                all_dates.append({"name": target.profile.first + " " + target.profile.last,
                                  "date": feedback.date.date(),
                                  "prompt": feedback.prompt,
                                  "mate_id": target.id,
                                  "bio": target.profile.bio
                                  })

    return render_template('giveFeedback.html', dates=all_dates)

@main.route('/profile')# @login_required
def profile():
    return render_template('profile.html')

@main.route('/match_profile')
@login_required
def match_profile():
    #use login_required

    target_id = request.args['uid']


    # matchObjs = Match.objects(uid1=current_user.id, uid2=target_id).extend(Match.objects(uid2=current_user.id, uid1=target_id))
    # matchObjs = matchObjs[0]

    target_id = request.args['uid']


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
    #here or on frontend note when other user has selected a date
    #must give new date if reject old one
    #show the give feedback button when your feedback is empty and date is after today
    #check if date is after today for the give feedback button
    return render_template("matches.html", matches=matches)
