import pandas as pd
from Model.Scenarios.IScenarioDefinition import IScenarioDefinition


class ExpertScenario(IScenarioDefinition):
    def __init__(self, base_case: pd.DataFrame, scenario_definition: pd.DataFrame, reporting_date: str,
                 total_months: int = 120):
        super().__init__(None, base_case, None, None, reporting_date, total_months, False)

        self.reporting_Date = reporting_date
        self.scenarios = scenario_definition

    @property
    def scenarios(self):
        return self.__scenarios

    @scenarios.setter
    def scenarios(self, value: pd.DataFrame):
        self.__scenarios = value
        self.scenario_Names = value['Scenario_Name'].unique().tolist()
        var_list = value.columns.tolist()

        for n in ["Weight", "Timestep", "Scenario_Name", "CI"]:
            if n in var_list:
                var_list.remove(n)

        self.variable_Names = var_list
        self._linear_interpolation()
