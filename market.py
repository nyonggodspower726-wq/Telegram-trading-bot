import os
from datetime import datetime
import requests

API_KEY = os.getenv("TWELVE_DATA_API_KEY")


def is_market_open():
    """
    Forex market closed on Saturday and Sunday.
    Monday = 0, Sunday = 6
    """
    day = datetime.utcnow().weekday()

    if day in [5, 6]:
        return False

    return True


def get_market_data():

    if not is_market_open():
        return {
            "status": "CLOSED",
            "message": "Forex market is closed for the weekend."
        }

    url = "https://api.twelvedata.com/time_series"

    params = {
        "symbol": "EUR/USD",
        "interval": "5min",
        "outputsize": 5,
        "apikey": API_KEY
    }

    response = requests.get(url, params=params)

    data = response.json()

    return data
