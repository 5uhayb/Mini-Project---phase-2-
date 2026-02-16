import pandas as pd
import numpy as np


def ensure_dataframe(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame.")

def data_cleaner(df: pd.DataFrame) -> pd.DataFrame:
    ensure_dataframe(df)
    df.drop_duplicates(inplace=True)
    df.replace('%','',regex=True,inplace=True)
    df.replace(["NULL", "N/A"], np.nan, inplace=True)

    return df