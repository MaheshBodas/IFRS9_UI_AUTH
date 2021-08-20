import dash_bootstrap_components as dbc
from dash_oop_components import DashComponent, DashComponentTabs
from tnp_dash_library.CompositeWidgetLibrary.NavigationBars import NavigationBars
from abc import abstractmethod
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import sqlite3
import socket
from dash import callback_context
from dash.exceptions import PreventUpdate
from tnp_dash_library.CompositeWidgetLibrary.ControlPanel import ControlPanel
import dash_html_components as html
from datetime import datetime


class TNPDashboard(DashComponent):

    @abstractmethod
    def __init__(self, application_name, page_tab_name, tabs, authenticate, db_connection,
                 url_base_path, debug=False, test_role: str = 'super', control_panel=None):
        self._navigation_bar = NavigationBars(application_name, authenticate, url_base_path).layout()
        self._application_name = application_name
        self._tabs = tabs
        self._authenticate = authenticate
        self._logged_on = False
        self._class_name = "shown"
        self._db_connection = db_connection
        self._control_panel = control_panel
        self._test_role = test_role
        self._debug = debug

        if not isinstance(control_panel, ControlPanel) and control_panel is not None:
            raise Exception("Object of type 'ControlPanel' can only be added as a Control panel to the dashboard")

        super().__init__(title=page_tab_name, name=application_name)

    def layout(self, params=None):

        if self._control_panel is not None:
            control_panel = self._control_panel.layout()
        else:
            control_panel = html.Div(hidden=True)

        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y, %H:%M")
        return dbc.Container([
            dcc.Store(id="app-run", data=False, storage_type='session'),
            dcc.Store(id="user-name", data=None, storage_type='session'),
            dcc.Store(id="role", data=self._test_role, storage_type='session'),
            dcc.Store(id="organisation", data=None, storage_type='session'),
            dcc.Store(id="login-time", data=date_time, storage_type='session'),
            dcc.Store(id="debug", data=self._debug, storage_type='session'),

            dbc.Row([
                dbc.Col([
                    self._navigation_bar
                ])
            ], id='nav-bar-row'),

            html.Div(control_panel, id='app_control_panel'),

            dbc.Row([
                dbc.Col([
                    self.querystring(params)(DashComponentTabs)(id="tabs", tabs=self._tabs,
                                                                params=params, component=self,
                                                                single_tab_querystrings=True),
                ], id="app_content")
            ], id='app-content-row')
        ], fluid=True)

    def register_callbacks(self, app):
        for t in self._tabs:
            for c in t.content:
                if c is not None:
                    c.content_call_back(app)
                    for w in c.controls:
                        w.store_value(app)

            if t.headline is not None:
                for h in t.headline.list_of_metrics:
                    h.component_callbacks(app)

        if self._control_panel is not None:
            self._control_panel.content_call_back(app)

        if self._authenticate:
            @app.callback(
                Output('user-name', 'data'),
                Output('role', 'data'),
                Output('organisation', 'data'),
                Output('log-in-details', 'children'),
                Input('app-run', 'data'),
                State('user-name', 'data'),
                State('role', 'data'),
                State('organisation', 'data'),
                State('login-time', 'data')
            )
            def set_user_data(_input, username, role, organisation, login_time):
                if not callback_context:
                    raise PreventUpdate

                if username != "" and username is not None:
                    logged_in_details = html.P([html.B("Username: "), username,
                                                html.Br(),
                                                html.B("Organisation: "), organisation,
                                                html.Br(),
                                                html.B("Role: "), role,
                                                html.Br(),
                                                html.B("Login Time: "), login_time], className='log-in-details')
                else:
                    try:

                        hostname = socket.gethostname()
                        ip_address = socket.gethostbyname(hostname)
                        task = (hostname, ip_address)
                        user_info = self.__get_user_connected_user_info_from_db(task)
                        self.__delete_current_user_from_db(task)
                        username, role, organisation = user_info[0]
                    except:
                        username = "Error"
                        organisation = "Error"
                        role = "Error"
                        login_time = "Error"
                    finally:
                        logged_in_details = html.P([html.B("Username: "), username,
                                                    html.Br(),
                                                    html.B("Organisation: "), organisation,
                                                    html.Br(),
                                                    html.B("Role: "), role,
                                                    html.Br(),
                                                    html.B("Login Time: "), login_time], className='log-in-details')

                return username, role, organisation, logged_in_details
        else:
            @app.callback(
                Output('user-name', 'data'),
                Output('role', 'data'),
                Output('organisation', 'data'),
                Output('log-in-details', 'children'),
                Input('app-run', 'data'),
                State('role', 'data'),
                State('login-time', 'data')
            )
            def set_user_data(_input, role, login_time):
                if not callback_context:
                    raise PreventUpdate

                logged_in_details = html.P([html.B("Username: "), "admin",
                                            html.Br(),
                                            html.B("Organisation: "), "TNP",
                                            html.Br(),
                                            html.B("Role: "), "admin",
                                            html.Br(),
                                            html.B("Login Time: "), login_time], className='log-in-details')

                return "admin", "admin", "TNP", logged_in_details

    def __get_user_connected_user_info_from_db(self, task):
        conn = sqlite3.connect(self._db_connection)
        sql = 'SELECT USERS.USERNAME, ROLE, ORGANISATION ' \
              'FROM LOGGED_ON ' \
              'LEFT JOIN USERS ' \
              'ON LOGGED_ON.USERNAME = USERS.USERNAME ' \
              'WHERE HOSTNAME=? AND IP_ADDRESS = ?'
        cursor = conn.execute(sql, task)
        return cursor.fetchall()

    def __delete_current_user_from_db(self, task):
        sql = 'DELETE FROM LOGGED_ON WHERE HOSTNAME=? AND IP_ADDRESS = ?'
        conn = sqlite3.connect(self._db_connection)
        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit()
