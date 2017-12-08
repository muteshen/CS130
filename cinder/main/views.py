from flask import render_template, session, redirect, url_for, jsonify
from . import main
from .. import db
from ..models import *
from ..sampleDB import *

@main.route('/', methods=["GET", "POST"])
def index():
    for user in User.objects:
        print(user.email)
    return render_template("home.html")

@main.route('/profile')
def profile():
    return "<h1>HELLO PROFILE</h1>"
