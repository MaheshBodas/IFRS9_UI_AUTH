import plotly.graph_objects as go
from Model.Scenarios.Distributions.IDistribution import IDistribution
from Visualisations.Styling import TNPColour, ChartGenericStyling as gs
import numpy as np
from scipy.stats import gumbel_r
from Model.Scenarios import IScenarioDefinition
from plotly.subplots import make_subplots
import json
import pandas as pd

colourTheme = TNPColour.TNPColour()


def plotDistributionFit(uncompressed_data) -> go.Figure:
    line_colour = colourTheme.get_theme_colour(3, 0)
    hist_colour = colourTheme.get_theme_colour(1, 0)

    range_high = uncompressed_data["high_low_range_interval"][0]
    range_low = uncompressed_data["high_low_range_interval"][1]
    range = uncompressed_data["high_low_range_interval"][2]
    interval = uncompressed_data["high_low_range_interval"][3]
    parameters = json.loads(uncompressed_data["distribution"])
    name = uncompressed_data["name"]
    historic_CI = uncompressed_data["historic_ci"]

    # GET PLOT DATA
    x = np.linspace(range_low, range_high, range)

    if name == "gumbel_r":
        y = gumbel_r.pdf(x, parameters['mu'], parameters['sigma'])
        name = "Gumbel Probability Density Function (\u03BC = " + "{:.3f}".format(parameters['mu']) \
               + ", \u03C3 = " + "{:.3f}".format(parameters['sigma']) + ")"
    else:
        # other distributions here
        y = gumbel_r.pdf(x, parameters['mu'], parameters['sigma'])
        name = "Gumbel Probability Density Function (\u03BC = " + "{:.3f}".format(parameters['mu']) \
               + ", \u03C3 = " + "{:.3f}".format(parameters['sigma']) + ")"

    y1 = y / np.sum(y)

    # ADD DATA SERIES
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y1,
        name=name,
        connectgaps=True,
        line=dict(color=line_colour, width=4)
    ))
    fig.add_trace(go.Histogram(
        x=historic_CI,
        histnorm='probability',
        opacity=0.2,
        marker_color=hist_colour,
        name="Observed Cyclicality Index",
        xbins=dict(start=range_low, end=range_high, size=interval)
    ))

    # STYLE PLOT
    fig.update_layout(bargroupgap=0.1)
    gs.update_layout(figure=fig, title="FITTED CYCLICALITY INDEX DISTRIBUTION", x_axis_title="Cyclicality Index",
                     y_axis_title="", colourTheme=colourTheme, y_axis_format=".0%")
    return fig


def plotCI_projections(uncompressed_data) -> go.Figure:
    historic_colour = colourTheme.get_dark_grey(0)

    historic_data_x = pd.read_json(uncompressed_data["historicData"])['Date'].tolist()
    historic_data_y = uncompressed_data["historic_ci"]
    scenarios = pd.read_json(uncompressed_data["scenarios"])
    scenario_Names = uncompressed_data["scenarioName"]

    # ADD DATA SERIES
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=historic_data_x,
        y=historic_data_y,
        name="Historic Cyclicality Index",
        connectgaps=True,
        line=dict(color=historic_colour, width=4, dash='dot')
    ))

    accent = 1
    shade = 0
    for s in scenario_Names:
        scenario = scenarios[(scenarios['Scenario_Name'] == s)]
        data_x = scenario["Date"].tolist()
        data_y = scenario["CI"].tolist()

        data_y.insert(0, historic_data_y[-1])
        data_x.insert(0, historic_data_x[-1])

        colour = colourTheme.get_theme_colour(accent, shade)
        fig.add_trace(go.Scatter(
            x=data_x,
            y=data_y,
            name=s,
            connectgaps=True,
            line=dict(color=colour, width=3)
        ))

        accent += 1
        if accent > 6:
            accent = 1
            shade += 1

    gs.update_layout(figure=fig, title="PROJECTED CYCLICALITY INDEX", x_axis_title="Date",
                     y_axis_title="Cyclicality Index", colourTheme=colourTheme, x_axis_format="%b-%y",
                     y_axis_format=".2f", show_x_grid_lines=False, show_y_grid_lines=True)

    return fig


def plot_all_scenarios(uncompressed_data) -> go.Figure:
    scenario_Names = uncompressed_data["scenarioName"]
    monthly_scenarios = pd.read_json(uncompressed_data["monthly_scenarios"])
    historicData = pd.read_json(uncompressed_data["historicData"])
    variable_Names = uncompressed_data["variables"]

    cols = 1
    rows = len(variable_Names)

    fig = make_subplots(
        rows=rows, cols=cols, shared_xaxes=True)

    col = 1
    row = 1

    for v in variable_Names:

        legend = row == 1

        historic_colour = colourTheme.get_dark_grey(0)
        historic_data_x = historicData['Date'].tolist()
        historic_data_y = historicData[v].tolist()
        fig.add_trace(go.Scatter(
            x=historic_data_x,
            y=historic_data_y,
            name="Observed",
            connectgaps=True,
            line=dict(color=historic_colour, width=4, dash='dot'),
            showlegend=legend,
            legendgroup="Observed"
        ), row=row, col=col)

        accent = 1
        shade = 0
        for s in scenario_Names:
            scenario = monthly_scenarios[(monthly_scenarios["Scenario"] == s)]
            data_x = scenario["Date"].tolist()
            data_y = scenario[v].tolist()
            weights = scenario["Weight"].tolist()

            data_y.insert(0, historic_data_y[-1])
            data_x.insert(0, historic_data_x[-1])
            weights.insert(0, np.nan)

            colour = colourTheme.get_theme_colour(accent, shade)
            fig.add_trace(go.Scatter(
                x=data_x,
                y=data_y,
                name=s,
                connectgaps=True,
                line=dict(color=colour, width=3),
                showlegend=legend,
                customdata=weights,
                legendgroup=s,
                hovertemplate='<b>Date:%{x}</b><br>Value:%{y:.3f}<br>Scenario Weight: %{customdata:.2%}',
            ), row=row, col=col)

            accent += 1
            if accent > 6:
                accent = 1
                shade += 1

        col += 1
        if col > cols:
            row += 1
            col = 1

    chart_background = colourTheme.get_white(0)
    grid_colour = colourTheme.get_light_grey(1)
    title_colour = colourTheme.get_theme_colour(1, 0)
    main_title = '<b>SCENARIO PROJECTIONS</b>'

    col = 1
    row = 1
    for v in variable_Names:
        x_title = "Date" if row == rows else ""
        fig.update_xaxes(dict(zeroline=False, title=x_title,
                              showline=False, showticklabels=row == rows,
                              showgrid=False,
                              tickfont=dict(color=title_colour, family=colourTheme.font), linecolor=grid_colour,
                              ticks="outside", tickwidth=1, tickcolor=chart_background, ticklen=10, visible=True,
                              tickformat="%b-%y"), row=row, col=col)
        fig.update_yaxes(
            dict(tickfont=dict(color=title_colour), title=v,
                 zeroline=True, zerolinecolor=grid_colour, showgrid=True,
                 showline=True, gridcolor=grid_colour, linecolor=grid_colour,
                 ticks="outside", tickwidth=1, tickcolor=chart_background, ticklen=10), row=row, col=col
        )
        col += 1
        if col > cols:
            row += 1
            col = 1

    fig.update_layout(
        title=dict(text=main_title, font=dict(size=18, family=colourTheme.font, color=title_colour),
                   xanchor='left', yanchor='top'), showlegend=True, paper_bgcolor=chart_background,
        plot_bgcolor=chart_background, legend=dict(font=dict(size=15, family=colourTheme.font, color=title_colour))
    )

    return fig
