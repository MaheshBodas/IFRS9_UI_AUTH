import dash_table
import dash_html_components as html
from Styling import Colours
import pandas as pd
from typing import List


def define_data_table_object(table_name: str, table: pd.DataFrame, page_size: int, theme: Colours.Colour,
                             height: int = 265, columns: List[str] = None, labels: List[str] = None,
                             export: bool = True, vh: bool = False):
    table_header_color = theme.get_theme_colour(2, 4)
    data_border_style = '1px solid ' + theme.get_theme_colour(2, 3)
    header_col = theme.get_white(0)
    font_col = theme.get_theme_colour(1, 0)
    font = theme.font

    if vh:
        table_height = str(height) + 'vh'
    else:
        table_height = str(height) + 'px'

    if columns is None:
        columns = table.columns

    if labels is None:
        labels = table.columns

    if export:
        exp = "csv"
    else:
        exp = ""

    return html.Div([
        dash_table.DataTable(
            id=table_name,
            data=table.to_dict('records'),
            columns=[{'name': labels[i], 'id': columns[i]} for i in range(0, len(columns))],
            style_cell={'textAlign': 'center',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'minWidth': '150px'
                        },
            style_table={'width': '100%', 'height': table_height, 'overflowY': 'auto'},
            style_header={
                'backgroundColor': table_header_color,
                'fontWeight': 'bold',
                'border': data_border_style,
                'font-family': font, 'color': header_col, 'whiteSpace': 'normal',
                'textAlign': 'center'
            },
            page_size=page_size,
            fixed_rows={'headers': True, 'data': 0},
            style_data={'border': data_border_style,
                        'font-family': font, 'color': font_col},
            export_format=exp,
            sort_mode="single",
            sort_action="native",

        )])
