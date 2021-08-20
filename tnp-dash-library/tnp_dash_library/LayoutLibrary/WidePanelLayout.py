import dash_html_components as html
import dash_bootstrap_components as dbc
from tnp_dash_library.LayoutLibrary.TNPContent import TNPContent
from dash_oop_components import DashComponent
from tnp_dash_library.CompositeWidgetLibrary.HeadlineMetricBar import HeadlineMetricBar
from tnp_dash_library.LayoutLibrary.content_functions import content_panel, tool_kit_panel
from tnp_dash_library.LayoutLibrary.ToolkitPanel import ToolkitPanel
from tnp_dash_library.Enums.TNPENums import WidePanelPosition


class WidePanelLayout(DashComponent):
    """
            Wide Panel Layout

            Creates nxm grid layout with a full width spanned panel on the top or bottom of the grid
    """

    def __init__(self, page_tab_name: str, component_id: str, headline: HeadlineMetricBar = None, rows: int = 1,
                 columns: int = 1, content: list = None, widths: list = None,
                 panel_position: WidePanelPosition = WidePanelPosition.TOP):

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
               List of components of Type 'TNPContent' or 'ToolkitPanel' (Default = sets empty content panel)
           widths : list, optional
               List of integers of column widths
                   (width should be 1<=width<=12 and renders the width of column as (width/12)%. Length of widths should
                   equal the 'columns'. Default = None, sets to even widths)
           panel_position : WidePanelPosition, optional
                Side the spanned column panel (default = WidePanelPosition.TOP)
        """



        if widths is None:
            widths = []

        if content is None:
            content = []

        if columns > 4 or columns < 1:
            raise Exception("A minimum of 1 column and a maximum of 3 columns can be added to a page layout")

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

        self._id = component_id
        self._rows = rows
        self._columns = columns
        self._content = content
        self._widths = widths
        self._headline = headline
        self._panel_side = panel_position

        self._height = (82 / (rows + 1))
        if headline is not None:
            self._height = ((82 - 15) / (rows+1))

        super().__init__(title=page_tab_name, name=component_id)

    def layout(self, params=None):
        content = html.Div(className='tnp-tab-container')

        row_layout = []
        content_index = 1
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

        empty = dbc.Row([
            html.Div(content_panel(self._id + '-' + str(0), "Empty Content",
                                   "No content defined", False), className='content-block-container')]
            , className='wide-panel-block-container', style={'height': str(self._height) + 'vh'})

        if len(self._content) > 0:
            if self._content[0] is not None:

                if issubclass(type(self._content[0]), TNPContent):
                    side_panel = dbc.Row([
                        html.Div(self._content[0].layout(), className='content-block-container')
                    ], className='wide-panel-block-container', style={'height': str(self._height) + 'vh'})
                else:
                    panel = tool_kit_panel(self._id + '-toolkit', self._content[0].layout())
                    side_panel = dbc.Row([
                        html.Div(panel, className='content-block-container toolkit-block-container')
                    ], className='wide-panel-block-container', style={'height': str(self._height) + 'vh'})
            else:
                side_panel = empty
        else:
            side_panel = empty

        content_columns = dbc.Row(dbc.Col(row_layout))
        side_panel_row = dbc.Row(side_panel)

        if self._panel_side == WidePanelPosition.TOP:
            container = html.Div(dbc.Col([side_panel_row, content_columns]),
                                 id=self.name, className="page-container-wide")
        else:
            container = html.Div(dbc.Col([content_columns, side_panel_row]),
                                 id=self.name, className="page-container-wide")

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
                content_block = content_panel(self._id + '-' + str(c), "Empty Content",
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
            content_block = content_panel(self._id + '-' + str(c), "Empty Content",
                                          "No content defined", False)
            block_type = ""
        return content_block, width, block_type
