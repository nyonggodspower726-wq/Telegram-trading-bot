from market import get_market_data


def analyze_market():
    """
    EUR/USD binary strategy framework.
    """

    pair = "EUR/USD"
    timeframe = "5M"
    expiry = "15 Minutes"

    data = get_market_data()

    if data.get("status") == "CLOSED":
        return f"""
📊 EUR/USD Binary Analysis

🛑 Market CLOSED

{data.get("message")}
"""

    trend = "Waiting for candle analysis..."
    structure = "Waiting for BOS / MSS..."
    key_area = "Waiting for Liquidity / Order Block..."
    engulfing = "Waiting for Engulfing Candle..."

    return f"""
📊 EUR/USD Binary Analysis

Pair: {pair}
Chart: {timeframe}
Expiry: {expiry}

Latest Market Data Received ✅

Trend: {trend}
Structure: {structure}
Key Area: {key_area}
Engulfing: {engulfing}

Signal: NO TRADE
Confidence: 0%

Data:
{data}
"""
