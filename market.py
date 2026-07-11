
from datetime import datetime


def get_market_data():
    """
    Market data structure for the strategy.
    Live prices will be connected later.
    """

    return {
        "pair": "EUR/USD",
        "timeframe": "5M",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "open": None,
        "high": None,
        "low": None,
        "close": None,
        "volume": None,
        "status": "Waiting for live market data..."
    }
