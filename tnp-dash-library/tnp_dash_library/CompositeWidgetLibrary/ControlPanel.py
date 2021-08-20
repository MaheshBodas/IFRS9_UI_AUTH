import dash_bootstrap_components as dbc
from dash_oop_components import DashComponent
from tnp_dash_library.LayoutLibrary.TNPContent import TNPControl
from tnp_dash_library.LayoutLibrary.ToolkitPanel import ToolkitPanel
import dash_html_components as html
from dash.dependencies import ClientsideFunction, Input, Output, State
import dash_core_components as dcc
from tnp_dash_library.LayoutLibrary.content_functions import tool_kit_panel


class ControlPanel(DashComponent):
    """
    Application Control Panel

    Hideable side panel that contains controls that need to be accessed across all tabs
    Must be filled with objects derived from 'TNPControls' or a list of 'ToolkitPanel' that contain 'TNPControls'
    """

    def __init__(self, name: str, list_of_controls: list = None):
        """
           Parameters
           ----------
            name : str
               Name displayed at the top of the control panel
            list_of_controls : list, optional
               List of 'TNPControl's or 'ToolkitPanel's (default = None)

       """

        super().__init__(title="control-side-panel", name='control-side-panel')
        self.id = 'control-side-panel'

        if list_of_controls is None:
            list_of_controls = []

        self.name = name
        self.list_of_controls = list_of_controls

        for control in list_of_controls:
            if not isinstance(control, TNPControl) and not isinstance(control, ToolkitPanel):
                raise Exception("Only a list of objects of type "
                                "'TNPControl' or 'ToolkitPanel' can be passed into a Control Panel")

    # region METHOD: DEFINE LAYOUT

    def layout(self, params=None):

        store = dcc.Store('side-toggle-state', data="Closed")
        c_layout = [store, html.Div(self.name, className="control-panel-name")]
        index = 0
        for control in self.list_of_controls:
            if issubclass(type(control), TNPControl):
                content_block = control.layout()
                block_type = ""
            else:
                content_block = tool_kit_panel(self.id + '-toolkit', control.layout())
                block_type = "toolkit-block-container"
                if index > 0:
                    block_type += ' toolkit-block-container-middle'

            c_layout.append(dbc.Row(html.Div(content_block, className=block_type),
                                    style={'width': '100%', 'margin-right': '0px', 'display': 'block'}))

            index += 1

        toggle = dbc.Row(dbc.Button("☰", color="primary", className="mr-1 openbtn btn_shown", id='toggle-button'))
        panel = html.Div(children=c_layout, className="sidepanel_closed ", id="mySidepanel")

        return html.Div([panel, toggle])

    # endregion

    def content_call_back(self, app):
        app.clientside_callback(
            ClientsideFunction(
                namespace='sidepanel',
                function_name='open_close_Nav'
            ),
            Output('side-toggle-state', 'data'),
            Input('toggle-button', 'n_clicks'),
            State('side-toggle-state', 'data')
        )

        for c in self.list_of_controls:
            if c is not None:
                c.content_call_back(app)
