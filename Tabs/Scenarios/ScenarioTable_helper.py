import Styling.DataTable as dt
import Utility.Unzip as uz
import json
import pandas as pd
from Styling import TNPColour
import dash_html_components as html


def get_scenario_tables(model_data, region):
    theme = TNPColour.TNPColour()

    uncompressed_data = json.loads(uz.json_unzip(model_data)['scenarios'])[region]
    ms = pd.read_json(uncompressed_data['monthly_scenarios'])
    sn = pd.read_json(uncompressed_data['scenarios'])

    annual1, monthly1, annual2, monthly2 = create_table_objects(ms, sn, theme)

    a1 = html.Div(annual1, style={'height': '32vh'})
    m1 = html.Div(monthly1, style={'height': '32vh'})
    a2 = html.Div(annual2, style={'height': '72vh'})
    m2 = html.Div(monthly2, style={'height': '72vh'})

    monthly_modal = html.Div([monthly2], id='monthly2-scenario-table-container', style={"height": '72vh'})
    annual_modal = html.Div([annual2], id='annual2-scenario-table-container', style={"height": '72vh'},
                            hidden=True)
    modal = html.Div([monthly_modal, annual_modal])
    return a1, m1, modal


def create_table_objects(ms, sn, theme):

    ms["Date"] = ms["Date_str"]
    ms = ms.drop(columns=["Date_str"])

    sn["Date"] = sn["Date_str"]
    sn = sn.drop(columns=["Date_str"])
    sn = sn.drop(columns=["Timestep"])
    sn = sn.rename(columns={"Scenario_Name": "Scenario Name"})
    variable_list = sn.columns[4:]
    cols = ["Date", "Scenario Name", "Weight", "CI"]
    cols.extend(variable_list)
    new_df = sn[cols]
    sn = new_df

    monthly1 = dt.define_data_table_object('monthly1-scenario-projection-table', ms, 61, theme, 24, None, None, False,
                                           True)
    annual1 = dt.define_data_table_object('annual1-scenario-projection-table', sn, 61, theme, 27, None, None, False,
                                          True)
    monthly2 = dt.define_data_table_object('monthly2-scenario-projection-table', ms, 61, theme, 63, None, None, True,
                                           True)
    annual2 = dt.define_data_table_object('annual2-scenario-projection-table', sn, 61, theme, 68, None, None, True,
                                          True)

    return annual1, monthly1, annual2, monthly2
