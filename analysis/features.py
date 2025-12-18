import pandas as pd
import numpy as np


class FeatureEngineer:
    def __init__(self):
        pass


    def add_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        price_col = None
        for col in ["close", "latest"]:
            if col in df.columns:
                price_col = col
                break
        if not price_col:
            raise ValueError ("No 'close' or 'latest' column found for feature calculation.")
        

        # Moving Average
        df["SMA_10"] = df[price_col].rolling(window=10).mean()
        df["SMA_30"] = df[price_col].rolling(window=30).mean()
        df["EMA_10"] = df[price_col].ewm(span=10, adjust=False).mean()
        df["EMA_30"] = df[price_col].ewm(span=30, adjust=False).mean()


        # RSI
        delta = df[price_col].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain/loss
        df["RSI_14"] = 100 - (100 / (1+rs))


        # MACD
        ema_12 = df[price_col].ewm(span=12, adjust=False).mean()
        ema_26 = df[price_col].ewm(span=26, adjust=False).mean()
        df["MACD"] = ema_12 - ema_26
        df["MACD_signal"] = df["MACD"].ewm(span=9, adjust=False).mean()


        # Bollinger Bands
        df ["BB_Middle"] = df[price_col].rolling(window=20).mean()
        df ["BB_Std"] = df[price_col].rolling(window=20).std()
        df["BB_Upper"] = df["BB_Middle"] + 2 * df["BB_Std"]
        df["BB_Lower"] = df["BB_Middle"] - 2 * df["BB_Std"]


        # Volatility
        df["volatility_20"] = df[price_col].rolling(window=20).std()


        # Price Change Features
        if {"high", "low"} <= set(df.columns):
            df["HL_range"] = df["high"] - df["low"]
        if {"open", "close"} <= set(df.columns):
            df["OC_change"] = df["close"] - df["open"]
        df["Return"] = df[price_col].pct_change()
        df["Log_Return"] = np.log(df[price_col] / df[price_col].shift(1))


        df = df.replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)
        return df
