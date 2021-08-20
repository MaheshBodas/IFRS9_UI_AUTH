# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask, url_for
from flask_login import LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path

db = SQLAlchemy()
login_manager = LoginManager()
server = Flask(__name__, static_folder='base/static')


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    for module_name in ('base', 'home'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def create_flask_server(config):
    # server = Flask(__name__, static_folder='base/static')
    server.config.from_object(config)
    register_extensions(server)
    register_blueprints(server)
    configure_database(server)
    flask_server = server
    for view_func in flask_server.view_functions:
        if view_func.startswith('/ifrs9') and not "dash" in view_func:
            flask_server.view_functions[view_func] = login_required(flask_server.view_functions[view_func])
    return flask_server
