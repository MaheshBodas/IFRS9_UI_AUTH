# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# from flask_migrate import Migrate
from os import environ
from sys import exit
from decouple import config
import logging

from config import config_dict
from app import create_flask_server, db
from tnp_dash_library.AppFactory import AppFactory
import app.Dashboard as dashboard

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    
    # Load the configuration using the default values 
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

# Flask server
server = create_flask_server(app_config)

APPLICATION_NAME = "IFRS9 ECL Tool"
TAB_NAME = "TNP | IFRS9 ECL Tool"
USE_DATABASE = False
APPLICATION_PATH = "ifrs9"
DASHBOARD_TYPE = dashboard.Dashboard
APPLICATION_ID = "IFRS9"
DEBUG = False
application = AppFactory.fromDashboardObject(APPLICATION_NAME, TAB_NAME, USE_DATABASE, APPLICATION_PATH,
                                             DASHBOARD_TYPE, APPLICATION_ID, DEBUG, "", USE_DATABASE, server)
# Migrate(server, db)

if DEBUG:
    server.logger.info('DEBUG       = ' + str(DEBUG))
    server.logger.info('Environment = ' + get_config_mode)
    server.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)

if __name__ == "__main__":
    server.run()
