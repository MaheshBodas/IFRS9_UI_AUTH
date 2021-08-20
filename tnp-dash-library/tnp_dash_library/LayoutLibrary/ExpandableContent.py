from dash.dependencies import ClientsideFunction, Input, Output, State
from tnp_dash_library.LayoutLibrary.content_functions import content_panel
from tnp_dash_library.LayoutLibrary.TNPContent import TNPContent
import dash_html_components as html
import dash_bootstrap_components as dbc


class ExpandableContent(TNPContent):
    def __init__(self, component_id, name, layout):
        self._id = component_id
        self.name = name
        self.modal = html.Div([
            dbc.Modal([
                dbc.ModalHeader(name),
                dbc.ModalBody(html.Div(id=self._id + '-modal-body'), style={"height": '72vh'}),
                dbc.ModalFooter(
                    dbc.Button("X", id=self._id + '-modal-close', className="btn_modal", n_clicks=0))],
                id=self._id + '-modal',
                is_open=False,
            )])
        self.layout = html.Div([layout, self.modal])

        super().__init__(component_id)

    def content_layout(self, params=None):
        return content_panel(self._id, self.name, self.layout, True)

    def content_call_back(self, app):
        @app.callback(
            Output(self._id + '-modal', "is_open"),
            [Input(self._id + '-toggle', 'n_clicks'),
             Input(self._id + '-modal-close', 'n_clicks')],
            [State(self._id + '-modal', "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open

    def register_control(self, control):
        pass
