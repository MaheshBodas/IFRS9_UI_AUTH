from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import Utility.Unzip as uz
from datetime import datetime
import json
import SidePanel.Callbacks.UploadFile_helper as uh


def update_controls(app):

    @app.callback(Output('rpt_date', 'data'),
                  Output('audit-log', 'value'),
                  Input({'type': 'reporting-date', 'index': 0}, 'value'),
                  State('rpt_date', 'data'),
                  State('user-name', 'data'),
                  State('audit-log', 'value'))
    def update_reporting_date(control_date, store_date, username, log):
        if control_date == store_date:
            raise PreventUpdate

        if store_date is None:
            return control_date, log

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datetime_object = datetime.strptime(control_date, '%Y-%m-%d')
        reporting_date = datetime_object.strftime('%d/%m/%Y')

        if log is None:
            updated_log = now + ", " + username + ": Reporting date updated to '" + reporting_date + "'"
        else:
            updated_log = log + "\n" + now + ", " + username + ": Reporting date updated to '" + reporting_date + "'"

        return control_date, updated_log

    @app.callback([Output('model_data', 'data'),
                   Output('config-data', 'data')],
                  [Input('user-name', 'data'),],
                  [State('model_data', 'data'),
                   State('config-data', 'data')])
    def on_load(n_clicks, model_data, config_data):
        return model_data, config_data

    # Update region check list
    @app.callback([Output('scenario_checklist', 'options'),
                   Output('scenario_checklist', 'value')],
                  [Input('regions', 'data'),
                   Input('chosen_region', 'data')],
                  prevent_initial_call=True)
    def update_drop_downs(option_list, value):
        if option_list is None:
            raise PreventUpdate
        option = [{'label': name, 'value': name} for name in option_list]
        return option, option_list

    @app.callback(Output('view-analysis-div', 'hidden'),
                  Input('model_data', 'data'))
    def show_analysis_panel(model_data):
        if model_data is None:
            return True
        return False

    @app.callback(Output('scenario-checklist-div', 'hidden'),
                  Output('regions', 'data'),
                  Input('config-data', 'data'))
    def show_configuration_panel(config_data):
        if config_data is None:
            return True, None
        try:
            uncompressed = uz.uncompress(config_data)
            content_string, option_list, option_list_PD = uh.get_spreadsheet_content(uncompressed, True)
            return False, option_list
        except Exception as e:
            options = [{'label': 'Error', 'value': 'Error'}]
            return True, options

    # Update drop-downs with available model data
    @app.callback(Output({'type': 'scenario-dropdown', 'index': 0}, 'options'),
                   Input('model_data', 'data'))
    def update_drop_down_values(model_data):
        if model_data is None:
            raise PreventUpdate

        uncompressed_data = uz.json_unzip(model_data)
        scenarios = json.loads(uncompressed_data['scenarios'])
        options = [{'label': k, 'value': k} for k in scenarios.keys()]

        return options

    @app.callback(Output({'type': 'model-dropdown', 'index': 0}, 'options'),
                  Input({'type': 'scenario-dropdown', 'index': 0}, 'value'),
                  State('model_data', 'data'))
    def update_drop_down_values(region, model_data):
        if model_data is None:
            raise PreventUpdate

        if region is None:
            return {}

        models = json.loads(uz.json_unzip(model_data)['pd_data'])
        options = [{'label': str(k).replace('_', ' '), 'value': k} for k in models.keys() if str(k).startswith(region)]

        return options

