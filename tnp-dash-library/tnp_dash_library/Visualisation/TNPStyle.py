import tnp_dash_library.Visualisation.Theme as Cols

TITLE_COLOR = Cols.dark_blue.get(0)
GRID_COLOR = Cols.white.get(1)
AXIS_COLOR = Cols.light_gray.get(2)
TICK_FONT = Cols.light_gray.get(3)


def style_chart_standard(fig, title: str, legend: bool = True):
    title = '<b>' + title + '</b>'



    return fig
