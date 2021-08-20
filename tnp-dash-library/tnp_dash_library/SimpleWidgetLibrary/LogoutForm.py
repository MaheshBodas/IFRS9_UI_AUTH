from dash_oop_components import DashComponent
import dash_bootstrap_components as dbc
import dash_html_components as html


class LogoutForm(DashComponent):
    def __init__(self):
        super().__init__(name='log-out')

    def layout(self, params=None):
        return dbc.Form(
            [
                html.A("Log out", href='/logout', style={'margin-right': '20px'})
            ],
            inline=True,
            id='logout-form'
        )
