import dash_html_components as html
import SidePanel.Callbacks.RunModel_helper as rm
import Styling.DataTable as dt
from Styling import TNPColour
import Utility.Unzip as uz


def get_scenario_specification_inputs(region, data, as_json=True):
    theme = TNPColour.TNPColour()

    uncompressed = uz.uncompress(data)

    bc, dd, dr, mm, sd, pf = rm.create_scenario_dataframes_from_data(uncompressed, region, as_json)
    coefficients, base_case, scenario_def, def_rate, macro = \
        create_parameter_table_objects(bc, dd, dr, mm, sd, theme)
    inputs = html.Div([html.Div([html.B("1. Macro Model:"), coefficients], style={'margin-top': '20px'}),
                       html.Div([html.B("2. Base Case:"), base_case], style={'margin-bottom': '20px'}),
                       html.Div([html.B("3. Scenario Definitions:"), scenario_def],
                                style={'margin-bottom': '20px'}),
                       html.Div([html.B("4. Historic Default Rates:"), def_rate],
                                style={'margin-bottom': '40px'}),
                       html.Div([html.B("5. Historic Macro Variables:"), macro],
                                style={'margin-bottom': '20px'})], )
    ui_input = html.Div(inputs, style={'height': '30vh', 'padding-right': '10px'}, className='scrollable')
    modal_input = html.Div(inputs, style={'height': '70vh', 'padding': '10px'}, className='scrollable')
    return modal_input, ui_input


def create_parameter_table_objects(bc, dd, dr, mm, sd, theme):
    coefficients = dt.define_data_table_object('coefficients', mm, 50, theme, 100, None, None, False)
    base_case = dt.define_data_table_object('base_case', bc, 50, theme, 230, None, None, False)
    scenarios = dt.define_data_table_object('base_case', sd, 50, theme, 230, None, None, False)
    def_rate = dt.define_data_table_object('base_case', dr, 10000, theme, 360, None, None, False)
    macro = dt.define_data_table_object('base_case', dd, 10000, theme, 360, None, None, False)
    return coefficients, base_case, scenarios, def_rate, macro