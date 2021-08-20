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


class MacroScalarsContent(TNPContent):

    def __init__(self, debug: bool = False):
        EXPANDABLE = True
        ID = 'ms-container'
        NAME = "Macroeconomic Scalars"

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

        chart = dcc.Loading(html.Div(id='ms-chart-child-container'))

        return dcc.Loading(html.Div([chart], id='ms-chart-container',
                                    hidden=True))

    def layout(self, params=None):
        return self.layout_helper.content_layout()

    def content_call_back(self, app):
        if self.is_expandable:
            self.layout_helper.content_call_back(app)

        @app.callback(Output('ms-chart-child-container', 'children'),
                      Output('ms-container-modal-body', 'children'),
                      Output('ms-chart-container', 'hidden'),
                      Input('submit-model', 'n_clicks'),
                      State('model_data', 'data'),
                      State({'type': 'model-dropdown', 'index': 0}, 'value'))
        def update_transition_matrix(n_clicks, model_data, model):
            if n_clicks is None:
                raise PreventUpdate
            if n_clicks == 0:
                raise PreventUpdate
            dist, dist2 = get_macro_scalar(model, model_data)
            return dist2, dist, False

        @app.callback(
            Output('ms-chart-child-container', 'children'),
            Output('ms-container-modal-body', 'children'),
            Output('ms-chart-container', 'hidden'),
            Input({'type': 'model-dropdown', 'index': 0}, 'value'))
        def clear(model):
            if model is not None:
                raise PreventUpdate
            return "", "", True

    def register_control(self, control):
        if not issubclass(type(control), TNPControl):
            raise Exception("Only a 'TNPControl' can be registered in 'TNPContent'")
        self.controls.append(control)


def get_macro_scalar(model, model_data):
    uncompressed_data = json.loads(uz.json_unzip(model_data)['pd_data'])[model]
    fig1 = pdc.plotMacroScalars(uncompressed_data)
    title = fig1['layout']['title']['text']
    fig1['layout']['title']['text'] = title + ": " + str(model).upper().replace("_", " ")
    dist = dcc.Graph(figure=fig1, config={'displaylogo': False, 'editable': True},
                     className='expandable_chart-half', style={"height": "72vh"})
    dist2 = dcc.Graph(figure=fig1, config={'displaylogo': False, 'editable': True},
                     className='expandable_chart-half', style={"height": "31vh"})
    return dist, dist2
