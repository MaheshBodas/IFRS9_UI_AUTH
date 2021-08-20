from dash_oop_components import DashComponent
from tnp_dash_library.LayoutLibrary.TNPContent import TNPControl
import dash_html_components as html
import dash_bootstrap_components as dbc


class ToolkitPanel(DashComponent):
    """
    Container for TNPControls

    Styled content panel that is used to store a series of connected TNPControls
    """
    def __init__(self, component_id: str, name: str, controls: list = None):
        """
            Parameters
            ----------
            component_id: str
                Unique name of the toolkit panel
            name : str
               Name displayed at the top of the toolkit panel
            controls : list, optional
               List of 'TNPControl's  (default = None)
       """

        if controls is None:
            controls = []

        for t in controls:
            if not issubclass(type(t), TNPControl) and t is not None:
                raise Exception("Content must inherit from 'TNPContent' class")

        self.controls = []
        self.name = name
        self.controls = controls
        self.id = component_id
        super().__init__(name=component_id)

    def layout(self, params=None):

        c_layout = []
        for control in self.controls:
            c_layout.append(html.Div(control.layout(), style={'width': '100%'}))

        panel = html.Div(children=c_layout, className="tool-kit-panel", id=self.id + '-toolkit',
                         style={'padding-top':'10px'})

        return html.Div([html.Div(self.name, className="toolkit-label"), panel], style={'width': '100%'})

    def content_call_back(self, app):
        for t in self.controls:
            t.store_value(app)
