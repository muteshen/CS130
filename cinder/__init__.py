from pymongo import MongoClient
from flask import Flask, render_template, flash, request, redirect
from flask_script import Manager
from flask_mongoengine import MongoEngine
from flask_bootstrap import Bootstrap

from config import config

bootstrap = Bootstrap()
db = MongoEngine()

def create_app(config_name):
    app = Flask(__name__, template_folder="public", static_folder="src")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
