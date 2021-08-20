import dash_html_components as html
import dash_core_components as dcc
from tnp_dash_library.LayoutLibrary.ExpandableContent import ExpandableContent
from tnp_dash_library.LayoutLibrary.FixedContent import FixedContent
from tnp_dash_library.LayoutLibrary.TNPContent import TNPContent, TNPControl
import Utility.Unzip as uz
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from tnp_dash_library.SimpleWidgetLibrary.TNPSlider import TNPSlider
import Visualisations.PDCharts as pdc
import json
import copy

class TransitionMatrixContent(TNPContent):

    def __init__(self, debug: bool = False):
        EXPANDABLE = True
        ID = 'pd-transition-matrix-container'
        NAME = "Transition Matrix"

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

        slider = TNPSlider('transition-year', 'Transition Year', 'tsm000', 0, 9, 0,
                           {x: x for x in range(0, 10)}, 1, self.debug, 0)
        chart = dcc.Loading(html.Div(id='pd-transition-matrix-chart-child-container'))

        return dcc.Loading(html.Div([slider.layout(), chart], id='pd-transition-matrix-chart-container',
                                    hidden=True))

    def layout(self, params=None):
        return self.layout_helper.content_layout()

    def content_call_back(self, app):
        if self.is_expandable:
            self.layout_helper.content_call_back(app)

        @app.callback(Output('pd-transition-matrix-chart-child-container', 'children'),
                      Output('pd-transition-matrix-container-modal-body', 'children'),
                      Output('pd-transition-matrix-chart-container', 'hidden'),
                      Input('submit-model', 'n_clicks'),
                      State('model_data', 'data'),
                      State({'type': 'model-dropdown', 'index': 0}, 'value'),
                      State({'type': 'transition-year', 'index': 0}, 'value'))
        def update_transition_matrix(n_clicks, model_data, model, year):
            if n_clicks is None:
                raise PreventUpdate
            if n_clicks == 0:
                raise PreventUpdate
            dist, dist2 = get_transition_matrix_chart_data(model, model_data, year)
            return dist2, dist, False

        @app.callback(
            Output('pd-transition-matrix-chart-child-container', 'children'),
            Output('pd-transition-matrix-container-modal-body', 'children'),
            Output('pd-transition-matrix-chart-container', 'hidden'),
            Input({'type': 'model-dropdown', 'index': 0}, 'value'))
        def clear(model):
            if model is not None:
                raise PreventUpdate
            return "", "", True

        @app.callback(
            Output('pd-transition-matrix-chart-child-container', 'children'),
            Output('pd-transition-matrix-container-modal-body', 'children'),
            Output('pd-transition-matrix-chart-container', 'hidden'),
            Input({'type': 'transition-year', 'index': 0}, 'value'),
            State('model_data', 'data'),
            State({'type': 'model-dropdown', 'index': 0}, 'value'),
            State('pd-transition-matrix-chart-container', 'hidden'),
            prevent_initial_call = True)
        def update_transition_matrix( year, model_data, model, hidden):
            if hidden:
                raise PreventUpdate
            dist, dist2 = get_transition_matrix_chart_data(model, model_data, year)
            return dist2, dist, False

    def register_control(self, control):
        if not issubclass(type(control), TNPControl):
            raise Exception("Only a 'TNPControl' can be registered in 'TNPContent'")
        self.controls.append(control)


def get_transition_matrix_chart_data(model, model_data, year):
    uncompressed_data = json.loads(uz.json_unzip(model_data)['pd_data'])[model]
    fig1 = pdc.plotTransitionMatrix(uncompressed_data, year)
    fig2 = copy.copy(fig1)

    title = fig1['layout']['title']['text']
    fig1['layout']['title']['text'] = title + ": " + str(model).upper().replace("_", " ")
    fig2['layout']['title']['text'] = title + ": " + str(model).upper().replace("_", " ")
    dist = dcc.Graph(figure=fig2, config={'displaylogo': False, 'editable': True},
                     id='ci-projection-plot', className='expandable_chart-half', style={"height": "72vh"})
    for i, txt in enumerate(d['text'] for d in fig1['layout']['annotations']):
        fig1['layout']['annotations'][i]['text'] = ""
        fig2['layout']['annotations'][i]['text'] = "{:.1%}".format(float(txt))
    dist2 = dcc.Graph(figure=fig1, config={'displaylogo': False, 'editable': True},
                      id='ci-projection-plot-2', className='expandable_chart-half', style={"height": "25vh"})
    return dist, dist2