from pymongo import MongoClient
from flask import Flask, render_template, flash, request, redirect
from flask_script import Manager
from flask_social import Social
import pprint

client = MongoClient('mongodb://admin:admin1@ds259255.mlab.com:59255/cinder')
db = client.cinder
collection = db.newcollection

app = Flask(__name__, template_folder="public", static_folder="src")
app.config['SECRET_KEY'] = "hard"

#Social Config
app.config['SOCIAL_FACEBOOK'] = {
    'consumer_key': '1751621538216434',
    'consumer_secret': '8052e75bdf98fe8fea0b1c8677544e71'
}
app.config['SECURITY_POST_LOGIN'] = '/profile'

manager = Manager(app)

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("home.html")

@app.route('/profile')
def profile():
    return "<h1>HELLO PROFILE</h1>"

if __name__ == "__main__":
    manager.run()
