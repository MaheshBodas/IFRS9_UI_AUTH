import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
from datetime import datetime
import SidePanel.Callbacks.UploadFile_helper as uh
import Utility.Unzip as uz


def upload_file(app):

    # Upload config file
    @app.callback([Output('config-data', 'data'),
                   Output('config-alert', 'is_open'),
                   Output('config-alert', 'children'),
                   Output('config-alert-green', 'is_open'),
                   Output('config-alert-green', 'children'),
                   Output('audit-log', 'value')],
                  [Input({'type': 'scenario-config-uploader', 'index': ALL}, 'filename')],
                  [State({'type': 'scenario-config-uploader', 'index': ALL}, 'contents'),
                   State('user-name', 'data'),
                   State('audit-log', 'value')],
                  prevent_initial_call=True)
    def upload_config_file(filename, contents, username, log):
        if filename is None or contents is None:
            raise PreventUpdate

        if filename[0] is None:
            raise PreventUpdate

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            content_string, option_list, option_list_PD = uh.get_spreadsheet_content(contents)

            if log is None:
                updated_log = now + ", " + username + ": Config file '" + filename[0] + "' uploaded"
            else:
                updated_log = log + "\n" + now + ", " + username + ": Config file '" + filename[0] + "' uploaded"

            return uz.compress(content_string), False, "", True, "Configuration successfully uploaded", updated_log

        except Exception as e:
            options = options = [{'label': 'Error', 'value': 'Error'}],
            error = html.Div(["Error processing file: ", str(e)])

            if log is None:
                updated_log = now + ", " + username + ": Config file '" + filename[0] \
                              + "' upload failure (" + str(e) + ")"
            else:
                updated_log = log + "\n" + now + ", " + username + ": Config file '" + filename[0] \
                              + "' upload failure (" + str(e) + ")"

            return None, True, error, False, "", updated_log
