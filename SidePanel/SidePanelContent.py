from tnp_dash_library.LayoutLibrary.ToolkitPanel import ToolkitPanel
from tnp_dash_library.SimpleWidgetLibrary.TNPInputBox import TNPInputBox
from tnp_dash_library.SimpleWidgetLibrary.TNPDataUploader import TNPDataUpload
from tnp_dash_library.SimpleWidgetLibrary.TNPDropdown import TNPDropdown
from tnp_dash_library.Enums.TNPENums import LabelPosition
import dash_bootstrap_components as dbc
import dash_html_components as html
from tnp_dash_library.CompositeWidgetLibrary.ContentHolder import TNPContentPanel
import datetime
import dash_core_components as dcc
import SidePanel.Callbacks as cb


def side_panel_content(debug):
    today = datetime.date.today()
    first = today.replace(day=1)
    lastMonth = (first - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    store = html.Div([dcc.Store('config-data', storage_type='session', data=None),
                      dcc.Store('regions', storage_type='session', data=None),
                      dcc.Store('chosen_region', storage_type='session', data=None),
                      dcc.Store('model_data', storage_type='session', data=None),
                      dcc.Store('rpt_date', storage_type='session', data=None)])

    inputBox = TNPInputBox('reporting-date', "Reporting Date:", 'dt', LabelPosition.LEFT, "", "date", 3,
                           lastMonth, debug, 0, "Reporting Date", "text-input")
    uploader = TNPDataUpload('scenario-config-uploader', 'sc-filename', debug, 0,
                             'Model Configuration File ("xlsx", "xlsm" or "xlsb")')
    alert = dbc.Alert(id="config-alert", dismissable=True, is_open=False, color="danger", style={'font-size': '16px'})
    alert_green = dbc.Alert(id="config-alert-green", dismissable=True, is_open=False, color="success",
                            style={'font-size': '16px'})

    model_config = html.Div([html.B("Model Set-Up", style={'font-size': '16px'}),
                             inputBox.layout(), html.Div(uploader.layout(), style={'margin-top': '20px'}), alert,
                             alert_green],
                            id='model-config-div', hidden=False, className="toolkit-frame",
                            style={'margin-top': '10px'})

    store1 = dcc.Store(id="submitted-store")
    store2 = dcc.Store(id="finished-store")
    interval = dcc.Interval(id="interval", interval=500)

    scenario_check = html.Div(
        children=[html.B("Model Configuration", style={'margin-bottom': '20px', 'font-size': '16px'}),
                  dbc.Row(
                      dbc.Col(
                          html.Div(
                              [html.Div(
                                  dbc.DropdownMenu(children=[
                                      dbc.Checklist(options=[], value=[], id='scenario_checklist',
                                                    style={'font-size': '20px'}, className='checkBox')],
                                                    label="Select regions to model",
                                                    bs_size="lg",
                                                    toggleClassName="drop-down-check"),
                                  style={'float': 'left', 'width': '85%', 'margin-right': '2%'}),
                                  html.Div(dcc.Loading(dbc.Button("Run", 'run-model', className='btn_submit'),
                                                       type="circle"),
                                           style={'float': 'left', 'width': '13px'})]
                          ))
                  ),
                  interval,
                  dbc.Collapse(
                      [
                        dbc.Progress(id="progress", color="success", style={'height': '20px'}),
                        html.Div("Running model", id="run-model-log", style={'height': '40px'})
                      ]
                      , id="collapse"
                  ),
                  dbc.Alert("Model has failed to run!!", id="run-alert", dismissable=True,
                            is_open=False, color="danger",
                            style={'font-size': '16px'}),
                  dbc.Alert("Model has run successfully!", id="run-alert-green",
                            dismissable=True, is_open=False, color="success",
                            style={'font-size': '16px'})],
        id='scenario-checklist-div', hidden=True, className="toolkit-frame")

    region_drop_down = TNPDropdown('scenario-dropdown', "Region:", "scenario-portfolio", [],
                                   LabelPosition.LEFT, 4, "", debug, 0,
                                   "Choose region")
    region_button = dbc.Button("\u25B6", 'submit-region', className='btn_modal')

    region_layout = html.Div([region_drop_down.layout(), region_button],
                             style={'padding-right': '15px', 'display': 'flex'})

    model_drop_down = TNPDropdown('model-dropdown', "Model:", "scenario-portfolio", [],
                                  LabelPosition.LEFT, 4, "", debug, 0,
                                  "Choose model")
    model_button = dbc.Button("\u25B6", 'submit-model', className='btn_modal')
    model_layout = html.Div([model_drop_down.layout(), model_button],
                            style={'padding-right': '15px', 'display': 'flex'})

    view_analysis = html.Div([html.B("Analysis Views", style={'font-size': '16px', 'margin-bottom': '20px'}),
                              region_layout, model_layout],
                             id='view-analysis-div', hidden=True, className="toolkit-frame",
                             style={'margin-top': '10px'})

    layout2 = html.Div([model_config, scenario_check, view_analysis, store, store1, store2])
    content = TNPContentPanel('side-panel-content', layout2)
    tool_kit_panel = ToolkitPanel('main-control', "Model Control Panel", [content])
    return tool_kit_panel


# HACK: To Get this to work, this function must be called from one of the content callback methods
# Added to ConfigurationUpload.py
def side_panel_call_backs(app):
    cb.upload_file(app)
    cb.run_model(app)
    cb.update_controls(app)
