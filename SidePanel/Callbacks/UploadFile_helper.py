import base64
import Utility.Excel as xl


# Get xlsx config file contents and helper functions
def get_spreadsheet_content(contents, decode=False):
    if decode:
        content_string = contents
    else:
        content_type, content_string = contents[0].split(',')

    decoded = base64.b64decode(content_string)
    sheets = xl.get_list_of_sheets(decoded)
    option_list = [name.replace("Scenario_", "") for name in sheets if "Scenario" in name]
    option_list_PD = [name.replace("PD_", "") for name in sheets if "PD" in name]
    return content_string, option_list, option_list_PD