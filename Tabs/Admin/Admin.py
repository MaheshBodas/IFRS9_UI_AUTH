import dash_html_components as html
import dash_core_components as dcc
from tnp_dash_library.LayoutLibrary.ExpandableContent import ExpandableContent
from tnp_dash_library.LayoutLibrary.FixedContent import FixedContent
from tnp_dash_library.LayoutLibrary.TNPContent import TNPContent, TNPControl
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from tnp_dash_library.SimpleWidgetLibrary.TNPInputBox import TNPInputBox
from tnp_dash_library.Enums.TNPENums import LabelPosition
import dash_bootstrap_components as dbc


class Admin(TNPContent):

    def __init__(self, debug: bool = False):
        EXPANDABLE = False
        ID = 'admin-container'
        NAME = "User Setting and Administration"

        self.is_expandable = EXPANDABLE
        self.id = ID
        self.name = NAME
        self.controls = []
        self.debug = debug
        self.uploader = None

        if self.is_expandable:
            self.layout_helper = ExpandableContent(self.id, self.name, self.content_layout())
        else:
            self.layout_helper = FixedContent(self.id, self.name, self.content_layout())

        super().__init__(self.id)

    def content_layout(self, params=None):
        tab_style = {
            'borderBottom': '1px solid #d6d6d6',
            'padding': '6px',
            'fontWeight': 'bold',
            'borderRight': '1px solid #d6d6d6',
        }
        tab_selected_style = {
            'borderTop': '1px solid #d6d6d6',
            'borderBottom': '1px solid #d6d6d6',
            'backgroundColor': 'white',
            'color': '#599FE1',
            'padding': '6px',
            'borderRight': 'none',
        }

        password = TNPInputBox("password-user", "Password", "psw-1", LabelPosition.LEFT, "", 'password', 3, "",
                               self.debug, 0, "Update password", "", False)
        confirm_password = TNPInputBox("password-user-confirm", "Confirm Password", "psw-2", LabelPosition.LEFT, "",
                                      'password', 3, "",
                                      self.debug, 0, "Confirm password", "", False)
        submit_password = dbc.Button("Submit", id='submit-password-btn', className='btn_submit',
                                     style={'float': 'right', 'width': '80px'}, n_clicks=0)
        password_alert_red = dbc.Alert(id="password_alert_red", dismissable=True, is_open=False, color="danger",
                                       style={'font-size': '16px'})
        password_alert_green = dbc.Alert(id="password_alert_green", dismissable=True, is_open=False, color="success",
                                         style={'font-size': '16px'})

        container = html.Div([password.layout(), confirm_password.layout(),
                              password_alert_red, password_alert_green, submit_password],
                             style={'padding-top': '50px', 'padding-left': '25vh', 'padding-right': '25vh'})

        tabs = dcc.Tabs(
            [dcc.Tab(
                html.Div([container], className='admin-content'),
                label="Change Password", style=tab_style,
                selected_style=tab_selected_style),
                dcc.Tab(
                    html.Div([], className='admin-content'),
                    label="Add User", style=tab_style, selected_style=tab_selected_style, id='add-user-tab'),
                dcc.Tab(
                    html.Div([], className='admin-content'),
                    label="Remove User", style=tab_style, selected_style=tab_selected_style, id='remove-user-tab'),
                dcc.Tab(
                    html.Div([], className='admin-content'),
                    label="Change User Password", style=tab_style, selected_style=tab_selected_style,
                    id='change-user-tab')
            ], id=self.id + '-tabs')

        return html.Div([tabs], style={'height': '100%'}, id=self.id + '-container')

    def layout(self, params=None):
        return self.layout_helper.content_layout()

    def content_call_back(self, app):
        if self.is_expandable:
            self.layout_helper.content_call_back(app)

        @app.callback(Output('add-user-tab', 'children'),
                      Output('add-user-tab', 'disabled'),
                      Input('role', 'data'))
        def disable_add_user_tabs(role):
            if role == "admin":
                raise PreventUpdate
            return "", True

        @app.callback(Output('remove-user-tab', 'children'),
                      Output('remove-user-tab', 'disabled'),
                      Input('role', 'data'))
        def disable_add_user_tabs(role):
            if role == "admin":
                raise PreventUpdate
            return "", True

        @app.callback(Output('change-user-tab', 'children'),
                      Output('change-user-tab', 'disabled'),
                      Input('role', 'data'))
        def disable_add_user_tabs(role):
            if role == "admin":
                raise PreventUpdate
            return "", True

        @app.callback(Output('password_alert_green', 'children'),
                      Output('password_alert_green', 'is_open'),
                      Output('password_alert_red', 'children'),
                      Output('password_alert_red', 'is_open'),
                      Input('submit-password-btn', 'n_clicks'),
                      State({'type': 'password-user', 'index': 0}, 'value'),
                      State({'type': 'password-user-confirm', 'index': 0}, 'value'))
        def update_password(n_clicks, password, confirm_password):
            if n_clicks is None:
                raise PreventUpdate
            if n_clicks == 0:
                raise PreventUpdate

            if password == "":
                raise PreventUpdate

            if password != confirm_password:
               return "", False, "Passwords don't match", True

            # logic to update DB

            return "Password updated", True, "", False

    def register_control(self, control):
        if not issubclass(type(control), TNPControl):
            raise Exception("Only a 'TNPControl' can be registered in 'TNPContent'")
        self.controls.append(control)
