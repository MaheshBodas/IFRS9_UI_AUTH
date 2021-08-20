import dash_html_components as html
import dash_core_components as dcc


def content_panel(panel_id, header, layout, is_expandable):
    if header != "":
        header_class = "panel-heading"
        icon_class = ""
    else:
        header_class = "panel-heading panel-no-header"
        icon_class = "glyphicon-no-header"

    if is_expandable:

        header_row = html.Div(
            [
                html.H3(header, className='panel-title'),
                dcc.Store(id=panel_id + '-hidden', storage_type='memory', data="Closed"),
                html.Ul(
                    [
                        html.Li([
                            html.A(
                                html.I(className="glyphicon glyphicon-resize-full " + icon_class,
                                       id=panel_id + '-tog-btn'),
                                className="fullscreen-btn", role="button",
                                title="Toggle fullscreen", id=panel_id + '-toggle'),
                        ])
                    ], className='list-inline panel-actions')
            ], className=header_class
        )
    else:
        header_row = html.Div(html.H3(header, className='panel-title'), className=header_class)

    panel_body = html.Div([html.Div(layout)], className="panel-body")

    return html.Div(
        [header_row,
         panel_body
         ], className="panel panel-default content-block")


def tool_kit_panel(panel_id, layout):
    return html.Div(layout, id=panel_id, className="toolkit-panel-body")
