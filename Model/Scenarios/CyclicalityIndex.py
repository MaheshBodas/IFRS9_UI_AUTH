import pandas as pd
from Model.Scenarios.IScenarioDefinition import IScenarioDefinition
from Model.Interfaces.ILinearModel import ILinearModel
import numpy as np
from dateutil.relativedelta import relativedelta


class CyclicalityIndex(IScenarioDefinition):
    def __init__(self, scenario_definitions: pd.DataFrame, base_case: pd.DataFrame, macro_model: ILinearModel,
                 historic_data: pd.DataFrame, reporting_date: str, total_months: int = 120):
        super().__init__(scenario_definitions, base_case, macro_model.variablesNames, historic_data, reporting_date,
                         total_months)
        scenario_definitions['Confidence'] = scenario_definitions.apply(CyclicalityIndex.f, axis=1)

        ds_ci = CyclicalityIndex.min_ge(scenario_definitions['Confidence'].tolist(), 0.5)
        us_ci = CyclicalityIndex.max_le(scenario_definitions['Confidence'].tolist(), 0.5)
        self.__fds = scenario_definitions[scenario_definitions['Confidence'] == ds_ci]['Name'].tolist()[0]
        self.__fus = scenario_definitions[scenario_definitions['Confidence'] == us_ci]['Name'].tolist()[0]
        self.macroModel = macro_model
        self.__grid = pd.DataFrame

    @property
    def scenarios(self):
        return self.__scenarios

    @scenarios.setter
    def scenarios(self, value: pd.DataFrame):
        if self.timesteps == 0:
            raise Exception("Number of timesteps not set")

        for t in range(1, self.timesteps+1):

            timestep = value.query('Timestep==' + str(t))
            up_weight = timestep.query('Scenario_Name=="' + self.first_upside_scenario + '"')['Weight'].tolist()[0]
            down_weight = timestep.query('Scenario_Name=="' + self.first_downside_scenario + '"')['Weight'].tolist()[0]
            cond = ((value['Timestep'] == t) & (value['Scenario_Name'] == 'Base'))
            value.loc[cond, 'Weight'] = 1 - up_weight - down_weight
            total_weight = sum(value.query('Timestep==' + str(1))['Weight'].tolist())

            for index, row in value.query('Timestep==' + str(t)).iterrows():
                cond = ((value['Timestep'] == t) & (value['Scenario_Name'] == row['Scenario_Name']))
                value.loc[cond, 'Weight'] = row['Weight'] / total_weight

            if round(sum(value.query('Timestep==' + str(1))['Weight'].tolist()), 2) != 1:
                raise Exception("Weight error")

        self.__scenarios = value

    @property
    def first_downside_scenario(self):
        return self.__fus

    @property
    def first_upside_scenario(self):
        return self.__fds

    @property
    def grid(self):
        return self.__grid

    def findScenarios(self, gridSize: int = 1000):
        vars_list = []
        grid = []

        var1 = self.variable_Names[1]

        for v in self.variable_Names:
            if v == "Date":
                continue
            mx = max(self.historicData[v])
            mn = min(self.historicData[v])
            step_size = (mx - mn) / gridSize
            base_case = self.baseCase[v].tolist()[1]

            if v == var1 or (self.macroModel.coefficients[v][0] > 0 and self.macroModel.coefficients[var1][0] > 0) or \
                    (self.macroModel.coefficients[v][0] < 0 and self.macroModel.coefficients[var1][0] < 0):
                rng = np.linspace(base_case, base_case + step_size * (gridSize / 2), gridSize).tolist()
                rng.extend(np.linspace(base_case, base_case - step_size * (gridSize / 2), gridSize).tolist())
                vars_list.append(rng)
            else:
                rng = np.linspace(base_case, base_case - step_size * (gridSize / 2), gridSize).tolist()
                rng.extend(np.linspace(base_case, base_case + step_size * (gridSize / 2), gridSize).tolist())
                vars_list.append(rng)

        result = list(zip(*vars_list))

        for r in result:
            macroVars = {}
            index = 0
            for v in self.variable_Names:
                if v == "Date":
                    continue
                macroVars[v] = r[index]
                index += 1
            macroVars["Prediction"] = self.macroModel.score_up(macroVars)
            grid.append(macroVars)

        df = pd.DataFrame(grid)
        self.__grid = df
        self._create_Scenarios()

    def _create_Scenarios(self):
        rows = []

        for index, row in self.scenarios.iterrows():
            value = row["CI"]
            df_candidate = self.grid.iloc[(self.grid["Prediction"] - value).abs().argsort()].iloc[0].T
            row["Date"] = self.reporting_Date + relativedelta(years=row["Timestep"])

            for v in self.variable_Names:
                if v == "Date":
                    continue
                row[v] = df_candidate[v]

            rows.append(row)

        df = pd.DataFrame(rows)
        df["Date_str"] = df['Date'].dt.strftime('%d/%m/%Y')
        self.__scenarios = df
        self._linear_interpolation()

    @staticmethod
    def max_le(vals, val):
        return max([v for v in vals if v < val])

    @staticmethod
    def min_ge(vals, val):
        return min([v for v in vals if v > val])

    @staticmethod
    def f(row):
        if row['Type'] == "Upside":
            val = 1 - 1 / row['OneInX']
        elif row['Type'] == "Downside":
            val = 1 / row['OneInX']
        else:
            val = pd.NA
        return val
