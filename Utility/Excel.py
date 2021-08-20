import io
import pandas as pd
from typing import List

def get_list_of_sheets(byte_data: bytes) -> List[str]:
    df = pd.read_excel(byte_data, None)
    return list(df.keys())


def from_byte(byte_data: bytes, sheetName: str, header_row: int, columns: str, clean: bool = True) -> pd.DataFrame:
    df = pd.read_excel(io.BytesIO(byte_data), sheetName, header=header_row, usecols=columns)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.dropna()

    if clean:
        for i in range(1, 4):
            df.columns = df.columns.str.replace('.' + str(i), '')
    return df
