from Model.PD.ITermStructure import ITermStructure
import pandas as pd
from dateutil.relativedelta import relativedelta
import numpy as np


class ExpertTermStructure(ITermStructure):
    def __init__(self, term_structure: pd.DataFrame, years: int = 10):
        super().__init__(years)
        self.relative_term_structures = term_structure
        self.linear_interpolate_ts()

    # override interpolation
    def linear_interpolate_ts(self):
        record = {}
        ts = self.relative_term_structures
        for t in range(0, self.projection_years-1):

            month = (t * 12)
            record['M' + str(month)] = ts['Year ' + str(t)]

            for m in range(1, 12):
                month = (t*12) + m
                record['M' + str(month)] = (ts['Year ' + str(t+1)] - ts['Year ' + str(t)])/12 + \
                                           record['M' + str(month-1)]

        df = pd.DataFrame.from_dict(record)
        df = df.transpose().drop('Default', axis=1)
        df["Months"] = df.index.str.replace('M', '0').astype(np.int64)

        for index, row in df.iterrows():
            df.loc[index, "Date"] = self.reporting_Date + relativedelta(months=row["Months"])
        df.index = df["Months"]
        df = df.drop('Months', axis=1)
        self.interpolated_term_structures = df