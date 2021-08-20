from Model.PD.ITermStructure import ITermStructure
from Model.Scenarios.IScenarioDefinition import IScenarioDefinition
from Model.Interfaces.ILinearModel import ILinearModel
from Model.Scenarios.ExpertScenario import ExpertScenario
from Model.Scenarios.Distributions.IDistribution import IDistribution
import numpy as np
import pandas as pd
from scipy.stats import norm
from typing import List


class PiTPD:
    def __init__(self, master_rating_scale: pd.DataFrame, term_structure: ITermStructure,
                 scenarios: IScenarioDefinition,
                 distribution: IDistribution, beta: float = 1, macro_model: ILinearModel = None):
        if isinstance(scenarios, ExpertScenario):
            if macro_model is None:
                raise Exception("Macro model not set correctly in PiT PD")
            self.__macroModel = macro_model
        else:
            self.__macroModel = scenarios.macroModel
        self.__scenario = scenarios
        self.__ts = term_structure
        self.__distribution = distribution
        self.__macro_impact = None
        self.__masterRatingScale = master_rating_scale
        self.__beta = beta
        self.__pd_term_structures = None
        self.__scenario_Names = scenarios.scenario_Names
        self.__ratings = term_structure.ratings
        self._calculate_macro_adjustment()
        self._calculate_PiT_PDs()

    @property
    def masterRatingScale(self):
        return self.__masterRatingScale

    @masterRatingScale.setter
    def masterRatingScale(self, value: pd.DataFrame):
        self.__masterRatingScale = value

    @property
    def macroModel(self):
        return self.__macroModel

    @macroModel.setter
    def macroModel(self, value: ILinearModel):
        self.__macroModel = value

    @property
    def scenarioDefinitions(self):
        return self.__scenario

    @scenarioDefinitions.setter
    def scenarioDefinitions(self, value: IScenarioDefinition):
        self.__scenario = value

    @property
    def termStructure(self):
        return self.__ts

    @termStructure.setter
    def termStructure(self, value: ITermStructure):
        self.__ts = value

    @property
    def distribution(self):
        return self.__distribution

    @distribution.setter
    def distribution(self, value: IDistribution):
        self.__distribution = value

    @property
    def beta(self):
        return self.__beta

    @beta.setter
    def beta(self, value: float):
        self.__beta = value

    @property
    def macroImpacts(self):
        return self.__macro_impact

    @property
    def PDTermStructures(self):
        return self.__pd_term_structures

    @property
    def scenario_Names(self):
        return self.__scenario_Names

    @scenario_Names.setter
    def scenario_Names(self, value: List[str]):
        self.__scenario_Names = value

    @property
    def ratings(self):
        return self.__ratings

    @ratings.setter
    def ratings(self, value: List[str]):
        self.__ratings = value

    def _calculate_macro_adjustment(self):
        scenarios = self.scenarioDefinitions.monthly_scenarios
        scenarios["Prediction"] = np.nan
        a = 1

        # score up scenario through macro model
        macroVars = {}
        for index, row in scenarios.iterrows():
            for v in self.macroModel.variablesNames:
                if v == "Date":
                    continue
                macroVars[v] = row[v]
            scenarios.loc[index, "Prediction"] = self.macroModel.score_up(macroVars)

        # create scenario macro scalar
        mm = scenarios
        likely_PD = norm.cdf(self.distribution.median)
        scalars = {}

        for s in self.scenario_Names:

            _mm = mm[mm["Scenario"] == s][["Date", "Prediction", "Scenario"]]
            prev_cum = 0
            prev_likely_cum = 0
            for index, row in _mm.iterrows():
                _mm.loc[index, 'cond'] = norm.cdf(row["Prediction"])
                #_mm.loc[index, 'Macro_Scalar'] = \
                #    1 + ((((_mm.loc[index, 'cond'] / 12) / (likely_PD / 12)) - 1) * self.beta)

                # UPDATED: REMOVED SCALAR BASED UPON CUMULATIVE
                if index == 0:
                    _mm.loc[index, 'Cumulative'] = _mm.loc[index, 'cond'] / 12
                    _mm.loc[index, 'Survival'] = 1
                    _mm.loc[index, 'Likely_Cum'] = likely_PD / 12
                    _mm.loc[index, 'Likely_Survival'] = 1

                else:
                    _mm.loc[index, 'Cumulative'] = ((1 - prev_cum) * (_mm.loc[index, 'cond'] / 12)) + prev_cum
                    _mm.loc[index, 'Survival'] = 1 - prev_cum
                    _mm.loc[index, 'Likely_Cum'] = ((1 - prev_likely_cum) * (likely_PD / 12)) + prev_likely_cum
                    _mm.loc[index, 'Likely_Survival'] = 1 - prev_likely_cum

                prev_cum = _mm.loc[index, 'Cumulative']
                prev_likely_cum = _mm.loc[index, 'Likely_Cum']
                _mm.loc[index, 'Macro_Scalar'] = 1 + ((((_mm.loc[index, 'Cumulative'] / _mm.loc[index, 'Likely_Cum']) *
                                                        (_mm.loc[index, 'Survival'] / _mm.loc[
                                                            index, 'Likely_Survival'])) - 1)
                                                      * self.beta)

            _mm = _mm[["Date", "Scenario", "Macro_Scalar"]]
            scalars[s] = _mm.to_json()

        self.__macro_impact = scalars

    def _calculate_PiT_PDs(self):
        ts = self.termStructure.interpolated_term_structures
        mm = self.macroImpacts
        mrs = self.masterRatingScale

        grade_no = 0
        _ts = pd.DataFrame()
        for r in self.ratings:
            if r == "Default":
                continue

            if grade_no == 0:
                _ts = ts[["Date"]]

            _ts[r + '_ts'] = ts[r]  # _mm2 = pd.merge(_mm, _ts, on="Date")
            _ts[r + "_ttc_pd"] = mrs[mrs["Rating"] == r]["PD"].tolist()[0]
            grade_no += 1

        pd_term_structures = pd.DataFrame()
        scenario_no = 0
        for s in self.scenario_Names:
            _pd = pd.merge(pd.read_json(self.macroImpacts[s]), _ts, on="Date")
            for r in self.termStructure.ratings:
                if r == "Default":
                    continue

                _pd[r + '_ttc_ts'] = [1 if x >= 1 else y
                                      for x, y in zip(_pd[r + "_ttc_pd"], (_pd[r + "_ttc_pd"] * _pd[r + "_ts"]))]
                _pd[r + '_pit_pd'] = [1 if x >= 1 else x
                                      for x in _pd[r + '_ttc_ts']]
                _pd[r + '_pit_pd'] = [1 if x >= 1 else y
                                      for x, y in zip(_pd[r + '_pit_pd'], _pd[r + '_ttc_ts'] * _pd['Macro_Scalar'])]
                _pd[r + '_pit_pd'] = [1 if x >= 1 else x
                                      for x in _pd[r + '_pit_pd']]

            if scenario_no == 0:
                pd_term_structures = _pd
            else:
                pd_term_structures = pd_term_structures.append(_pd, ignore_index=True)
            scenario_no += 1

        self.__pd_term_structures = pd_term_structures
