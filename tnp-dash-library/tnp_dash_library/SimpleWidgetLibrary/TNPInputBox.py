from tnp_dash_library.LayoutLibrary.TNPContent import TNPControl
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, MATCH
from tnp_dash_library.Enums.TNPENums import LabelPosition


class TNPInputBox(TNPControl):
    """
    TNP Input Box

    Styled input box with label.

    Callback outputs:
     - var_name stores the value of the slider
    """

    def __init__(self, input_id: str, label: str, var_name: str, label_position: LabelPosition.LEFT,
                 input_unit: str = "£", input_type: str = "number", label_width: int = 3,
                 default_value: str = "", debug: bool = False, index: int = 0, tool_tip: str = "", className="",
                 persist=True,
                 **kwargs):
        """
            Parameters
            ----------
            input_id : str
               Unique id of the input box
            label : str
               The label displayed above the slider
            var_name : str
               The variable name used to store the slider value to use as inputs into calculation callbacks
            default_value : str
               Default textbox value
            debug: bool, optional
                Prints the stored var_name and value above slider if true to help debugging (default = False)

            index :  int, optional
               Used to control index of callbacks - use when dynamically creating component  (Default = 0)

            tool_tip :  str, optional
               Tool tip on text box hover  (Default = None)

            **kwargs: optional
                See https://dash.plotly.com/dash-core-components/input for more details
       """

        self.id = input_id
        self.label = label
        self.default_value = default_value
        self.var_name = var_name + "_" + str(index)
        self.kwargs = kwargs
        self.debug = debug
        self.registered = False
        self.index = index
        self.input_unit = input_unit
        self.label_position = label_position
        self.input_type = input_type
        self.label_width = label_width
        self.tool_tip = tool_tip
        self.className = className
        self.persist = persist

        if (label_width < 1 or label_width > 12) and label_position == LabelPosition.LEFT:
            raise Exception("Label width should be between 1 and 12 if using LabelPosition.LEFT")

        super().__init__(name=self.id)

    def layout(self, params=None):

        if self.tool_tip == "":
            tool_tip = html.Div()
        else:
            tool_tip = dbc.Tooltip(self.tool_tip, target=self.id + '-tooltip-target', className="tb-tool-tip")

        if self.label_position == LabelPosition.LEFT:
            input_width = 12 - self.label_width
            control = dbc.Row(
                [
                    dbc.Col(html.Div(self.label, style={"margin-top": "7px", "padding-right": "0px"}),
                            width=self.label_width, style={"padding-right": "0px"}),
                    dbc.Col(
                        dbc.InputGroup([
                            dbc.InputGroupAddon(self.input_unit, addon_type="prepend"),
                            dbc.Input(**self.kwargs,
                                      id={'type': self.id, 'index': self.index},
                                      className='tnp_input_box',
                                      persistence_type='session',
                                      persistence=self.persist,
                                      debounce=True,
                                      type=self.input_type,
                                      value=self.default_value

                                      )], className="mb-3",
                        )
                        , width=input_width, style={"padding-left": "0px"}), tool_tip
                ], id=self.id + '-tooltip-target', className=self.className)
        else:
            control = html.Div(
                [
                    html.Div(self.label),
                    dbc.InputGroup([
                        dbc.InputGroupAddon(self.input_unit, addon_type="prepend"),
                        dbc.Input(**self.kwargs,
                                  id={'type': self.id, 'index': self.index},
                                  className='tnp_input_box',
                                  persistence_type='session',
                                  persistence=True,
                                  debounce=True,
                                  placeholder=self.default_value,
                                  type=self.input_type

                                  )], className="mb-3",
                    ), tool_tip

                ], id=self.id + '-tooltip-target'
            )

        if self.debug:
            debug_html = html.Div(
                [html.Div("", id={'type': self.id + '-test-div', 'index': self.index},
                          hidden=not self.debug, className="debug_variable"),
                 ]
            )
        else:
            debug_html = html.Div()

        return html.Div(
            [dcc.Store(id={'type': self.id + '-data', 'index': self.index},
                       data=self.default_value, storage_type='session'),
             debug_html,
             control
             ],
            style={'width': '100%', 'margin-top': '10px'}, className="TNP_input_box " + self.className, id=self.id)

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
