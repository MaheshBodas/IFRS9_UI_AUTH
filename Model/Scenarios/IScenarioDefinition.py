import pandas as pd
from dateutil import parser
from typing import List
from dateutil.relativedelta import relativedelta
from abc import ABC
from Model.Interfaces.ILinearModel import ILinearModel


class IScenarioDefinition(ABC):
    def __init__(self, scenario_definitions: pd.DataFrame, base_case: pd.DataFrame, variable_Names: List[str],
                 historic_data: pd.DataFrame, reporting_date: str,  total_months: int = 120,
                 full_scenario: bool = True):

        self.timesteps = len(base_case[base_case["Year"] != "Present"]["Year"].tolist())
        self.projectionMonths = self.timesteps * 12
        self.__macroModel = None

        if not full_scenario:
            self.__totalMonths = int(total_months)
            self.__baseCase = base_case
            return
        else:
            if 'Name' not in scenario_definitions.columns or 'Type' not in scenario_definitions.columns \
                    or 'OneInX' not in scenario_definitions.columns:
                raise Exception("Required columns 'Name', 'Type' or 'OneInX' not in DataFrame")

            self.__definitions = scenario_definitions
            self.__historicData = historic_data
            self.__totalMonths = int(total_months)
            self.__baseCase = base_case
            self.__scenarios = None
            self.__date = parser.parse(reporting_date)
            scenarios = ["Base"]
            scenarios.extend(scenario_definitions['Name'].tolist())
            self.__scenario_Names = scenarios
            self.__monthly_scenarios = pd.DataFrame
            self.__variable_Names = variable_Names

    @property
    def macroModel(self):
        return self.__macroModel

    @macroModel.setter
    def macroModel(self, value: ILinearModel):
        self.__macroModel = value

    @property
    def scenarios(self):
        return self.__scenarios

    @scenarios.setter
    def scenarios(self, value: pd.DataFrame):
        pass

    @property
    def monthly_scenarios(self):
        return self.__monthly_scenarios

    @monthly_scenarios.setter
    def monthly_scenarios(self, value: pd.DataFrame):
        self.__monthly_scenarios = value

    @property
    def scenario_Names(self):
        return self.__scenario_Names

    @scenario_Names.setter
    def scenario_Names(self, value: List[str]):
        self.__scenario_Names = value

    @property
    def reporting_Date(self):
        return self.__date

    @reporting_Date.setter
    def reporting_Date(self, value: str):
        self.__date = parser.parse(value)

    @property
    def baseCase(self):
        return self.__baseCase

    @baseCase.setter
    def baseCase(self, value: pd.DataFrame):
        self.__baseCase = value

    @property
    def scenario_definitions(self):
        return self.__definitions

    @property
    def timesteps(self):
        return self.__timesteps

    @timesteps.setter
    def timesteps(self, value: int):
        self.__timesteps = value

    @property
    def historicData(self):
        return self.__historicData

    @historicData.setter
    def historicData(self, value: pd.DataFrame):
        self.__historicData = value

    @property
    def projectionMonths(self):
        return self.__n_months

    @projectionMonths.setter
    def projectionMonths(self, value: int):
        self.__n_months = value

    @property
    def totalMonths(self):
        return self.__totalMonths

    @totalMonths.setter
    def totalMonths(self, value: int):
        self.__totalMonths = value

    @property
    def variable_Names(self):
        return self.__variable_Names

    @variable_Names.setter
    def variable_Names(self, value: List[str]):
        self.__variable_Names = value

    def _linear_interpolation(self):
        df = self.scenarios
        columns = ["Date", "Scenario", "Weight"]
        columns.extend(self.variable_Names)
        new_df = pd.DataFrame(columns=columns)
        years = int(self.projectionMonths / 12)
        total_years = int(self.totalMonths / 12)

        for s in self.scenario_Names:
            scenario = self.scenarios[(self.scenarios['Scenario_Name'] == s)]

            total_months = 0

            for t in range(1, years+1):
                if t == 1:
                    loop_start = 0
                    current = self.baseCase[self.baseCase["Year"] == "Present"]
                else:
                    loop_start = 1

                for m in range(loop_start, 13):
                    record = {"Scenario": s, "Date": self.reporting_Date + relativedelta(months=total_months)}
                    total_months += 1
                    for v in self.variable_Names:
                        if t == 1:
                            # noinspection PyUnboundLocalVariable
                            prev_value = current[v].tolist()[0]
                        else:
                            prev_value = scenario[(scenario['Timestep'] == t - 1)][v].tolist()[0]

                        current_value = scenario[(scenario['Timestep'] == t)][v].tolist()[0]
                        step = (current_value - prev_value) / 12

                        record["Weight"] = scenario[(scenario['Timestep'] == t)]["Weight"].tolist()[0]
                        record[v] = prev_value + (step * m)

                    new_df = new_df.append(record, ignore_index=True)

            record = {}
            for t in range(years+1, total_years + 1):
                for m in range(1, 13):
                    record = {"Scenario": s,
                              "Date": self.reporting_Date + relativedelta(months=total_months),
                              "Weight": scenario[(scenario['Timestep'] == years)]["Weight"].tolist()[0]}

                    for v in self.variable_Names:
                        record[v] = scenario[(scenario['Timestep'] == years)][v].tolist()[0]
                    total_months += 1
                    new_df = new_df.append(record, ignore_index=True)

        new_df["Date_str"] = new_df['Date'].dt.strftime('%d/%m/%Y')
        self.monthly_scenarios = new_df
