import pandas as pd


def ensure_dataframe(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame.")

def drop_duplicate(df: pd.DataFrame) -> pd.DataFrame:
    ensure_dataframe(df)
    return df.drop_duplicates()

