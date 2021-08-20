import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_oop_components import DashComponent
from tnp_dash_library.SimpleWidgetLibrary.LogoutForm import LogoutForm

TNP_LOGO = 'assets/TNP-Logo_no background.png'


class NavigationBars(DashComponent):

    def __init__(self, application_name, authenticate, url_base_path):
        self._application_name = application_name
        self.authenticate = authenticate
        self._url_base_path = url_base_path
        super().__init__(title=application_name, name='nav-bar')

    # region METHOD: DEFINE STANDARD NAVIGATION BAR
    def layout(self, params=None):

        if self.authenticate:
            login_out_form = LogoutForm().layout()
            logout_class = "shown"
        else:
            login_out_form = html.Div()
            logout_class = "hidden"

        return dbc.Navbar(
            [
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=TNP_LOGO, height="40px", style={'margin-left': '100px'}), width=3),
                        dbc.Col(html.Div(self._application_name, className="ml-5 app-title")),
                        html.Div(id='log-in-details', className="col-2", style={'font-size': '10px'}),
                        html.Div(login_out_form, id="logout-container", className=logout_class),
                    ],
                    align="center",
                    no_gutters=True,
                    id="navbar-container"
                ),

            ],
            color="light",
            dark=False,
            sticky="top",

        )

    # endregion
