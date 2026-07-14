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
    previous = candles[1]

    open_price = float(latest["open"])
    high_price = float(latest["high"])
    low_price = float(latest["low"])
    close_price = float(latest["close"])

    prev_high = float(previous["high"])
    prev_low = float(previous["low"])

    # Trend
    if close_price > open_price:
        trend = "Bullish 🟢"
    elif close_price < open_price:
        trend = "Bearish 🔴"
    else:
        trend = "Neutral 🟡"

    # Simple CRT checks
    liquidity = "No Sweep"
    structure = "No Break"
    signal = "WAIT ⏳"
    confidence = "20%"

    if high_price > prev_high:
        liquidity = "Buy-side Liquidity Taken"

    if low_price < prev_low:
        liquidity = "Sell-side Liquidity Taken"

    if close_price > prev_high:
        structure = "Bullish Break"
        signal = "BUY 🟢"
        confidence = "65%"

    elif close_price < prev_low:
        structure = "Bearish Break"
        signal = "SELL 🔴"
        confidence = "65%"

    return f"""
📊 PipsPilot CRT Analysis

Pair: {pair}
Timeframe: {timeframe}
Expiry: {expiry}

Current Candle

Open : {open_price}
High : {high_price}
Low  : {low_price}
Close: {close_price}

Trend: {trend}

CRT Analysis

Liquidity: {liquidity}
Structure: {structure}

Signal: {signal}
Confidence: {confidence}
"""
