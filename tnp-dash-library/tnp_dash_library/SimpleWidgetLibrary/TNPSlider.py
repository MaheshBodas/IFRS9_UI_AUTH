from tnp_dash_library.LayoutLibrary.TNPContent import TNPControl
import dash_core_components as dcc
from dash.dependencies import Input, Output, MATCH
import dash_html_components as html


class TNPSlider(TNPControl):
    """
    TNP Slider

    Styled slider with label.

    Callback outputs:
     - var_name stores the value of the slider
    """

    def __init__(self, slider_id: str, label: str, var_name: str, min_value: float, max_value: float,
                 value: float, marks: dict, step: float = None, debug: bool = False, index: int = 0,
                 className="", **kwargs):
        """
            Parameters
            ----------
            slider_id : str
               Unique id of the slider
            label : str
               The label displayed above the slider
            var_name : str
               The variable name used to store the slider value to use as inputs into calculation callbacks
            min_value : float
               Minimum value of the slider
            max_value : float
               Maximum value of the slider
            value : float
               Initial value of the slider
            marks : dict
               Dictionary value of slider marks:
                    Key = value on the slider corresponding to where the mark label will be placed
                    Value = Dictionary of attributes (Label attribute is mandatory)
                    Example with styling (dictionary of styles):
                    marks={0:     {'label': '0%',   'style': {'color': '#9EB979'}},
                           0.025: {'label': '2.5%', 'style': {'color': '#9EB979'}},
                           0.05:  {'label': '5%',   'style': {'color': '#9EB979'}},
                           0.075: {'label': '7.5%', 'style': {'color': '#A13B00'}},
                           0.1:   {'label': '10%',  'style': {'color': '#A13B00'}},
                           0.125: {'label': '12.5%','style': {'color': '#A13B00'}},
                           0.15:  {'label': '15%',  'style': {'color': '#A13B00'}},
                           0.175: {'label': '17.5%','style': {'color': '#A13B00'}},
                           0.2:   {'label': '20%',  'style': {'color': '#A13B00'}},
                           0.225: {'label': '22.5%','style': {'color': '#A13B00'}},
                           0.25:  {'label': '25%',  'style': {'color': '#A13B00'}},
                           0.275: {'label': '27.5%','style': {'color': '#A13B00'}},
                           0.30:  {'label': '30%',  'style': {'color': '#A13B00'}}}
            step : float, optional
                Value by which increments or decrements are made (default = None)

            debug: bool, optional
                Prints the stored var_name and value above slider if true to help debugging (default = False)

            index :  int, optional
               Used to control index of callbacks - use when dynamically creating component  (Default = 0)

            **kwargs: optional
                See https://dash.plotly.com/dash-core-components/slider for more details
       """

        self.id = slider_id
        self.label = label
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = value
        self.marks = marks
        self.var_name = var_name + "_" + str(index)
        self.kwargs = kwargs
        self.debug = debug
        self.index = index
        self.registered = False
        self.className = className
        super().__init__(name=self.id)

    def layout(self, params=None):

        if self.debug:
            debug_html = html.Div(
                [html.Div("", id={'type': self.id + '-test-div', 'index': self.index},
                          hidden=not self.debug, className="debug_variable")]
            )
        else:
            debug_html = html.Div()

        return html.Div(
            [debug_html,
             dcc.Store(id={'type': self.id + '-data', 'index': self.index},
                       data=self.value, storage_type='session'),
             html.Div(self.label, className='data-options-headings-top'),
             dcc.Slider(**self.kwargs,
                        min=self.min_value,
                        max=self.max_value,
                        step=self.step,
                        value=self.value,
                        marks=self.marks,
                        id={'type': self.id, 'index': self.index},
                        className='layout-sliders',
                        persistence_type='session',
                        persistence=True
                        )
             ],
            style={'width': '100%'}, className=self.className)

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
