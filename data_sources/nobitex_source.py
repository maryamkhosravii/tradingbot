import requests

BASE_URL = "https://apiv2.nobitex.ir"

def get_ticker (symbol):
    try: 
        src, dst = symbol.split("-")
        url = f"{BASE_URL}/market/stats"
        params = {
            "srcCurrency": src,
            "dstCurrency": dst
        }

        response = requests.get (url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        stats = data.get ("stats", {}).get(symbol, {})
        if not stats:
            print (f"No data for {symbol}")

        return {
            "symbol": symbol,
            "latest": float (stats.get("latest", 0)),
            "dayHigh": float (stats.get("dayHigh", 0)),
            "dayLow": float (stats.get("dayLow", 0)),
            "dayOpen": float (stats.get("dayOpen", 0)),
            "dayClose": float (stats.get("dayClose", 0)),
            "bestBuy": float (stats.get("bestBuy", 0)),
            "bestSell": float (stats.get("bestSell", 0)),
            "volumeSrc": float (stats.get("volumeSrc", 0)),
            "volumeDst": float (stats.get("volumeDst", 0)),
            "dayChange": float (stats.get("dayChange", 0)),
            "isClosed": stats.get("isClosed", False)

        }

    except requests.exceptions.RequestException as e:
        print (f"Error fetching {symbol}: {e}")
        return None
