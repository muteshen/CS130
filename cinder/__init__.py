from pymongo import MongoClient
from flask import Flask, render_template, flash, request, redirect
from flask_script import Manager
from flask_mongoengine import MongoEngine
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from config import config

bootstrap = Bootstrap()
db = MongoEngine()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.index'

def create_app(config_name):
    app = Flask(__name__, template_folder="public", static_folder="src")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
