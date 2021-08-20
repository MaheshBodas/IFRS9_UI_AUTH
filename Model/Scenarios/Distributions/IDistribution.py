from abc import ABC, abstractmethod
from typing import List, Dict
from scipy.stats import norm
import Model.Scenarios.CyclicalityIndex as cyc_ind


class IDistribution(ABC):

    def __init__(self):
        self.__parameters = {}
        self.__historic_CI = []
        self.__historic_DR = []
        self.__name = ""
        self.__dist = None
        self.__median = None
        self.__fitted = False
        self.__lower = -3.5
        self.__upper = 0
        self.__interval = 0.05
        self.__range = 71

    # region PROPERTY: DISTRIBUTION PARAMETERS
    @property
    def parameters(self):
        return self.__parameters

    @parameters.setter
    def parameters(self, value: Dict[str, float]):
        self.__parameters = value

    # endregion

    # region PROPERTY: HISTORIC CYCLICALITY INDEX
    @property
    def historic_CI(self):
        return self.__historic_CI

    @historic_CI.setter
    def historic_CI(self, value: List[float]):
        self.__historic_DR = norm.cdf(value)
        self.__historic_CI = value

    # endregion

    # region PROPERTY: HISTORIC DEFAULT RATE
    @property
    def historic_DR(self):
        return self.__historic_DR

    @historic_DR.setter
    def historic_DR(self, value: List[float]):
        self.__historic_CI = norm.ppf(value)
        self.__historic_DR = value

    # endregion

    # region PROPERTY: NAME
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    # endregion

    # region PROPERTY: DISTRIBUTION
    @property
    def distribution(self):
        return self.__dist

    @distribution.setter
    def distribution(self, value):
        self.__dist = value

    # endregion

    # region PROPERTY: MEDIAN
    @property
    def median(self):
        return self.__median

    @median.setter
    def median(self, value):
        self.__median = value

    # endregion

    # region PROPERTY: FITTED
    @property
    def fitted(self):
        return self.__fitted

    @fitted.setter
    def fitted(self, value: bool):
        self.__fitted = value

    # endregion

    # region PROPERTY: RANGE_LOW
    @property
    def range_low(self):
        return self.__lower

    @range_low.setter
    def range_low(self, value: float):
        self.__lower = value
        self._set_range()

    # endregion

    # region PROPERTY: RANGE_HIGH
    @property
    def range_high(self):
        return self.__upper

    @range_high.setter
    def range_high(self, value: float):
        self.__upper = value
        self._set_range()

    # endregion

    # region PROPERTY: INTERVAL
    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, value: float):
        self.__interval = value
        self._set_range()

    # endregion

    # region PROPERTY: RANGE
    @property
    def range(self):
        return self.__range

    # endregion

    def _set_range(self):
        self.__range = int(abs((self.__upper - self.__lower) / self.__interval) + 1)

    @abstractmethod
    def fitDistribution(self):
        pass

    @abstractmethod
    def _findMedian(self):
        pass

    @abstractmethod
    def CiProbability(self, baseCaseCI: List[float], confidenceInterval: float) -> List[float]:
        pass

    @abstractmethod
    def CiProbability_from_Definition(self, baseCaseCI: List[float], scenarios: cyc_ind.CyclicalityIndex) -> None:
        pass
