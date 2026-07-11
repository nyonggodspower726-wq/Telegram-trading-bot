from datetime import datetime

def is_market_open():
    """
    Forex market is closed on Saturday (5) and Sunday (6).
    Monday = 0
    """
    day = datetime.utcnow().weekday()

    if day in [5, 6]:
        return False

    return True


def get_market_data():
    if not is_market_open():
        return {
            "status": "CLOSED"
        }

    return {
        "status": "OPEN",
        "pair": "EUR/USD",
        "timeframe": "5M"
    }
