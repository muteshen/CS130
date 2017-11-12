from pymongo import MongoClient
from flask import Flask, render_template, flash, request, redirect
from flask_script import Manager
import pprint

client = MongoClient('mongodb://admin:admin1@ds259255.mlab.com:59255/cinder')
db = client.cinder
collection = db.newcollection

app = Flask(__name__)
app.config['SECRET_KEY'] = "hard"
manager = Manager(app)

@app.route('/', methods=["GET", "POST"])
def index():
    return "<h1>HELLO WORLD</h1>"

if __name__ == "__main__":
    manager.run()
