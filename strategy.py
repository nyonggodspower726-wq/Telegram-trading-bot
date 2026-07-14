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
    close_price = float(latest["close"])
    high_price = float(latest["high"])
    low_price = float(latest["low"])

    prev_open = float(previous["open"])
    prev_close = float(previous["close"])

    confidence = 0
    reasons = []

    # Trend
    if close_price > open_price:
        trend = "Bullish 🟢"
        confidence += 20
        reasons.append("Bullish trend")
    else:
        trend = "Bearish 🔴"
        confidence += 20
        reasons.append("Bearish trend")

    # Candle confirmation
    if close_price > open_price:
        confidence += 30
        reasons.append("Bullish candle")
    else:
        confidence += 30
        reasons.append("Bearish candle")

    # Previous candle confirmation
    if (close_price > open_price and prev_close > prev_open) or \
       (close_price < open_price and prev_close < prev_open):
        confidence += 20
        reasons.append("Previous candle agrees")

    # Strong candle body
    candle_range = high_price - low_price
    candle_body = abs(close_price - open_price)

    if candle_range > 0 and candle_body / candle_range >= 0.6:
        confidence += 30
        reasons.append("Strong momentum candle")

    # Final signal
    if confidence >= 50:
        signal = "BUY 🟢" if close_price > open_price else "SELL 🔴"
    else:
        signal = "WAIT ⏳"

    return f"""
📊 PipsPilot CRT Analysis

Pair: {pair}
Timeframe: {timeframe}
Expiry: {expiry}

Trend: {trend}

Confidence: {confidence}%

Signal: {signal}

Reason:
- {'\n- '.join(reasons)}
"""
