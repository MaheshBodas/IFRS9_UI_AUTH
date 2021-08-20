from Model.Scenarios.Distributions import Gumbel as gm
import Model.Interfaces.ILinearModel as lm
import Model.Scenarios.CyclicalityIndex as ci
import pandas as pd
import json
import Visualisations.ScenarioCharts as sc
import Visualisations.Styling.TNPColour as tnp
from typing import Dict


def generateScenarios(historic_default_rates: str, ci_model_coefficients: str, historical_macro_variables: str,
                      base_case_projections: str, scenario_definitions: str, reporting_date: str,
                      distribution: str = "gumbel", total_months: int = 120) -> Dict[str, str]:
    # Load data to dataframes
    DR_Data = pd.read_json(historic_default_rates)['Default_rate'].tolist()
    df1 = pd.read_json(base_case_projections)
    df2 = pd.read_json(ci_model_coefficients)
    df3 = pd.read_json(scenario_definitions)
    df4 = pd.read_json(historical_macro_variables)

    # Fit distribution
    if distribution == "gumbel":
        dist = gm.Gumbel()
    else:
        dist = gm.Gumbel()

    dist.historic_DR = DR_Data
    dist.fitDistribution()

    lin_model_scenario = lm.ILinearModel(df1, df2)
    lin_model_historic = lm.ILinearModel(df4, df2)

    #  CI Scenarios
    c_index = ci.CyclicalityIndex(df3, df1, lin_model_historic, df4, reporting_date, total_months)
    dist.CiProbability_from_Definition(lin_model_scenario.projections[1:], c_index)

    #  Grid Search for scenario
    c_index.findScenarios()

    # Chart outputs
    theme = tnp.TNPColour()
    distribution_fit_chart = sc.plotDistributionFit(dist, theme)
    ci_time_series = sc.plotCI_projections(c_index, dist, theme)
    macro_projections = sc.plot_all_scenarios(c_index, theme)

    return_data = {"scenarios": c_index.scenarios.to_json(), "monthly_scenarios": c_index.monthly_scenarios.to_json(),
                   "distribution": json.dumps(dist.parameters), "distribution_fit_chart": distribution_fit_chart,
                   "ci_time_series": ci_time_series, "macro_projections": macro_projections}

    return return_data


def generateAllRegions(packaged_data: str) -> Dict[str, Dict[str, str]]:
    data = {}
    pack_dict = json.loads(packaged_data)
    for k in pack_dict.keys():
        historic_default_rates = pack_dict[k]["historic_default_rates"]
        ci_model_coefficients = pack_dict[k]["ci_model_coefficients"]
        historical_macro_variables = pack_dict[k]["historical_macro_variables"]
        base_case_projections = pack_dict[k]["base_case_projections"]
        scenario_definitions = pack_dict[k]["scenario_definitions"]
        reporting_date = pack_dict[k]["reporting_date"]
        distribution = pack_dict[k]["distribution"]
        total_months = int(pack_dict[k]["total_months"])

        data[k] = generateScenarios(historic_default_rates, ci_model_coefficients, historical_macro_variables,
                                    base_case_projections, scenario_definitions, reporting_date, distribution,
                                    total_months)

    return data
