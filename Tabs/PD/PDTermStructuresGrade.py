import dash_html_components as html
import dash_core_components as dcc
from tnp_dash_library.LayoutLibrary.ExpandableContent import ExpandableContent
from tnp_dash_library.LayoutLibrary.FixedContent import FixedContent
from tnp_dash_library.LayoutLibrary.TNPContent import TNPContent, TNPControl
import Utility.Unzip as uz
import json
import Visualisations.PDCharts as pdc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from tnp_dash_library.SimpleWidgetLibrary.TNPDropdown import TNPDropdown
from tnp_dash_library.Enums.TNPENums import LabelPosition


class PDTermStructuresGradeContent(TNPContent):

    def __init__(self, debug: bool = False):
        EXPANDABLE = True
        ID = 'pd-ts-grade-container'
        NAME = "Probability of Default Term Structures by Grade"

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

        drop_down = TNPDropdown('pd-ts-grade', 'Grade', 'pit000', None, LabelPosition.LEFT, 3,
                                None, self.debug, 0, "Select Model Grade")
        chart = dcc.Loading(html.Div(id='pd-ts-grade-chart-child-container'))

        return dcc.Loading(html.Div([drop_down.layout(), chart], id='pd-ts-grade-chart-container',
                                    hidden=True))

    def layout(self, params=None):
        return self.layout_helper.content_layout()

    def content_call_back(self, app):
        if self.is_expandable:
            self.layout_helper.content_call_back(app)

        @app.callback(Output('pd-ts-grade-chart-child-container', 'children'),
                      Output('pd-ts-grade-container-modal-body', 'children'),
                      Output('pd-ts-grade-chart-container', 'hidden'),
                      Input('submit-model', 'n_clicks'),
                      State('model_data', 'data'),
                      State({'type': 'model-dropdown', 'index': 0}, 'value'),
                      State({'type': 'pd-ts-grade', 'index': 0}, 'value'))
        def update_transition_matrix(n_clicks, model_data, model, grade):
            if n_clicks is None:
                raise PreventUpdate
            if n_clicks == 0:
                raise PreventUpdate
            model_grade = grade['value']
            dist, dist2 = get_PiT_PD_chart_data(model, model_data, model_grade)
            return dist2, dist, False

        @app.callback(
            Output('pd-ts-grade-chart-child-container', 'children'),
            Output('pd-ts-grade-container-modal-body', 'children'),
            Output('pd-ts-grade-chart-container', 'hidden'),
            Input({'type': 'model-dropdown', 'index': 0}, 'value'))
        def clear(model):
            if model is not None:
                raise PreventUpdate
            return "", "", True

        @app.callback(
            Output('pd-ts-grade-chart-child-container', 'children'),
            Output('pd-ts-grade-container-modal-body', 'children'),
            Output('pd-ts-grade-chart-container', 'hidden'),
            Input({'type': 'pd-ts-grade', 'index': 0}, 'value'),
            State('model_data', 'data'),
            State({'type': 'model-dropdown', 'index': 0}, 'value'),
            State('pd-transition-matrix-chart-container', 'hidden'),
            prevent_initial_call = True)
        def update_transition_matrix(grade, model_data, model, hidden):
            if hidden:
                raise PreventUpdate
            model_grade = grade
            dist, dist2 = get_PiT_PD_chart_data(model, model_data, model_grade)
            return dist2, dist, False

        @app.callback(Output({'type': 'pd-ts-grade', 'index': 0}, 'options'),
                      Output({'type': 'pd-ts-grade', 'index': 0}, 'value'),
                      Input({'type': 'model-dropdown', 'index': 0}, 'value'),
                      State('model_data', 'data'))
        def update_drop_down_values(model, model_data):
            if model_data is None:
                raise PreventUpdate

            if model is None:
                return {}

            model_data = json.loads(uz.json_unzip(model_data)['pd_data'])[model]["ratings"]
            options = [{'label': k, 'value': k} for k in model_data if k != "Default"]

            return options, options[0]

    def register_control(self, control):
        if not issubclass(type(control), TNPControl):
            raise Exception("Only a 'TNPControl' can be registered in 'TNPContent'")
        self.controls.append(control)


def get_PiT_PD_chart_data(model, model_data, grade):
    uncompressed_data = json.loads(uz.json_unzip(model_data)['pd_data'])[model]
    fig1 = pdc.plotGradeTermStructures(uncompressed_data, grade)
    title = fig1['layout']['title']['text']
    fig1['layout']['title']['text'] = title + ": " + str(model).upper().replace("_", " ")
    dist = dcc.Graph(figure=fig1, config={'displaylogo': False, 'editable': True},
                     className='expandable_chart-half', style={"height": "72vh"})
    dist2 = dcc.Graph(figure=fig1, config={'displaylogo': False, 'editable': True},
                     className='expandable_chart-half', style={"height": "26vh"})
    return dist, dist2
