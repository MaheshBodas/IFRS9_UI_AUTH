import dash_html_components as html
from tnp_dash_library.LayoutLibrary.ExpandableContent import ExpandableContent
from tnp_dash_library.LayoutLibrary.FixedContent import FixedContent
from tnp_dash_library.LayoutLibrary.TNPContent import TNPContent, TNPControl
from Styling import TNPColour
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
from dash.exceptions import PreventUpdate
import Tabs.Scenarios.ScenarioTable_helper as sh


class ScenarioTable(TNPContent):

    def __init__(self, debug: bool = False):
        EXPANDABLE = True
        ID = 'scenario-projections-container'
        NAME = "Scenario Projections"

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
        theme = TNPColour.TNPColour()

        monthly = html.Div([], id='monthly-scenario-table-container', style={"height": "15vh"})
        annual = html.Div([], id='annual-scenario-table-container', style={"height": "15vh"}, hidden=True)
        monthly_modal = html.Div([], id='monthly2-scenario-table-container', style={"height": '72vh'}, hidden=True)
        annual_modal = html.Div([], id='annual2-scenario-table-container', style={"height": '72vh'}, hidden=True)

        radio_items = dbc.FormGroup(
            [
                dbc.RadioItems(
                    options=[
                        {"label": "Monthly", "value": "Monthly"},
                        {"label": "Annual", "value": "Annual"},
                    ],
                    value="Monthly",
                    id="time-step-choice",
                    inline=True,
                ),
            ]
        )
        layout = dbc.Row(radio_items, style={'padding-right': '15px'})
        return dcc.Loading(html.Div([layout, monthly, annual, monthly_modal, annual_modal],
                                    id='scenario-table-container', hidden=True))

    def layout(self, params=None):
        return self.layout_helper.content_layout()

    def content_call_back(self, app):
        if self.is_expandable:
            self.layout_helper.content_call_back(app)

        @app.callback(Output('monthly-scenario-table-container', 'children'),
                      Output('annual-scenario-table-container', 'children'),
                      Output('scenario-projections-container-modal-body', 'children'),
                      Output('scenario-table-container', 'hidden'),
                      Input('submit-region', 'n_clicks'),
                      State('model_data', 'data'),
                      State({'type': 'scenario-dropdown', 'index': 0}, 'value'))
        def update_scenario_configuration(n_clicks, model_data, region):
            if n_clicks is None:
                raise PreventUpdate
            if n_clicks == 0:
                raise PreventUpdate

            a1, m1, modal = sh.get_scenario_tables(model_data, region)

            return m1, a1, modal, False

        @app.callback(Output('monthly-scenario-table-container', 'hidden'),
                      Output('annual-scenario-table-container', 'hidden'),
                      Output('monthly2-scenario-table-container', 'hidden'),
                      Output('annual2-scenario-table-container', 'hidden'),
                      [Input('time-step-choice', 'value')])
        def force_button_click(value):
            if value == "Annual":
                return True, False, True, False
            return False, True, False, True

        @app.callback(
            Output('monthly-scenario-table-container', 'children'),
            Output('annual-scenario-table-container', 'children'),
            Output('scenario-projections-container-modal-body', 'children'),
            Output('scenario-table-container', 'hidden'),
            Input({'type': 'scenario-dropdown', 'index': 0}, 'value'))
        def clear(region):
            if region is not None:
                raise PreventUpdate
            return "", "", "", True

    def register_control(self, control):
        if not issubclass(type(control), TNPControl):
            raise Exception("Only a 'TNPControl' can be registered in 'TNPContent'")
        self.controls.append(control)
