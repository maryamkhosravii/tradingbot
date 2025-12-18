from load_data import MongoLoader
from cleaning_data import DataCleaner
from features import FeatureEngineer
from labels import LabelMaker
from typing import List, Optional
import pandas as pd
import os


class DatasetBuilder:
    def __init__(self, output_folder="datasets"):
        self.loader = MongoLoader()
        self.cleaner = DataCleaner()
        self.featuring = FeatureEngineer()
        self.labeling = LabelMaker()
        self.output_folder = output_folder

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)


    def build_dataset(
            self,
            symbols: List[str] = ["btc-irt", "eth-irt", "usdt-irt"],
            horizon: int = 1,
            threshold: Optional[float] = None,
            seperate_files: bool = False,
            output_name: str = "dataset.csv"
    ) -> pd.DataFrame:
        
        all_dfs = []
        for symbol in symbols:
            print (f"Loading raw data for {symbol}...")
            df = self.loader.load_symbol(symbol)

            if df.empty:
                print(f"No data for {symbol}, skipping...")
                continue

            print ("Cleaning data...")
            df = self.cleaner.clean(df)

            print("Adding features...")
            df = self.featuring.add_features(df)

            print ("Creating labels...")
            if threshold:
                df = self.labeling.add_threshold_label(df, horizon=horizon, threshold=threshold)
            else:
                df = self.labeling.add_future_price_label(df, price_col="close", horizon=horizon)

            df["symbol"] = symbol

            if seperate_files:
                output_path = f"{self.output_folder}/{symbol}_{output_name}"
                df.to_csv(output_path, index=False)
                print (f"Saved : {output_path}")
            else:
                all_dfs.append(df)

            
        if not seperate_files and all_dfs:
            df_all = pd.concat(all_dfs, ignore_index=True)
            output_path = f"{self.output_folder}/{output_name}"
            df_all.to_csv(output_path, index=False)
            print (f"Combined dataset saved: {output_path}")
            return df_all
            
        if seperate_files:
            print ("All symbols saved in seperated files.")
            return None
        
        print ("No data processed.")
        return pd.DataFrame()
