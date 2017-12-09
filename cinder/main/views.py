from flask import render_template, session, redirect, url_for, jsonify
from flask_login import login_required
from . import main
from .. import db
from ..models import *
from ..sampleDB import *
from datetime import *

@main.route('/', methods=["GET", "POST"])
def index():
    c = Connection(liked_you = [], swiped = []).save()
    p = Profile(first="Solomon", last="Wang", gender="M", birthday="1995-09-25", photo="www.google.com", bio="haha")
    u1 = User(cid=c, email="sw@gmail.com", profile=p, new_matches=False, interested_in="F",
            location="Los Angeles", answers=[])
    u1.password = "password123" #needed to hash password
    u1.save()
    users = []
    for user in User.objects:
        users += [user]
    f = Feedback(uid1=users[0], uid2=users[1], response=[]).save()
    m = Match(uid1=users[0], uid2=users[1], match_date=datetime.today(), feedback_id=f).save()

    # for m in Match.objects:
    #     print(m.match_date)

    print(users[0])

    print("Testing Here")
    return render_template("home.html")

@main.route('/give_feedback')
def give_feedback():
    return render_template('giveFeedback.html')

@main.route('/your_feedback')
def your_feedback():
    return render_template('yourFeedback.html')


@main.route('/meet')
def meet():
    return render_template('meet.html')

@main.route('/profile')# @login_required
def profile():
    return render_template('profile.html')
