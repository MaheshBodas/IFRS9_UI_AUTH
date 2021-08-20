from tnp_dash_library.LayoutLibrary.TNPContent import TNPControl
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, MATCH
from tnp_dash_library.Enums.TNPENums import LabelPosition


class TNPDropdown(TNPControl):
    """
    TNP Dropdown Box

    Styled dropdown with label.

    Callback outputs:
     - var_name stores the value of the slider
    """

    def __init__(self, input_id: str, label: str, var_name: str, values: list, label_position: LabelPosition.LEFT,
                 label_width: int = 3, selected_value: str = "", debug: bool = False, index: int = 0,
                 tool_tip: str = "", className="", **kwargs):
        """
            Parameters
            ----------
            input_id : str
               Unique id of the input box
            label : str
               The label displayed above the slider
            var_name: str
                Variable name for storing selected values
            values: list
                List of values e.g. [1,"a",9]
            label_position : LabelPosition
               Position of label (Left or Top)
            label_width: int
                Width of label on grid (1-12) as a proportion of 12 (Default = 3 -> 3/12 = 25%)
            selected_value : str
               Default selected value
            debug: bool, optional
                Prints the stored var_name and value above slider if true to help debugging (default = False)
            index :  int, optional
               Used to control index of callbacks - use when dynamically creating component  (Default = 0)
            tool_tip :  str, optional
               Tool tip on text box hover  (Default = None)
            className :  str, optional
               Class Name of component  (Default = None)
            **kwargs: optional
                See https://dash.plotly.com/dash-core-components/dropdown for more details
       """

        if values is None:
            self.values = []
        else:
            self.values = []
            for v in values:
                self.values.append({'label': v, 'value': v})

        self.id = input_id
        self.label = label
        self.selected_value = selected_value
        self.var_name = var_name + "_" + str(index)
        self.kwargs = kwargs
        self.debug = debug
        self.registered = False
        self.index = index
        self.label_position = label_position
        self.label_width = label_width
        self.tool_tip = tool_tip
        self.className = className

        if (label_width < 1 or label_width > 12) and label_position == LabelPosition.LEFT:
            raise Exception("Label width should be between 1 and 12 if using LabelPosition.LEFT")

        super().__init__(name=self.id)

    def layout(self, params=None):

        if self.tool_tip == "":
            tool_tip = html.Div()
        else:
            tool_tip = dbc.Tooltip(self.tool_tip, target=self.id + '-tooltip-target', className="tb-tool-tip")

        dropdown = dcc.Dropdown(**self.kwargs,
                                id={'type': self.id, 'index': self.index},
                                options=self.values,
                                value=self.selected_value,
                                className="drop-form-control",
                                persistence_type='session',
                                persistence=True)

        if self.label_position == LabelPosition.LEFT:
            input_width = 12 - self.label_width
            control = dbc.Row(
                [
                    dbc.Col(html.Div(self.label, style={"margin-top": "7px", 'font-size':'16px'}),
                            width=self.label_width),
                    dbc.Col(dropdown, style={"padding-left": "0px"}),
                    tool_tip
                ], id=self.id + '-tooltip-target', className=self.className)
        else:
            control = html.Div(
                [
                    html.Div(self.label),
                    dropdown,
                    tool_tip
                ], id=self.id + '-tooltip-target'
            )

        if self.debug:
            debug_html = html.Div(
                [html.Div("", id={'type': self.id + '-test-div', 'index': self.index},
                          hidden=not self.debug, className="debug_variable")])
        else:
            debug_html = html.Div()

        return html.Div(
            [dcc.Store(id={'type': self.id + '-data', 'index': self.index},
                           data=self.selected_value, storage_type='session'),
             debug_html,
             control
             ],
            style={'width': '100%'}, className="TNP_dropdown_box " + self.className, id=self.id)

    def store_value(self, app):
        if not self.registered:
            self.registered = True

            if self.debug:
                @app.callback(Output({'type': self.id + '-test-div', 'index': MATCH}, 'children'),
                              Input({'type': self.id, 'index': MATCH}, 'value'))
                def _display_value(input_value):
                    return self.var_name + ' = ' + str(input_value)

            @app.callback(Output({'type': self.id + '-data', 'index': MATCH}, 'data'),
                          Input({'type': self.id, 'index': MATCH}, 'value'))
            def _update_variable(input_value):
                return input_value
