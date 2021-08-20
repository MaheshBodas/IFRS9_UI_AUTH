import plotly.graph_objects as go
from Visualisations.Styling import Colours


def update_layout(figure: go.Figure, title: str, x_axis_title: str, y_axis_title: str, colourTheme: Colours,
                  show_x_grid_lines: bool = True, show_y_grid_lines: bool = True, show_legend: bool = True,
                  x_axis_format: str = "", y_axis_format: str = ""):
    chart_background = colourTheme.get_white(0)
    grid_colour = colourTheme.get_light_grey(1)
    title_colour = colourTheme.get_theme_colour(1, 0)

    main_title = '<b>' + title + '</b>'

    figure.update_layout(
        title=dict(text=main_title, font=dict(size=18, family=colourTheme.font, color=title_colour),
                   x=0.02, y=1, xanchor='left', yanchor='top'),

        xaxis=dict(domain=[0, 1], zeroline=show_x_grid_lines, title=x_axis_title,
                   showline=show_x_grid_lines, zerolinecolor=grid_colour, showticklabels=True,
                   showgrid=show_x_grid_lines, gridcolor=grid_colour,
                   tickfont=dict(color=title_colour, family=colourTheme.font), linecolor=grid_colour,
                   ticks="outside", tickwidth=1, tickcolor=chart_background, ticklen=10, visible=True,
                   tickformat=x_axis_format),

        yaxis=dict(
            title=y_axis_title, titlefont=dict(color=title_colour, family=colourTheme.font),
            tickfont=dict(color=title_colour),
            zeroline=show_y_grid_lines, zerolinecolor=grid_colour, showgrid=show_y_grid_lines,
            showline=show_y_grid_lines, gridcolor=grid_colour, linecolor=grid_colour,
            domain=[0, 0.90], ticks="outside", tickwidth=1, tickcolor=chart_background, ticklen=10,
            automargin=True, tickformat=y_axis_format),
        showlegend=show_legend,
        paper_bgcolor=chart_background,
        plot_bgcolor=chart_background,
        margin=dict(l=50, r=20, t=30, b=20),
        legend=dict(orientation="h",
                    yanchor="bottom",
                    y=0.85,
                    xanchor="right",
                    x=1,
                    font=dict(size=12, family=colourTheme.font, color=title_colour))
    )

    return figure
