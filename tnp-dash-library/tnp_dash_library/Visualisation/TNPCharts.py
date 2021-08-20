import plotly.graph_objects as go
import tnp_dash_library.Visualisation.Theme as Cols

TITLE_COLOR = Cols.dark_blue.get(0)
GRID_COLOR = Cols.white.get(1)
AXIS_COLOR = Cols.light_gray.get(2)
TICK_FONT = Cols.light_gray.get(3)


def empty_chart():
    return go.Figure()

def bar_line(title, x, x_name: str, y: list, y_name: list, colors: list, legend: bool = True,
             stacked: bool = True, line: bool = False, x_axis_title: str = ""):
    title = '<b>' + title + '</b>'

    fig = go.Figure()
    for r, n, c in zip(y, y_name, colors):
        if line:
            fig.add_trace(go.Scatter(x=x, y=r, name=n, marker=dict(color=c, line=dict(width=2, color=c)),
                                     mode='lines+markers'))
        else:
            fig.add_trace(go.Bar(x=x, y=r, name=n, marker=dict(color=c, line=dict(width=2, color="#FFFFFF")),
                                 ))

    if line:
        lines = True
        col = "#d3d3d3"
        fig.update_yaxes(rangemode="tozero")
        fig.update_xaxes(rangemode="tozero")
        fig.update_xaxes(range=[0, 20])
    else:
        lines = False
        col = "#FFFFFF"

    fig.update_xaxes(tick0=1, dtick=1)


    fig.update_layout(
        title=dict(text=title, font=dict(size=18, family=Cols.font, color=TITLE_COLOR),
                   x=0.02, y=0.90, xanchor='left', yanchor='top'),
        xaxis=dict(domain=[0, 1], zeroline=False, title=x_axis_title,
                   showline=False, zerolinecolor=col, showticklabels=True, showgrid=False,
                   gridcolor=col, tickfont=dict(color=TITLE_COLOR), linecolor=col,
                   ticks="outside", tickwidth=1, tickcolor=Cols.banner_background, ticklen=10, visible=True),

        yaxis=dict(
            titlefont=dict(color=TITLE_COLOR), tickfont=dict(color=TITLE_COLOR),
            zeroline=lines, zerolinecolor=col, showgrid=True, showline=lines, gridcolor=col, linecolor=col,
            domain=[0, 0.85], ticks="outside", tickwidth=1, tickcolor=Cols.banner_background, ticklen=10,
            automargin=True),
        showlegend=legend, paper_bgcolor=Cols.banner_background, plot_bgcolor=Cols.banner_background,
        margin=dict(l=50, r=20, t=30, b=20),
    )

    if stacked:
        fig.update_layout(barmode='stack')

    return fig
