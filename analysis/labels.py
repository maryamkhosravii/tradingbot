import pandas as pd
from typing import Optional

class LabelMaker:
    def __init__(self):
        pass

    def add_future_price_label(
            self, df: pd.DataFrame, price_col: str = "close", horizon: int = 1
    ) -> pd.DataFrame:
        
        df = df.copy()
        if price_col not in df.columns:
            raise ValueError (f"Column '{price_col}' not found in dataframe")
        
        df[f"future_{horizon}"] = df[price_col].shift(-horizon)
        df[f"label_{horizon}"] = (df[f"future_{horizon}"] > df[price_col]).astype(int)

        df = df.dropna().reset_index(drop=True)
        return df
    

    def add_threshold_label (
        self, df: pd.DataFrame, price_col: str = "close", horizon: int = 1, threshold: float = 0.001
    ) -> pd.DataFrame:
        df = df.copy()
        if price_col not in df.columns:
            raise ValueError (f"Column '{price_col}' not found in dataframe")
        
        df[f"future_{horizon}"] = df[price_col].shift(-horizon)
        df[f"pct_change_{horizon}"] = (df[f"future_{horizon}"] - df[price_col]) / df[price_col]

        df[f"label_{horizon}"] = df[f"pct_change_{horizon}"].apply(
            lambda x: 1 if x > threshold
            else (-1 if x < -threshold else 0)
        )

        df = df.dropna().reset_index(drop=True)
        return df