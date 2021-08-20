import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from tnp_dash_library.LayoutLibrary.TNPContent import TNPContent
from tnp_dash_library.Enums.TNPENums import ChangeMetricType


class ChangeMetric(TNPContent):
    """
    Change Metric

    Creates a RAG status headline metric based upon the size of the change of the value from the initial value
    Must be added to a 'HeadlineMetricBar' to be rendered in the application

    Callback outputs:
     - value: metric_id + '-value'
     - base_value: metric_id + '-base-value'
    """

    def __init__(self, base_value: float, value: float, change_type: ChangeMetricType, name: str, metric_id: str,
                 red: float, amber: float, format_code: str):

        """
        Parameters
        ----------
        base_value : float
            The base value the change is compared against
        value : str
            The value of the metric
        change_type : ChangeMetricType
            ChangeMetricType.ABSOLUTE considers the difference in the value to the base value, ChangeMetricType.RELATIVE
            considers the percentage change in the value to the base value
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

        self.base_value = base_value
        self.value = value
        self.id = metric_id
        self.name = name
        self.change_type = change_type

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

    def register_control(self, control):
        pass

    def layout(self, params=None):

        tool_tip_text = ChangeMetric.__tooltiptext(self.ltet, self.RAYG_Cutoffs, self.format_code, self.change_type)

        card_content = [
            dcc.Store(self.id + '-rayg', data=self.RAYG_Cutoffs),
            dcc.Store(self.id + '-ltet', data=self.ltet),
            dcc.Store(self.id + '-format', data=self.format_code),
            dcc.Store(self.id + '-name', data=self.name),
            dcc.Store(self.id + '-base', data=self.base_value),
            dcc.Store(self.id + '-type', data=int(self.change_type.value)),
            dbc.CardHeader(self.name),
            dbc.CardBody(
                [
                    html.Div([
                        html.H5(className="card-title", id=self.id + '-display'),
                        html.P(className="card-title-base", id=self.id + '-base-display'),
                    ], className='metric-base-value'),
                    html.Div(self.value, hidden=True, id=self.id + '-value'),
                    html.Div(self.base_value, hidden=True, id=self.id + '-base-value'),
                    html.Div([
                        html.P(id=self.id + '-change', className='metric-change-value'),
                        html.Div(
                            html.Span(tool_tip_text, id=self.id + '-indicator-arrow-tool',
                                      className="tooltiptext_custom"),
                            id=self.id + '-indicator-arrow', className='tooltip_custom')
                    ], className='metric-indicator-container')
                ]
            ),
        ]
        metric = dbc.Card(card_content, inverse=False, className='headline-metric',
                          id=self.id + '-card-color')
        return metric

    def component_callbacks(self, app):
        @app.callback(Output(self.id + '-indicator-arrow', 'className'),
                      Output(self.id + '-display', 'children'),
                      Output(self.id + '-base-display', 'children'),
                      Output(self.id + '-change', 'children'),
                      Output(self.id + '-indicator-arrow-tool', 'children'),
                      Input(self.id + '-value', 'children'),
                      Input(self.id + '-base-value', 'children'),
                      State(self.id + '-rayg', 'data'),
                      State(self.id + '-ltet', 'data'),
                      State(self.id + '-format', 'data'),
                      State(self.id + '-type', 'data'),
                      )
        def update_color(value, base_value, rayg, ltet, format_code, change_type):

            metric = str(format_code).format(value)
            base_metric = str(format_code).format(base_value)

            if change_type == ChangeMetricType.ABSOLUTE.value:
                change = value - base_value
                change_output = str(format_code).format(change)
            else:
                change = (value / base_value) - 1
                change_output = "{:.2%}".format(change)

            if value > base_value:
                direction_class = "arrow-up"
                change_output = "+" + change_output
            else:
                direction_class = "arrow-down"

            if ltet:
                if change >= rayg[0]:
                    class_name = direction_class + "-red"
                elif change >= rayg[1]:
                    class_name = direction_class + "-amber"
                else:
                    class_name = direction_class + "-green"
            else:
                if change <= rayg[2]:
                    class_name = direction_class + "-red"
                elif change <= rayg[1]:
                    class_name = direction_class + "-amber"
                else:
                    class_name = direction_class + "-green"

            tool_tip = ChangeMetric.__tooltiptext(ltet, rayg, format_code, change_type)

            return direction_class + ' ' + class_name + ' ' + 'tooltip_custom', metric, base_metric, \
                   change_output, tool_tip

    @staticmethod
    def __tooltiptext(ltet: bool, rayg_cutoffs: list, format_code: str, change_type: type(ChangeMetricType)):

        if change_type == ChangeMetricType.ABSOLUTE.value:
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
        else:
            if ltet:
                return html.Div(html.P(["Red: >=" + str("{:.2%}").format(rayg_cutoffs[0]),
                                        html.Br(),
                                        "Amber: >=" + str("{:.2%}").format(rayg_cutoffs[1]),
                                        html.Br(),
                                        "Green: <" + str("{:.2%}").format(rayg_cutoffs[1])]))
            else:
                return html.Div(html.P(["Red: <=" + str("{:.2%}").format(rayg_cutoffs[2]),
                                        html.Br(),
                                        "Amber: <=" + str("{:.2%}").format(rayg_cutoffs[1]),
                                        html.Br(),
                                        "Green: >" + str("{:.2%}").format(rayg_cutoffs[1])]))
