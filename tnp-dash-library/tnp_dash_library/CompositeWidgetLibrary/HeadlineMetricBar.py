import dash_bootstrap_components as dbc
from dash_oop_components import DashComponent
from tnp_dash_library.SimpleWidgetLibrary.ValueMetric import ValueMetric
from tnp_dash_library.SimpleWidgetLibrary.ChangeMetric import ChangeMetric


class HeadlineMetricBar(DashComponent):
    """
        Headline Metric Bar

        Container to hold content of type 'ValueMetric' or 'ChangeMetric'
    """

    def __init__(self, bar_id: str, list_of_metrics: list = None):

        """
            Parameters
            ----------
            bar_id : str
                Unique id of the headline metric bar
            list_of_metrics : list, optional
                List of 'ValueMetric' or 'ChangeMetric' objects (default = None)
        """

        super().__init__(title="headline-metric-bar", name=bar_id)

        if list_of_metrics is None:
            list_of_metrics = []

        for metric in list_of_metrics:
            if not isinstance(metric, ValueMetric) and not isinstance(metric, ChangeMetric):
                raise Exception("Only a list of objects of type "
                                "'ValueMetric' or 'ChangeMetric' can be passed into a HeadlineMetricBar")
        self.list_of_metrics = list_of_metrics

    # region METHOD: DEFINE LAYOUT

    def layout(self, params=None):
        c_layout = []
        for metric in self.list_of_metrics:
            c_layout.append(dbc.Col(metric.layout()))

        return c_layout

    # endregion
