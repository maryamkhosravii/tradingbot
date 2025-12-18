import pandas as pd
import numpy as np
from typing import Optional

class DataCleaner:
    def __init__(self):
        pass

    def clean (self, df: pd.DataFrame) -> pd.DataFrame:
        if df is None or df.empty:
            print ("Empty dataframe received.")
            return pd.DataFrame()
        
        df = df.copy()

        drop_cols = ["_id"]
        df = df.drop (columns=[c for c in drop_cols if c in df.columns], errors="ignore")

        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime (df["timestamp"], errors="coerce")

        df = df.dropna(subset=["timestamp"]).reset_index(drop=True)


        rename_map ={
            "dayOpen": "open",
            "dayHigh": "high",
            "dayLow": "low",
            "dayClose": "close"
        }

        df = df.rename(columns=rename_map)

        df = df.sort_values("timestamp"). reset_index(drop=True)

        price_cols = ["open","high", "low", "close", "price"]
        for col in price_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        for col in price_cols:
            if col in df.columns:
                df = df[df[col]>0]

        df = df.drop_duplicates(subset=["symbol", "timestamp"], keep="first")

        return df
        
    def clean_multiple (self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        return self.clean(df)
