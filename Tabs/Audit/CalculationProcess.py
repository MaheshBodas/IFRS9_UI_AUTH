import dash_html_components as html
import dash_core_components as dcc
from tnp_dash_library.LayoutLibrary.ExpandableContent import ExpandableContent
from tnp_dash_library.LayoutLibrary.FixedContent import FixedContent
from tnp_dash_library.LayoutLibrary.TNPContent import TNPContent, TNPControl
from dash_extensions import Mermaid


class CalculationProcess(TNPContent):

    def __init__(self, debug: bool = False):
        EXPANDABLE = False
        ID = 'audit-log-container'
        NAME = "Calculation Process"

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

        chart = """
        graph LR;
        s100((start))-->a101;
        style s100 fill:#00B050,stroke:#599FE1,stroke-width:3px,color:white;
        a101(Select reporting date)== 31/03/2016 ==>b102(Upload model configuration file);
        style a101 fill:#9EB979,stroke:#599FE1,stroke-width:3px,color:#13245A;
        b102== configuration.xlsx ==>c103(Run Models);
        style b102 fill:#9EB979,stroke:#599FE1,stroke-width:3px,color:#13245A;
        c103== UK, GCC ==>d104(Import Facility Data);
        style c103 fill:#9EB979,stroke:#599FE1,stroke-width:3px,color:#13245A;
        d104== Data Import Error ==>err1[Error];
        style err1 fill:#A13B00,stroke:#599FE1,stroke-width:3px,color:white ;
        d104-->e105(Perform Calculation);
        style d104 fill:#DEB43F,stroke:#599FE1,stroke-width:3px,color:#13245A ;
        e105-->f106(Period on Period Reporting);
        style e105 fill:#E4EAED,stroke:#599FE1,stroke-width:3px,color:#13245A;
        f106-->g107(ECL Forecasting);
        style f106 fill:#E4EAED,stroke:#599FE1,stroke-width:3px, color:#13245A;
        style g107 fill:#E4EAED,stroke:#599FE1,stroke-width:3px,color:#13245A;
        g107-->e100((end));
        style e100 fill:#FF0000,stroke:#599FE1,stroke-width:3px,color:white;
        """

        return html.Div(Mermaid(chart=chart), style={ 'margin-top': '9vh', 'text-align': 'center'})

    def layout(self, params=None):
        return self.layout_helper.content_layout()

    def content_call_back(self, app):
        if self.is_expandable:
            self.layout_helper.content_call_back(app)

    def register_control(self, control):
        if not issubclass(type(control), TNPControl):
            raise Exception("Only a 'TNPControl' can be registered in 'TNPContent'")
        self.controls.append(control)


