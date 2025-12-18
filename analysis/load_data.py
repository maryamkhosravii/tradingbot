import pandas as pd
from pymongo import MongoClient
from typing import List, Optional
from datetime import datetime

class MongoLoader:
    def __init__(self, uri: str = "mongodb://localhost:27017/", db_name: str = "trading"):
        self.client = MongoClient (uri)
        self.db = self.client [db_name]


    def load_symbol (
            self,
            symbol: str,
            collection_name: str = "raw_ohlc",
            start_date: Optional[datetime] = None,
            end_date: Optional [datetime] = None,
    ) -> pd.DataFrame:
        
        col = self.db[collection_name]

        query = {"symbol": symbol}

        if start_date:
            query["timestamp"] = {"$gte": start_date}
        if end_date:
            if "timestamp" in query:
                query["timestamp"] ["$lte"] = end_date
            else:
                query["timestamp"] = {"$lte": end_date}

        
        data = list (col.find(query))
        if not data:
            print(f"Not data found for symbol: {symbol}")
            return pd.DataFrame
        
        df = pd.DataFrame(data)
        return df
        

    

    def load_symbols (
            self,
            symbols: List[str],
            collection_name: str = "raw_ohlc",
            start_date: Optional[datetime] = None,
            end_date: Optional [datetime] = None,
    ) -> pd.DataFrame:
        
        dfs = []
        for sym in symbols:
            df = self.load_symbol(sym, collection_name, start_date, end_date)
            if not df.empty:
                dfs.append(df)

        if dfs:
            return pd.concat (dfs, ignore_index=True)
        return pd.DataFrame()