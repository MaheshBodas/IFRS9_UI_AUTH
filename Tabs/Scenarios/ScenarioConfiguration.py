import dash_html_components as html
from dash.dependencies import Input, Output, State
from tnp_dash_library.LayoutLibrary.ExpandableContent import ExpandableContent
from tnp_dash_library.LayoutLibrary.FixedContent import FixedContent
from tnp_dash_library.LayoutLibrary.TNPContent import TNPContent, TNPControl
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
from Styling import TNPColour
from datetime import datetime
from SidePanel.SidePanelContent import side_panel_call_backs
import Tabs.Scenarios.ScenarioConfiguration_helper as sh


class ScenarioConfiguration(TNPContent):

    def __init__(self, debug: bool = False):
        EXPANDABLE = True
        ID = 'scenario-config-container'
        NAME = "Scenario Configuration"

        self.is_expandable = EXPANDABLE
        self.id = ID
        self.name = NAME
        self.controls = []
        self.debug = debug
        self.uploader = None
        self.drop_down = None

        if self.is_expandable:
            self.layout_helper = ExpandableContent(self.id, self.name, self.content_layout())
        else:
            self.layout_helper = FixedContent(self.id, self.name, self.content_layout())

        super().__init__(self.id)

    def content_layout(self, params=None):
        return html.Div([dcc.Loading(html.Div(id='scenario-input-holder', hidden=True))])

    def layout(self, params=None):
        return self.layout_helper.content_layout()

    def content_call_back(self, app):
        if self.is_expandable:
            self.layout_helper.content_call_back(app)

        # HACK - to get side panel call backs registered
        side_panel_call_backs(app)

        @app.callback(Output('scenario-input-holder', 'hidden'),
                      Output('scenario-config-container-modal-body', 'children'),
                      Output('scenario-input-holder', 'children'),
                      Input('submit-region', 'n_clicks'),
                      State('config-data', 'data'),
                      State({'type': 'scenario-dropdown', 'index': 0}, 'value'))
        def update_scenario_configuration(n_clicks, config_data, region):
            if n_clicks is None:
                raise PreventUpdate
            if n_clicks == 0:
                raise PreventUpdate

            modal_input, ui_input = sh.get_scenario_specification_inputs(region, config_data, False)
            return False, modal_input, ui_input

        @app.callback(
            Output('scenario-input-holder', 'hidden'),
            Output('scenario-config-container-modal-body', 'children'),
            Output('scenario-input-holder', 'children'),
            Input({'type': 'scenario-dropdown', 'index': 0}, 'value'))
        def clear(region):
            if region is not None:
                raise PreventUpdate
            return "", "", True

    def register_control(self, control):
        if not issubclass(type(control), TNPControl):
            raise Exception("Only a 'TNPControl' can be registered in 'TNPContent'")
        self.controls.append(control)
