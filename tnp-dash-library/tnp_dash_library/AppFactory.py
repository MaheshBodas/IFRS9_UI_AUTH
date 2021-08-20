from dash_bootstrap_components.themes import FLATLY
from tnp_dash_library.DashOOP.core import DashApp
from tnp_dash_library.TNPDashboard import TNPDashboard
from tnp_dash_library.Authentication.FlaskLoginAuth import FlaskLoginAuth
from flask import Flask
import os

DB_CONNECTION = "tnptools.sqlite"
JS = [{'src': "https://code.jquery.com/jquery-1.11.2.min.js"},
      {'src': "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"},
      {'src': "https://code.jquery.com/jquery-1.11.2.min.js"}]

CSS = [{'href': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css', 'rel': 'stylesheet'},
       {'href': '//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap.min.css', 'rel': 'stylesheet'}]


class AppFactory:
    """
        Application Factory

        Creates an instance of the dashboard
    """

    # Start changes for passing in flask server
    # def __init__(self, application_name: str, tab_name: str, authenticate: bool, application_base_path: str,
    def __init__(self, application_name: str, tab_name: str, authenticate: bool, application_base_path: str,
                 dashboard_type: type(TNPDashboard), app_id: str, debug: bool = False,
                 test_role: str = 'super', use_db: bool = True, server: Flask = None):

        if not issubclass(dashboard_type, TNPDashboard):
            raise Exception("Dashboard type should be a sub-class of 'TNPDashboard'")

        self._application_name = application_name
        self._tab_name = tab_name
        self._authenticate = authenticate
        # Start changes for flask_login
        self._server = server
        # End changes for flask_login
        self._dashboard_type = dashboard_type
        self._application_base_path = application_base_path

        if not str(application_base_path).endswith('/'):
            self._application_base_path = application_base_path + "/"

        # noinspection PyArgumentList
        dashboard = dashboard_type(application_name, tab_name, authenticate, DB_CONNECTION, application_base_path,
                                   test_role, debug)
        self.dashboard = dashboard

        # Start changes for flask_login authentication

        # Just a hack right now to see if Dash comes up
        self._app = DashApp(dashboard, querystrings=True, bootstrap=FLATLY, server=self._server,
                            # routes_pathname_prefix="/ifrs9/",
                            url_base_pathname='/' + self._application_base_path, external_scripts=JS,
                            external_stylesheets=CSS)
        # if not authenticate:
        #     self._server  = Flask(__name__)
        #     self._app = DashApp(dashboard, querystrings=True, bootstrap=FLATLY,
        #                         url_base_pathname='/' + self._application_base_path, external_scripts=JS,
        #                         external_stylesheets=CSS, server=self._server)
        # else:
        #     self._server = Flask(__name__)
        #
        #     self._server.config.update(
        #         SECRET_KEY=os.urandom(12),
        #     )
        #
        #     self._app = DashApp(dashboard, querystrings=True, bootstrap=FLATLY, server=self._server,
        #                         url_base_pathname='/' + self._application_base_path, external_scripts=JS,
        #                         external_stylesheets=CSS)
        #
        #
        #     if use_db:
        #         # noinspection SpellCheckingInspection
        #         FlaskLoginAuth(self._app, '/' + self._application_base_path, app_id, application_name, tab_name,
        #                        use_default_views=True,
        #                        users=DB_CONNECTION, test_role=test_role)
        #     else:
        #         FlaskLoginAuth(self._app, '/' + self._application_base_path, app_id, application_name, tab_name,
        #                        use_default_views=True,
        #                        users=False, test_role=test_role)
        # Just a test this whole thing will go away
        # End changes for flask_login authentication

    @classmethod
    def from_config(cls, config):
        # TODO: Understand why this doesn't work and fix
        dashboard = DashApp.from_config(config)
        return dashboard

    # Start changes for flask_login authentication
    # @classmethod
    # def fromDashboardObject(cls, application_name: str, tab_name: str, authenticate: bool, application_base_path: str,
    #                         dashboard_type: type(TNPDashboard), app_id: str, debug: bool = False,
    #                         test_role: str = 'super', use_db: bool = True ):
    #     return cls(application_name, tab_name, authenticate, application_base_path, dashboard_type, app_id, debug,
    #                test_role, use_db)

    @classmethod
    def fromDashboardObject(cls, application_name: str, tab_name: str, authenticate: bool,
                            application_base_path: str,dashboard_type: type(TNPDashboard), app_id: str,
                            debug: bool = False,test_role: str = 'super', use_db: bool = True, server: Flask = None):
        return cls(application_name, tab_name, authenticate, application_base_path, dashboard_type, app_id, debug,
                   test_role, use_db, server)

    # End changes for flask_login authentication

    # region PROPERTY: APPLICATION NAME
    @property
    def application_name(self):
        """Get application name"""
        return self._application_name

    # endregion

    # region PROPERTY: TAB NAME
    @property
    def tab_name(self):
        """Get website tab information"""
        return self._tab_name

    # endregion

    # region PROPERTY: AUTHENTICATE
    @property
    def authenticate(self):
        """Get authentication type"""
        return self._authenticate

    # endregion

    # region PROPERTY: DASHBOARD TEMPLATE
    @property
    def dashboard_type(self):
        """Get authentication type"""
        return self._dashboard_type

    @dashboard_type.setter
    def dashboard_type(self, val):
        """Set authentication type"""

        self._dashboard_type = val

    # endregion

    # region PROPERTY: APPLICATION
    @property
    def app(self):
        """Get application"""
        return self._app

    # endregion

    # region PROPERTY: SERVER
    @property
    def server(self):
        """Get server"""
        return self._server

    # endregion

    # region PROPERTY: APPLICATION BASE PTH
    @property
    def base_path(self):
        """Get server"""
        return self._application_base_path

    # endregion

    def run_application(self, port=None):
        if port is None:
            self.server.run()
        else:
            self.server.run(debug=True, port=port)
