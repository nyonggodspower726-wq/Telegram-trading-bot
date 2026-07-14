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
❌ API Error

{data}
"""

    candles = data["values"]

    latest = candles[0]

    open_price = float(latest["open"])
    high_price = float(latest["high"])
    low_price = float(latest["low"])
    close_price = float(latest["close"])

    highs = [float(c["high"]) for c in candles[:10]]
    lows = [float(c["low"]) for c in candles[:10]]

    swing_high = max(highs)
    swing_low = min(lows)

    if close_price > open_price:
        trend = "Bullish 🟢"
    elif close_price < open_price:
        trend = "Bearish 🔴"
    else:
        trend = "Neutral 🟡"

    liquidity = "None"
    structure = "Waiting"
    signal = "WAIT ⏳"
    confidence = "40%"

    # CRT Logic
    if high_price >= swing_high:
        liquidity = "Buy-side Liquidity Sweep"

    elif low_price <= swing_low:
        liquidity = "Sell-side Liquidity Sweep"

    if liquidity == "Buy-side Liquidity Sweep" and close_price < open_price:
        structure = "Bearish Rejection"
        signal = "SELL 🔴"
        confidence = "75%"

    elif liquidity == "Sell-side Liquidity Sweep" and close_price > open_price:
        structure = "Bullish Rejection"
        signal = "BUY 🟢"
        confidence = "75%"

    return f"""
📊 PipsPilot CRT Analysis

Pair: {pair}
Timeframe: {timeframe}
Expiry: {expiry}

Trend: {trend}

Swing High: {swing_high}
Swing Low : {swing_low}

Liquidity: {liquidity}
Structure: {structure}

Signal: {signal}
Confidence: {confidence}
"""
