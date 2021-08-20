import Model.Scenarios.Distributions.IDistribution as IDist
import scipy
import scipy.stats as st
from scipy.stats import gumbel_r
from typing import List, Dict
import Model.Scenarios.CyclicalityIndex as cyc_ind
import pandas as pd


class Gumbel(IDist.IDistribution):

    def __init__(self):
        super().__init__()
        self.name = 'gumbel_r'

    def fitDistribution(self):
        if self.historic_CI is None:
            raise Exception("Data to fit the distribution to has not been assigned")
        else:
            data = self.historic_CI
            self.distribution = getattr(scipy.stats, self.name)
            params = self.distribution.fit(data)
            self.parameters['mu'] = params[0]
            self.parameters['sigma'] = params[1]
            self.fitted = True
            self._findMedian()

    def CiProbability_from_Definition(self, baseCaseCI: List[float], scenarios: cyc_ind.CyclicalityIndex) -> None:
        if self.fitted:
            weights = []
            df = pd.DataFrame(columns=['Scenario_Name', 'Timestep', 'Weight', 'CI'])

            for index, row in scenarios.scenario_definitions.iterrows():
                time = 1
                name = row['Name']
                confidenceInterval = row['Confidence']

                for base_ci in baseCaseCI:
                    ci, weight = self._calculate_weight_and_Z(base_ci, confidenceInterval)
                    df = df.append({'Scenario_Name': name, 'Timestep': time, 'Weight': weight, 'CI': ci},
                                   ignore_index=True)
                    time += 1

            time = 1
            for base_ci in baseCaseCI:

                df = df.append({'Scenario_Name': 'Base', 'Timestep': time, 'Weight': 0, 'CI': base_ci},
                               ignore_index=True)
                time += 1

            scenarios.scenarios = df
        else:
            raise Exception("Distribution has not been fitted")

    def CiProbability(self, baseCaseCI: List[float], confidenceInterval: float) -> List[Dict[str, float]]:
        if self.fitted:
            weights = []
            index = 1

            for base_ci in baseCaseCI:
                scenario_ci, weight = self._calculate_weight_and_Z(base_ci, confidenceInterval)
                scenario = {"T": index, "CI": scenario_ci, "weight": weight}
                weights.append(scenario)
                index += 1

            return weights
        else:
            raise Exception("Distribution has not been fitted")

    def _findMedian(self):
        if self.fitted:
            # updated implementation to mean
            self.median = gumbel_r.mean(self.parameters['mu'], self.parameters['sigma'])
        else:
            raise Exception("Distribution has not been fitted")

    def _calculate_weight_and_Z(self, base_ci, confidenceInterval):
        p_bc = gumbel_r.cdf(base_ci, self.parameters['mu'], self.parameters['sigma'])
        # get worse: right hand tail
        if confidenceInterval <= 0.5:
            p_scenario = (1 - confidenceInterval) * (1 - p_bc) + p_bc
            scenario_ci = gumbel_r.ppf(p_scenario, self.parameters['mu'], self.parameters['sigma'])
            weight = 1 - gumbel_r.cdf(scenario_ci, self.parameters['mu'], self.parameters['sigma'])
        # get better: left hand tail
        else:
            p_scenario = -(confidenceInterval * p_bc - p_bc)
            scenario_ci = gumbel_r.ppf(p_scenario, self.parameters['mu'], self.parameters['sigma'])
            weight = gumbel_r.cdf(scenario_ci, self.parameters['mu'], self.parameters['sigma'])
        return scenario_ci, weight
