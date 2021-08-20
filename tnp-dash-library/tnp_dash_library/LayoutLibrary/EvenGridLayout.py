import dash_html_components as html
import dash_bootstrap_components as dbc
from tnp_dash_library.LayoutLibrary.TNPContent import TNPContent
from tnp_dash_library.LayoutLibrary.ToolkitPanel import ToolkitPanel
from dash_oop_components import DashComponent
from tnp_dash_library.CompositeWidgetLibrary.HeadlineMetricBar import HeadlineMetricBar
from tnp_dash_library.LayoutLibrary.content_functions import content_panel, tool_kit_panel


class EvenGridLayout(DashComponent):
    """
    Even Grid Layout

    Creates an nxm layout grid
    """
    def __init__(self, page_tab_name: str, component_id: str, headline: HeadlineMetricBar = None, rows: int = 1,
                 columns: int = 1, content: list = None, widths: list = None):
        """
        Parameters
        ----------
        page_tab_name : str
            The name that appears on the tab
        component_id : str
            ID of tab page - must be unique
        headline : HeadlineMetricBar, optional
            Headline metric bar is added across the top of the tab (Default = None)
        rows : int, optional
            Number of grid rows (default=1, min=1)
        columns : int, optional
            Number of grid columns (default=1, min=1, max = 4)
        content : list, optional
            List of components of Type 'TNPContent' or 'ToolkitPanel'
        widths : list, optional
               List of integers of column widths
                   (width should be 1<=width<=12 and renders the width of column as (width/12)%. Length of widths should
                   equal the 'columns'. Default = None, sets to even widths)
        """


        if widths is None:
            widths = []

        if content is None:
            content = []

        if columns > 4 or columns < 1:
            raise Exception("A minimum of 1 column and a maximum of 4 columns can be added to a page layout")

        if rows < 1:
            raise Exception("A minimum of 1 row must be added to a page layout")

        if len(widths) != 0 and len(widths) != columns:
            raise Exception("The number of column widths given does not match number of columns")

        if len(widths) != 0 and sum(widths) != 12:
            raise Exception("Column widths should be integer values between 1 and 12 and sum to 12")

        for c in content:
            if not issubclass(type(c), TNPContent) and not issubclass(type(c), ToolkitPanel) and c is not None:
                raise Exception("Content must inherit from 'TNPContent' or 'ToolkitPanel' class")

        if not issubclass(type(headline), HeadlineMetricBar) and headline is not None:
            raise Exception("Only an object of type 'HeadlineMetricBar' can be added as a tab headline")

        self._column_width = 12 / columns
        self._height = (82 / rows)
        self._id = component_id
        self._rows = rows
        self._columns = columns
        self._content = content
        self._widths = widths
        self._headline = headline

        if headline is not None:
            self._height = (82 / rows) - 15

        super().__init__(title=page_tab_name, name=component_id)

    def layout(self, params=None):
        content = html.Div(className='tnp-tab-container')

        row_layout = []
        content_index = 0
        for r in range(0, self._rows):
            col_layout = []
            r_layout = dbc.Row(style={'height': str(self._height) + 'vh'})
            for c in range(0, self._columns):

                content_block, width, block_type = self.define_column(c, content_index)

                col_layout.append(
                    dbc.Col([
                            html.Div(content_block, className='content-block-container' + ' ' + block_type)
                    ], width=width)
                )

                content_index += 1

            r_layout.children = col_layout
            row_layout.append(r_layout)

        container = html.Div(row_layout, id=self.name, className="page-container")

        if self._headline is not None:
            content.children = [html.Div(self._headline.layout(), className='metric-bar',
                                         style={'display': 'flex'}), html.Div(container)]
        else:
            content.children = [html.Div(container)]

        return dbc.Container(content, fluid=True)

    def define_column(self, c, content_index):
        if len(self._widths) > c:
            width = self._widths[c]
        else:
            width = self._column_width
        if len(self._content) > content_index:

            if self._content[content_index] is None:
                content_block = content_panel(self._id + '-' + str(content_index), "Empty Content",
                                              "No content defined", False)
                block_type = ""
            else:
                if issubclass(type(self._content[content_index]), TNPContent):
                    content_block = self._content[content_index].layout()
                    block_type = ""
                else:
                    content_block = tool_kit_panel(self._id + '-toolkit', self._content[content_index].layout())
                    block_type = "toolkit-block-container"
        else:
            content_block = content_panel(self._id + '-' + str(content_index), "Empty Content",
                                          "No content defined", False)
            block_type = ""
        return content_block, width, block_type
