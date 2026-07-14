from market import get_market_data


def analyze_market():
    pair = "EUR/USD"
    timeframe = "5M"
    expiry = "15 Minutes"

    data = get_market_data()

    if data.get("status") == "CLOSED":
        return f"""
📊 PipsPilot CRT Analysis

🛑 Market CLOSED

{data.get("message")}
"""

    if "values" not in data:
        return f"""
❌ Failed to fetch market data.

Response:
{data}
"""

    candles = data["values"]

    latest = candles[0]

    open_price = float(latest["open"])
    high_price = float(latest["high"])
    low_price = float(latest["low"])
    close_price = float(latest["close"])

    if close_price > open_price:
        trend = "Bullish 🟢"
    elif close_price < open_price:
        trend = "Bearish 🔴"
    else:
        trend = "Neutral 🟡"

    return f"""
📊 PipsPilot CRT Analysis

Pair: {pair}
Timeframe: {timeframe}
Expiry: {expiry}

Current Candle

Open: {open_price}
High: {high_price}
Low: {low_price}
Close: {close_price}

Trend: {trend}

Liquidity Sweep: Waiting...
Market Structure Shift: Waiting...
Order Block: Waiting...
CRT Entry: Waiting...

Signal: WAIT ⏳
Confidence: 0%

Waiting for a valid CRT setup.
"""
