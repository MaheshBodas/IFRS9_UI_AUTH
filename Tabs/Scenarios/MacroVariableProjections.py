import dash_html_components as html
from tnp_dash_library.LayoutLibrary.ExpandableContent import ExpandableContent
from tnp_dash_library.LayoutLibrary.FixedContent import FixedContent
from tnp_dash_library.LayoutLibrary.TNPContent import TNPContent, TNPControl
import dash_core_components as dcc
import Utility.Unzip as uz
import json
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import Visualisations.ScenarioCharts as sc


class MacroProjectionChart(TNPContent):

    def __init__(self, debug: bool = False):
        EXPANDABLE = True
        ID = 'macro-config-container'
        NAME = "Macro Variable Projections"

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
        return dcc.Loading(html.Div([], id='macro-chart-container', hidden=True))

    def layout(self, params=None):
        return self.layout_helper.content_layout()

    def content_call_back(self, app):
        if self.is_expandable:
            self.layout_helper.content_call_back(app)

        @app.callback(Output('macro-chart-container', 'children'),
                      Output('macro-config-container-modal-body', 'children'),
                      Output('macro-chart-container', 'hidden'),
                      Input('submit-region', 'n_clicks'),
                      State('model_data', 'data'),
                      State({'type': 'scenario-dropdown', 'index': 0}, 'value'))
        def update_scenario_configuration(n_clicks, model_data, region):
            if n_clicks is None:
                raise PreventUpdate
            if n_clicks == 0:
                raise PreventUpdate

            uncompressed_data = json.loads(uz.json_unzip(model_data)['scenarios'])[region]
            fig1 = sc.plot_all_scenarios(uncompressed_data)
            title = fig1['layout']['title']['text']
            fig1['layout']['title']['text'] = title + ": " + str(region).upper()

            mv = dcc.Graph(figure=fig1, config={'displaylogo': False, 'editable': True},
                              id='ci-projection-plot-2', className='expandable_chart-half', style={"height": "72vh"})

            return mv, mv, False

        @app.callback(
            Output('macro-chart-container', 'children'),
            Output('macro-config-container-modal-body', 'children'),
            Output('macro-chart-container', 'hidden'),
            Input({'type': 'scenario-dropdown', 'index': 0}, 'value'))
        def clear(region):
            if region is not None:
                raise PreventUpdate
            return "", "", True

    def register_control(self, control):
        if not issubclass(type(control), TNPControl):
            raise Exception("Only a 'TNPControl' can be registered in 'TNPContent'")
        self.controls.append(control)
