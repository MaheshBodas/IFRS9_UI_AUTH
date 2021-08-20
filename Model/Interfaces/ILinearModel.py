from abc import ABC
import pandas as pd
from typing import Dict


class ILinearModel(ABC):

    def __init__(self, variables: pd.DataFrame, coefficients: pd.DataFrame):
        self.__variables = variables
        self.__coefficients = coefficients
        self.__has_intercept = True if "Intercept" in self.__coefficients.columns else False
        self.__intercept = self.__coefficients["Intercept"][0] if self.__has_intercept else 0
        self.__len = len(variables.index)
        names = self.__variables.columns.tolist()

        if "Date" in self.__variables.columns:
            names.remove("Date")
        elif "Year" in self.__variables.columns:
            names.remove("Year")

        self.__variablesNames = names
        self.__projections = []
        self._calculate_projections()

    @property
    def variables(self):
        return self.__variables

    @property
    def variablesNames(self):
        return self.__variablesNames

    @variables.setter
    def variables(self, value: pd.DataFrame):
        self.__variables = value
        self._calculate_projections()

    @property
    def coefficients(self):
        return self.__coefficients

    @coefficients.setter
    def coefficients(self, value: pd.DataFrame):
        self.__coefficients = value
        self._calculate_projections()

    @property
    def hasIntercept(self):
        return self.__has_intercept

    @property
    def intercept(self):
        return self.__intercept

    @property
    def length(self):
        return self.__len

    @property
    def projections(self):
        return self.__projections

    def _calculate_projections(self):
        for key in self.coefficients.columns:
            if key not in self.variables.columns and key != "Intercept":
                raise Exception(key + ' not on input data')

        if self.hasIntercept:
            self.__projections = [self.intercept] * self.length

        for key in self.__coefficients.columns:
            if key == "Intercept":
                continue

            index = 0
            coefficient = self.__coefficients[key][0]
            data = self.__variables[key]
            for d in data:
                self.__projections[index] = self.__projections[index] + coefficient * data[index]
                index += 1

    def score_up(self, data: Dict[str, float]) -> float:
        if self.hasIntercept:
            score = self.intercept
        else:
            score = 0

        for v in self.variablesNames:
            if v == "Date":
                continue
            score = score + self.__coefficients[v][0] * data[v]

        return score
