import plotly.graph_objects as go
from Model.PD.PiTPD import PiTPD
from Visualisations.Styling import TNPColour, ChartGenericStyling as gs
from Model.PD.TransitionMatrix import TransitionMatrix
import numpy as np
from enum import Enum
import plotly.figure_factory as ff
import pandas as pd
import json

colourTheme = TNPColour.TNPColour()

class CURVE(Enum):
    POINT_IN_TIME_PD = "pit_pd"
    PD_TERM_STRUCTURE = "ts"
    TTC_TERM_STRUCTURE = "ttc_ts"
    THROUGH_THE_CYCLE_PD = "ttc_pd"


def plotPDCurveAllScenarios(uncompressed_data, grade: str) -> go.Figure:
    curve = CURVE.POINT_IN_TIME_PD
    field = grade + "_" + str(curve.value)
    accent = 1
    shade = 0
    fig = go.Figure()
    scenario_Names = uncompressed_data["scenarioName"]
    PDTermStructures = pd.read_json(uncompressed_data["PDTermStructures"])

    for s in scenario_Names:
        scenario = PDTermStructures[PDTermStructures['Scenario'] == s]
        data_x = scenario["Date"].tolist()
        data_y = scenario[field].tolist()
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

    gs.update_layout(figure=fig, title="PROJECTED " + curve.name.replace("_", " ") + " - GRADE = " + grade,
                     x_axis_title="Date", y_axis_title=str(curve.name).upper().replace("_", " "),
                     colourTheme=colourTheme, x_axis_format="%b-%y",
                     y_axis_format=".2%", show_x_grid_lines=False, show_y_grid_lines=True)
    fig.update_layout(
        yaxis=dict(domain=[0, 0.95], zeroline=True),
        legend=dict(y=0.97))
    return fig


def plotPDCurveAllGrades(uncompressed_data, scenario) -> go.Figure:

    PDTermStructures = pd.read_json(uncompressed_data["PDTermStructures"])
    ratings = uncompressed_data["ratings"]

    curve = CURVE.POINT_IN_TIME_PD
    accent = 1
    shade = 0
    fig = go.Figure()

    dt = PDTermStructures[PDTermStructures['Scenario'] == scenario]
    for r in ratings:
        if r == "Default":
            continue

        field = r
        data_x = dt["Date"].tolist()
        data_y = dt[field + "_" + curve.value].tolist()
        colour = colourTheme.get_theme_colour(accent, shade)
        fig.add_trace(go.Scatter(
            x=data_x,
            y=data_y,
            name=field,
            connectgaps=True,
            line=dict(color=colour, width=3)
        ))

        accent += 1
        if accent > 6:
            accent = 1
            shade += 1

    gs.update_layout(figure=fig, title="PROJECTED " + curve.name.replace("_", " ") + ": SCENARIO = " + scenario,
                     x_axis_title="Date", y_axis_title=str(curve.name).upper().replace("_", " "),
                     colourTheme=colourTheme, x_axis_format="%b-%y",
                     y_axis_format=".2%", show_x_grid_lines=False, show_y_grid_lines=True)
    fig.update_layout(
        yaxis=dict(domain=[0, 0.95], zeroline=True),
        legend=dict(y=0.97))
    return fig


def plotTermStructures(uncompressed_data) -> go.Figure:
    accent = 1
    shade = 0
    fig = go.Figure()

    curve = CURVE.TTC_TERM_STRUCTURE

    PDTermStructures = pd.read_json(uncompressed_data["PDTermStructures"])
    ratings = uncompressed_data["ratings"]

    dt = PDTermStructures[PDTermStructures['Scenario'] == "Base"]
    for r in ratings:
        if r == "Default":
            continue

        field = r
        data_x = dt["Date"].tolist()
        data_y = dt[field + "_" + curve.value].tolist()
        colour = colourTheme.get_theme_colour(accent, shade)
        fig.add_trace(go.Scatter(
            x=data_x,
            y=data_y,
            name=field,
            connectgaps=True,
            line=dict(color=colour, width=3)
        ))

        accent += 1
        if accent > 6:
            accent = 1
            shade += 1

    gs.update_layout(figure=fig, title="PROJECTED " + curve.name.replace("_", " "),
                     x_axis_title="Date", y_axis_title=str(curve.name).upper().replace("_", " "),
                     colourTheme=colourTheme, x_axis_format="%b-%y",
                     y_axis_format=".2%", show_x_grid_lines=False, show_y_grid_lines=True)
    fig.update_layout(
        yaxis=dict(domain=[0, 0.95], zeroline=True),
        legend=dict(y=0.97))
    return fig


def plotGradeTermStructures(uncompressed_data, grade: str) -> go.Figure:
    accent = 1
    shade = 0
    curve = CURVE.TTC_TERM_STRUCTURE
    fig = go.Figure()

    PDTermStructures = pd.read_json(uncompressed_data["PDTermStructures"])
    ratings = uncompressed_data["ratings"]

    dt = PDTermStructures[PDTermStructures['Scenario'] == "Base"]
    data_x = dt["Date"].tolist()
    data_y = dt[grade + "_" + str(curve.value)].tolist()
    colour = colourTheme.get_theme_colour(accent, shade)
    fig.add_trace(go.Scatter(
        x=data_x,
        y=data_y,
        name=grade,
        connectgaps=True,
        line=dict(color=colour, width=3)
    ))

    accent += 1
    if accent > 6:
        accent = 1
        shade += 1

    gs.update_layout(figure=fig, title="PROJECTED " + curve.name.replace("_", " ") + " GRADE = " + grade,
                     x_axis_title="Date", y_axis_title=str(curve.name).upper().replace("_", " "),
                     colourTheme=colourTheme, x_axis_format="%b-%y",
                     y_axis_format=".2%", show_x_grid_lines=False, show_y_grid_lines=True)
    fig.update_layout(
        yaxis=dict(domain=[0, 0.95], zeroline=True),
        legend=dict(y=0.97))
    return fig


def plotMacroScalars(uncompressed_data) -> go.Figure:

    scenario_Names = uncompressed_data["scenarioName"]
    macroImpacts = json.loads(uncompressed_data["macro_impacts"])

    accent = 1
    shade = 0
    fig = go.Figure()

    for s in scenario_Names:
        scenario = pd.read_json(macroImpacts[s])
        data_x = scenario["Date"].tolist()
        data_y = scenario["Macro_Scalar"].tolist()
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

    gs.update_layout(figure=fig, title="SCENARIO MACRO SCALARS",
                     x_axis_title="Date", y_axis_title="SCALAR",
                     colourTheme=colourTheme, x_axis_format="%b-%y",
                     y_axis_format=".2%", show_x_grid_lines=False, show_y_grid_lines=True)
    fig.update_layout(
        yaxis=dict(domain=[0, 0.95], zeroline=True),
        legend=dict(y=0.97))
    return fig


def plotTransitionMatrix(uncompressed_data, year) -> go.Figure:
    transition_matrix = json.loads(uncompressed_data["matrixmultiplied"])
    grades = uncompressed_data["ratings"]
    df = pd.read_json(transition_matrix[str(year)])
    data = df.values.tolist()
    z_text = np.around(data, decimals=3)

    fig = ff.create_annotated_heatmap(z=data, x=grades, y=grades, annotation_text=z_text,
                                      colorscale=[[0., colourTheme.get_theme_colour(2, 1)],
                                                  [0.01, colourTheme.get_theme_colour(2, 2)],
                                                  [0.05, colourTheme.get_theme_colour(2, 3)],
                                                  [1, colourTheme.get_theme_colour(2, 0)]],
                                      hoverinfo='z')

    gs.update_layout(figure=fig, title="PD TRANSITION MATRIX - YEAR " + str(year),
                     x_axis_title="", y_axis_title="",
                     colourTheme=colourTheme, x_axis_format="",
                     y_axis_format="", show_x_grid_lines=False, show_y_grid_lines=True)
    fig['layout']['yaxis']['autorange'] = "reversed"
    return fig
