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

    confidence = 0
    reasons = []

    # Trend
    if close_price > open_price:
        trend = "Bullish 🟢"
        confidence += 20
        reasons.append("Bullish trend")
    elif close_price < open_price:
        trend = "Bearish 🔴"
        confidence += 20
        reasons.append("Bearish trend")
    else:
        trend = "Neutral 🟡"

    liquidity = "None"

    # Liquidity Sweep
    if low_price <= swing_low:
        liquidity = "Sell-side Sweep ✅"
        confidence += 30
        reasons.append("Sell-side liquidity swept")

    elif high_price >= swing_high:
        liquidity = "Buy-side Sweep ✅"
        confidence += 30
        reasons.append("Buy-side liquidity swept")

    signal = "WAIT ⏳"

    # Confirmation Candle
    if liquidity == "Sell-side Sweep ✅" and close_price > open_price:
        confidence += 50
        reasons.append("Bullish confirmation candle")
        signal = "BUY 🟢"

    elif liquidity == "Buy-side Sweep ✅" and close_price < open_price:
        confidence += 50
        reasons.append("Bearish confirmation candle")
        signal = "SELL 🔴"

    if confidence < 50:
        signal = "WAIT ⏳"

    return f"""
📊 PipsPilot CRT Analysis

Pair: {pair}
Timeframe: {timeframe}
Expiry: {expiry}

Trend: {trend}

Swing High: {swing_high}
Swing Low : {swing_low}

Liquidity: {liquidity}

Confidence: {confidence}%

Signal: {signal}

Reason:
- {'\n- '.join(reasons) if reasons else 'No valid setup'}
"""
