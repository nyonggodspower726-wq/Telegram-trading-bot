from datetime import datetime
import requests

API_KEY = "aba787bf68ba4008b359f34229fdbc29"


def is_market_open():
    day = datetime.utcnow().weekday()

    # Saturday = 5, Sunday = 6
    return day not in [5, 6]


def get_market_data(symbol):

    if not is_market_open():
        return {
            "status": "CLOSED",
            "message": "Forex market is closed for the weekend."
        }

    url = "https://api.twelvedata.com/time_series"

    params = {
        "symbol": symbol,
        "interval": "5min",
        "outputsize": 100,
        "apikey": API_KEY
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if data.get("status") == "error":
            return {
                "status": "ERROR",
                "message": data.get("message", "Unknown API error.")
            }

        if "values" not in data:
            return {
                "status": "ERROR",
                "message": "No candle data received."
            }

        return data

    except requests.exceptions.Timeout:

        return {
            "status": "ERROR",
            "message": "API request timed out."
        }

    except requests.exceptions.ConnectionError:

        return {
            "status": "ERROR",
            "message": "No internet connection."
        }

    except Exception as e:

        return {
            "status": "ERROR",
            "message": str(e)
        }
