from flask import Flask, url_for
import app.Dashboard as db
from tnp_dash_library.AppFactory import AppFactory

APPLICATION_NAME = "IFRS9 ECL Tool"
TAB_NAME = "TNP | IFRS9 ECL Tool"
USE_DATABASE = False
APPLICATION_PATH = "ifrs9"
DASHBOARD_TYPE = db.Dashboard
APPLICATION_ID = "IFRS9"
DEBUG = False
SERVER = Flask(__name__)
application = AppFactory.fromDashboardObject(APPLICATION_NAME, TAB_NAME, USE_DATABASE, APPLICATION_PATH,
                                             DASHBOARD_TYPE, APPLICATION_ID, DEBUG, "", USE_DATABASE, SERVER)
app = application.server

if __name__ == "__main__":
    application.run_application()
