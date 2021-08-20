import base64
import json
import queue
import threading
import zlib

import pandas as pd

import Model.Interfaces.ILinearModel as lm
import Model.Scenarios.CyclicalityIndex as ci
import Visualisations.PDCharts as pdc
import Visualisations.ScenarioCharts as sc
import Visualisations.Styling.TNPColour as tnp
from Model.PD.ExpertTermStructure import ExpertTermStructure
from Model.PD.PiTPD import PiTPD
from Model.PD.TransitionMatrix import TransitionMatrix
from Model.Scenarios.Distributions import Gumbel as gm
from rq import get_current_job
import SidePanel.Callbacks.RunModel as rm


class PDCalculator:
    def __init__(self, scenario_dictionary, pd_dictionary):
        self.__scenario_dictionary = json.loads(scenario_dictionary)
        self.__pd_dictionary = json.loads(pd_dictionary)
        self.__total_count = len(self.scenario_dictionary) + len(self.__pd_dictionary) + 1
        self.__theme = tnp.TNPColour()
        self.__pd_data = {}
        self.__scenario_data = {}
        self.__return_data = {}
        self.__run = 0
        self.__progress = 0

    @property
    def scenario_dictionary(self):
        return self.__scenario_dictionary

    @property
    def pd_dictionary(self):
        return self.__pd_dictionary

    @property
    def theme(self):
        return self.__theme

    @property
    def pd_data(self):
        return self.__pd_data

    @property
    def scenario_data(self):
        return self.__scenario_data

    @property
    def return_data(self):
        return self.__return_data

    @property
    def count(self):
        return self.__total_count

    @property
    def run(self):
        return self.__run

    @property
    def progrss(self):
        return self.__progress

    def calculate(self, multiThread=True):

        if not rm.TEST:
            job = get_current_job()
            job.meta["progress"] = 0
            job.save_meta()

        scenario_process = []
        que1 = queue.Queue()

        for region in self.scenario_dictionary:

            if multiThread:
                p1 = threading.Thread(target=lambda q, arg1: q.put(self._run_region(region, multiThread)),
                                      args=(que1, region))
                scenario_process.append(p1)
                p1.start()
            else:
                self._run_region(region, multiThread)

        if multiThread:
            for p in scenario_process:
                p.join()

        self.__return_data = {'scenarios': json.dumps(self.scenario_data),
                              'pd_data': json.dumps(self.pd_data)}

    def _run_region(self, region, multiThread=True):
        print("Running Scenario: " + region)
        self.__run += 1
        self.__progress = int(round(round(self.run / self.count, 2) * 100,0))

        c_index, dist, portfolios = self._scenario_calculation(region)

        if not rm.TEST:
            job = get_current_job()
            print("------------------- PROGRESS = " + str(self.__progress) + "%")
            job.meta["progress"] = self.__progress
            job.save_meta()


        pd_process = []
        que2 = queue.Queue()
        for model in portfolios:
            if multiThread:
                p2 = threading.Thread(target=lambda q,
                                                    arg1: q.put(
                    self._run_model(model, region, c_index, dist)),
                                      args=(que2, [model, region, c_index, dist]))
                pd_process.append(p2)
                p2.start()
            else:
                self._run_model(model, region, c_index, dist)

        if multiThread:
            for p in pd_process:
                p.join()

    def _run_model(self, model, region, c_index, dist):
        print("Running PD Model: " + region + ", " + model)
        self._pd_calculation(model, region, c_index, dist)
        self.__run += 1
        self.__progress = int(round(round(self.run / self.count, 2) * 100, 0))

        if not rm.TEST:
            job = get_current_job()
            print("------------------- PROGRESS = " + str(self.__progress) + "%")
            job.meta["progress"] = self.__progress
            job.save_meta()

    def _scenario_calculation(self, region):

        if not rm.TEST:
            job = get_current_job()
            job.meta["status"] = "Running " + region + " scenario: Reading Data"
            job.save_meta()

        historic_default_rates = json.loads(self.scenario_dictionary[region])["historic_default_rates"]
        ci_model_coefficients = json.loads(self.scenario_dictionary[region])["ci_model_coefficients"]
        historical_macro_variables = json.loads(self.scenario_dictionary[region])["historical_macro_variables"]
        base_case_projections = json.loads(self.scenario_dictionary[region])["base_case_projections"]
        scenario_definitions = json.loads(self.scenario_dictionary[region])["scenario_definitions"]
        reporting_date = json.loads(self.scenario_dictionary[region])["reporting_date"]
        distribution = json.loads(self.scenario_dictionary[region])["distribution"]
        total_months = int(json.loads(self.scenario_dictionary[region])["total_months"])
        portfolios = json.loads(self.scenario_dictionary[region])["portfolios"]

        DR_Data = pd.read_json(historic_default_rates)['Default_rate'].tolist()
        df1 = pd.read_json(base_case_projections)
        df2 = pd.read_json(ci_model_coefficients)
        df3 = pd.read_json(scenario_definitions)
        df4 = pd.read_json(historical_macro_variables)

        if distribution == "gumbel":
            dist = gm.Gumbel()
        else:
            dist = gm.Gumbel()

        if not rm.TEST:
            job = get_current_job()
            job.meta["status"] = "Running " + region + " scenario: Fitting distribution"
            job.save_meta()

        dist.historic_DR = DR_Data
        dist.fitDistribution()

        lin_model_scenario = lm.ILinearModel(df1, df2)
        lin_model_historic = lm.ILinearModel(df4, df2)

        #  CI Scenarios
        if not rm.TEST:
            job = get_current_job()
            job.meta["status"] = "Running " + region + " scenario: Finding scenario CIs"
            job.save_meta()
        c_index = ci.CyclicalityIndex(df3, df1, lin_model_historic, df4, reporting_date, total_months)
        dist.CiProbability_from_Definition(lin_model_scenario.projections[1:], c_index)

        #  Grid Search for scenario
        if not rm.TEST:
            job = get_current_job()
            job.meta["status"] = "Running " + region + " scenario: Finding macro economic variables"
            job.save_meta()
        c_index.findScenarios()

        self.__scenario_data[region] = {"scenarios": c_index.scenarios.to_json(),
                                        "monthly_scenarios": c_index.monthly_scenarios.to_json(),
                                        "distribution": json.dumps(dist.parameters),
                                        "high_low_range_interval": [dist.range_high, dist.range_low, dist.range, dist.interval],
                                        "historic_ci": dist.historic_CI.tolist(),
                                        "name": dist.name,
                                        "historicData": c_index.historicData.to_json(),
                                        "scenarioName": c_index.scenario_Names,
                                        "variables": c_index.variable_Names
                                        }
        return c_index, dist, portfolios

    def _pd_calculation(self, model, region, c_index, dist):

        if not rm.TEST:
            job = get_current_job()
            job.meta["status"] = "Running " + region + ", " + model + " PD model: Reading Data"
            job.save_meta()

        term_structure = pd.read_json(json.loads(self.pd_dictionary[model])["term_structure"])
        master_rating_scale = pd.read_json(json.loads(self.pd_dictionary[model])["master_rating_scale"])
        approach = json.loads(self.pd_dictionary[model])["approach"]
        reporting_date = json.loads(self.pd_dictionary[model])["reporting_date"]
        total_months = int(json.loads(self.pd_dictionary[model])["total_months"])

        tm = None

        if not rm.TEST:
            job = get_current_job()
            job.meta["status"] = "Running " + region + ", " + model + " PD model: Calculating Term Structures"
            job.save_meta()

        if approach == "Matrix":
            tm = TransitionMatrix(term_structure, reporting_date)
        else:
            tm = ExpertTermStructure(term_structure, int(total_months / 12))

        if not rm.TEST:
            job = get_current_job()
            job.meta["status"] = "Running " + region + ", " + model + " PD model: Calculating PiT PDs"
            job.save_meta()
        _pd = PiTPD(master_rating_scale, tm, c_index, dist)

        # return data
        self.__pd_data[region + "_" + model] = {"macro_impacts": json.dumps(_pd.macroImpacts),
                                                "PDTermStructures": _pd.PDTermStructures.to_json(),
                                                "ratings": _pd.ratings.tolist(),
                                                "scenarioName": c_index.scenario_Names,
                                                "matrixmultiplied": tm.matrix_multiplied_json}


def generateAllPDTermStructures(scenario_data, pd_data,  multiThread=True):
    try:

        calc = PDCalculator(scenario_data, pd_data)
        calc.calculate(multiThread)

        if not rm.TEST:
            job = get_current_job()
            job.meta["status"] = "Packaging return data"
            job.save_meta()

        return json_zip(calc.return_data)

    except Exception as e:

        if not rm.TEST:
            job = get_current_job()
            job.meta["status"] = "Packaging return data"
            job.save_meta()

        return json_zip("Error " + str(e))

ZIPJSON_KEY = 'base64(zip(o))'

def json_zip(j):
    j = {
        ZIPJSON_KEY: base64.b64encode(
            zlib.compress(
                json.dumps(j).encode('utf-8')
            )
        ).decode('ascii')
    }

    return j
