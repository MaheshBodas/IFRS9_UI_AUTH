import base64
import dash_core_components as dcc
import requests
import json
from app import Dashboard
import time
import Utility.Excel as xl
import Model.PD.PDFunctions as pdfunc



TOTAL_MONTHS = 120

# Run all models
def run_pd_models(data, regions, reporting_date):
    BASE = Dashboard.API
    decoded = base64.b64decode(data)
    scenario_package = {}
    run_models = []


    for r in regions:
        bc, dd, dr, mm, sd, pf = create_scenario_dataframes_from_data(data, r)

        scenario_package[r] = json.dumps({"historic_default_rates": dr, "ci_model_coefficients": mm,
                                          "historical_macro_variables": dd, "base_case_projections": bc,
                                          "scenario_definitions": sd, "reporting_date": reporting_date,
                                          "distribution": "gumbel", "total_months": str(TOTAL_MONTHS),
                                          "portfolios": pf})

        run_models.extend(pf)

    pd_package = {}
    for m in run_models:
        if m not in pd_package.keys():

            mrs, ts_type, matrix = create_pd_dataframes_from_data(data, m)
            pd_package[m] = json.dumps({"term_structure": matrix, "master_rating_scale": mrs,
                                        "approach": ts_type, "reporting_date": reporting_date,
                                        "total_months": str(TOTAL_MONTHS)})

    package = {"scenario_package": json.dumps(scenario_package), "pd_package": json.dumps(pd_package),
               "multiThread": "True"}

    start_time = time.time()
    response = pdfunc.generateAllPDTermStructures(json.dumps(scenario_package), json.dumps(pd_package), False)
    run_time = "--- %s seconds ---" % round((time.time() - start_time), 2)
    return response, run_time


def create_scenario_dataframes_from_data(data, sheet, asJson=True):
    decoded = base64.b64decode(data)
    mm = xl.from_byte(decoded, 'Scenario_' + sheet, 2, 'C:I')
    bc = xl.from_byte(decoded, 'Scenario_' + sheet, 2, 'K:Q')
    dr = xl.from_byte(decoded, 'Scenario_' + sheet, 2, 'S:T')
    sd = xl.from_byte(decoded, 'Scenario_' + sheet, 2, 'V:X')
    dd = xl.from_byte(decoded, 'Scenario_' + sheet, 2, 'Z:AF')
    _pf = xl.from_byte(decoded, 'Scenario_' + sheet, 2, 'AH:AH')
    pf = list(_pf['Portfolios'].values)

    if not asJson:
        return bc, dd, dr, mm, sd, pf
    else:
        return bc.to_json(), dd.to_json(), dr.to_json(), mm.to_json(), sd.to_json(), pf


def create_pd_dataframes_from_data(data, sheet):
    decoded = base64.b64decode(data)
    mrs = xl.from_byte(decoded, 'PD_' + sheet, 2, 'B:C').to_json()
    _ts_type = xl.from_byte(decoded, 'PD_' + sheet, 2, 'E:E')
    matrix = xl.from_byte(decoded, 'PD_' + sheet, 2, 'G:AL', False)
    ts_type = list(_ts_type['Type'].values)[0]
    matrix.columns = matrix.columns.str.replace('Rating.1', 'Rating')
    return mrs, ts_type, matrix.to_json()
