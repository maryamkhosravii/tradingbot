from data_sources.nobitex_source import get_ticker
from data_sources.binance_source import get_historical_ohlc
from utils.mongo_handler import insert_ohlc #, insert_many_ohlc
from datetime import datetime, timezone
import time
from apscheduler.schedulers.blocking import BlockingScheduler


symbols_nobitex = ["btc-irt", "eth-irt", "usdt-irt"]
#symbols_binance = ["BTCUSDT", "ETHUSDT", "USDTUSDT"]

def fetch_and_save():
    for symbol in symbols_nobitex:
        data = get_ticker(symbol)
        data["timestamp"] = datetime.now(timezone.utc)
        insert_ohlc(data)
        print (f"Saved NOBITEX {symbol} at {data['timestamp']}")

  #  for symbol in symbols_binance:
   #     ohlc_list = get_historical_ohlc (symbol, interval="1m", limit=100)
    #    insert_many_ohlc (ohlc_list)
     #   print (f"Saved BINANCE {symbol} {len(ohlc_list)} records")
      #  time.sleep(2)

scheduler = BlockingScheduler()
scheduler.add_job(fetch_and_save, 'interval', minutes=1)
scheduler.start()