from tnp_dash_library.LayoutLibrary.TNPContent import TNPControl
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH


class TNPDataUpload(TNPControl):
    """
    TNP Data Uploader

    Styled data upload widget .

    Callback outputs:
     - var_name stores the filename
    """

    def __init__(self, input_id: str, var_name: str, debug: bool = False, index: int = 0, fileDescription: str = "",
                 **kwargs):
        """
            Parameters
            ----------
            input_id : str
               Unique id of the input box
            var_name : str
               The variable name used to store the slider value to use as inputs into calculation callbacks
            debug: bool, optional
                Prints the stored var_name and value above slider if true to help debugging (default = False)
            index :  int, optional
               Used to control index of callbacks - use when dynamically creating component  (fefault = 0)
            **kwargs: optional
                See https://dash.plotly.com/dash-core-components/upload for more details
       """

        self.id = input_id
        self.kwargs = kwargs
        self.debug = debug
        self.registered = False
        self.index = index
        self.var_name = var_name
        self._description = fileDescription
        super().__init__(name=self.id)

    def layout(self, params=None):
        if self._description == "":
            content = ['📁 ', 'Drag and Drop or ', html.A('Select File')]
        else:
            content = ['📁 ', 'Drag and Drop or ', html.A('Select ' + self._description)]

        uploader = dcc.Upload(id={'type': self.id, 'index': self.index},
                              children=html.Div(content, style={'font-size': '12px'}),
                              multiple=False,
                              className='TNP-file-uploader')

        if self.debug:
            debug_html = html.Div(
                [html.Div("", id={'type': self.id + '-test-div', 'index': self.index},
                          hidden=not self.debug, className="debug_variable"),
                 dcc.Store(id={'type': self.id + '-data', 'index': self.index}, storage_type='session')])
        else:
            debug_html = html.Div()

        return html.Div(
            [debug_html,
             uploader],
            style={'width': '100%'})

    def store_value(self, app):
        if not self.registered:
            self.registered = True

            if self.debug:
                @app.callback(Output({'type': self.id + '-test-div', 'index': MATCH}, 'children'),
                              Input({'type': self.id, 'index': MATCH}, 'contents'),
                              State({'type': self.id, 'index': MATCH}, 'filename'))
                def _display_value(contents, filename):
                    return self.var_name + ' = ' + str(filename)

            @app.callback(Output({'type': self.id + '-data', 'index': MATCH}, 'data'),
                          Input({'type': self.id, 'index': MATCH}, 'contents'))
            def _display_value(contents):
                return contents
