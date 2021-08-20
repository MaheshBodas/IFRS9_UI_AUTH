import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from tnp_dash_library.LayoutLibrary.TNPContent import TNPContent


class ValueMetric(TNPContent):
    """
    Value Metric

    Creates a RAG status headline metric based upon an absolute value
    Must be added to a 'HeadlineMetricBar' to be rendered in the application

    Callback outputs:
     - value: metric_id + '-value'
    """

    def __init__(self, value: float, name: str, metric_id: str, red: float, amber: float,
                 format_code: str):
        """
        Parameters
        ----------
        value : str
            The value of the metric
        name : str
            Title of the metric displayed on the metric header
        metric_id : str
            Unique metric ID. Is used to define the callback output ids
        red : float
            The red tolerance of the metric
        amber : float
            The amber tolerance of the metric
        format_code : str
            Python string format code to render the display of the metric
        """

        self.value = value
        self.id = metric_id
        self.name = name

        if amber <= red:
            self.ltet = True
            self.RAYG_Cutoffs = [red, amber, -999999999999]
        else:
            self.ltet = False
            self.RAYG_Cutoffs = [999999999999, amber, red]

        self.format_code = format_code
        super().__init__(name)

    def content_call_back(self, app):
        return

    def content_layout(self, params=None):
        return

    def layout(self, params=None):

        tool_tip_text = ValueMetric.__tooltiptext(self.ltet, self.RAYG_Cutoffs, self.format_code)

        card_content = [
            dcc.Store(self.id + '-rayg', data=self.RAYG_Cutoffs),
            dcc.Store(self.id + '-ltet', data=self.ltet),
            dcc.Store(self.id + '-format', data=self.format_code),
            dcc.Store(self.id + '-name', data=self.name),
            dbc.CardHeader(self.name),
            dbc.CardBody(
                [
                    html.H5(className="card-title", id=self.id + '-display'),
                    html.Div(self.value, hidden=True, id=self.id + '-value'),
                    html.Div(
                        html.Span(tool_tip_text, id=self.id + '-indicator-circle-tool',
                                  className="tooltiptext_custom"),
                        id=self.id + '-indicator', className='tooltip_custom')
                ]
            ),
        ]
        metric = dbc.Card(card_content, inverse=False, className='headline-metric',
                          id=self.id + '-card-color')
        return metric

    def component_callbacks(self, app):
        @app.callback(Output(self.id + '-indicator', 'className'),
                      Output(self.id + '-display', 'children'),
                      Output(self.id + '-indicator-circle-tool', 'children'),
                      Input(self.id + '-value', 'children'),
                      State(self.id + '-rayg', 'data'),
                      State(self.id + '-ltet', 'data'),
                      State(self.id + '-format', 'data'),
                      )
        def update_color(value, rayg, ltet, format_code):

            metric = str(format_code).format(value)

            tool_tip_text = ValueMetric.__tooltiptext(ltet, rayg, format_code)

            if ltet:
                if value >= rayg[0]:
                    class_name = "red-indicator"
                elif value >= rayg[1]:
                    class_name = "amber-indicator"
                else:
                    class_name = "green-indicator"
            else:
                if value <= rayg[2]:
                    class_name = "red-indicator"
                elif value <= rayg[1]:
                    class_name = "amber-indicator"
                else:
                    class_name = "green-indicator"

            return class_name + ' ' + 'tooltip_custom', metric, tool_tip_text

    def register_control(self, control):
        pass

    @staticmethod
    def __tooltiptext(ltet, rayg_cutoffs, format_code):

        if ltet:
            return html.Div(html.P(["Red: >=" + str(format_code).format(rayg_cutoffs[0]),
                                    html.Br(),
                                    "Amber: >=" + str(format_code).format(rayg_cutoffs[1]),
                                    html.Br(),
                                    "Green: <" + str(format_code).format(rayg_cutoffs[1])]))
        else:
            return html.Div(html.P(["Red: <=" + str(format_code).format(rayg_cutoffs[2]),
                                    html.Br(),
                                    "Amber: <=" + str(format_code).format(rayg_cutoffs[1]),
                                    html.Br(),
                                    "Green: >" + str(format_code).format(rayg_cutoffs[1])]))
