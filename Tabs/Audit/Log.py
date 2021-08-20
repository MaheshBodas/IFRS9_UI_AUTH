import dash_html_components as html
import dash_core_components as dcc
from tnp_dash_library.LayoutLibrary.ExpandableContent import ExpandableContent
from tnp_dash_library.LayoutLibrary.FixedContent import FixedContent
from tnp_dash_library.LayoutLibrary.TNPContent import TNPContent, TNPControl
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


class AuditLog(TNPContent):

    def __init__(self, debug: bool = False):
        EXPANDABLE = False
        ID = 'audit-log-container'
        NAME = "Application Log"

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
        log_data = dcc.Store('log_data',  storage_type='session')

        return html.Div([log_data,
                         dcc.Textarea(
                             id='audit-log',
                             style={'width': '100%', 'height': '100%'},
                             contentEditable=False,
                             disabled=True,
                             draggable=False,
                             persistence=True,
                             persistence_type='session'
                         ),
                         ], style={'height': '31vh'})

    def layout(self, params=None):
        return self.layout_helper.content_layout()

    def content_call_back(self, app):
        if self.is_expandable:
            self.layout_helper.content_call_back(app)

        # update log data every time log is updated
        @app.callback(Output('log_data', 'data'),
                      Input('audit-log', 'value'))
        def update_log_value(log):
            return log

        @app.callback(Output('audit-log', 'value'),
                      Input('user-name', 'data'),
                      State('log_data', 'data'))
        def update_log_value(username, log):
            if log is None:
                raise PreventUpdate
            return log

    def register_control(self, control):
        if not issubclass(type(control), TNPControl):
            raise Exception("Only a 'TNPControl' can be registered in 'TNPContent'")
        self.controls.append(control)


