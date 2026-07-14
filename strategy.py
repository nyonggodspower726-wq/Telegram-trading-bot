from market import get_market_data


def analyze_market(pair):

    timeframe = "1M"
    expiry = "2 Minutes"

    data = get_market_data(pair)

    if data.get("status") == "CLOSED":
        return f"""
📊 PipsPilot Analysis

🛑 Market CLOSED

{data.get("message")}
"""

    if "values" not in data:
        return f"""
❌ API Error

Pair: {pair}

{data}
"""

    candles = data["values"]

    latest = candles[0]
    previous = candles[1]

    candle_time = latest.get("datetime", "Unknown")

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

    # Candle direction
    if close_price > open_price:
        confidence += 20
        reasons.append("Bullish candle")
    else:
        confidence += 20
        reasons.append("Bearish candle")

    # Previous candle agreement
    if (close_price > open_price and prev_close > prev_open) or \
       (close_price < open_price and prev_close < prev_open):
        confidence += 20
        reasons.append("Previous candle agrees")

    # Candle size
    candle_range = high_price - low_price
    candle_body = abs(close_price - open_price)
    previous_body = abs(prev_close - prev_open)

    if candle_range > 0 and candle_body / candle_range >= 0.6:
        confidence += 20
        reasons.append("Strong momentum candle")

    # Engulfing
    bullish_engulfing = (
        prev_close < prev_open and
        close_price > open_price and
        open_price <= prev_close and
        close_price >= prev_open
    )

    bearish_engulfing = (
        prev_close > prev_open and
        close_price < open_price and
        open_price >= prev_close and
        close_price <= prev_open
    )

    # Overlap
    bullish_overlap = (
        close_price > open_price and
        close_price > prev_close
    )

    bearish_overlap = (
        close_price < open_price and
        close_price < prev_close
    )

    # Bigger candle
    bullish_bigger = (
        close_price > open_price and
        candle_body > previous_body
    )

    bearish_bigger = (
        close_price < open_price and
        candle_body > previous_body
    )

    signal = "WAIT ⏳"

    buy_entry = (
        bullish_engulfing or
        bullish_overlap or
        bullish_bigger
    )

    sell_entry = (
        bearish_engulfing or
        bearish_overlap or
        bearish_bigger
    )

    if confidence >= 50:

        if close_price > open_price and buy_entry:
            signal = "BUY 🟢"

            if bullish_engulfing:
                reasons.append("Bullish engulfing entry")
            elif bullish_overlap:
                reasons.append("Bullish overlap entry")
            else:
                reasons.append("Bigger bullish candle entry")

        elif close_price < open_price and sell_entry:
            signal = "SELL 🔴"

            if bearish_engulfing:
                reasons.append("Bearish engulfing entry")
            elif bearish_overlap:
                reasons.append("Bearish overlap entry")
            else:
                reasons.append("Bigger bearish candle entry")

    return f"""
📊 PipsPilot Price Action

Pair: {pair}
Timeframe: {timeframe}
Expiry: {expiry}
Candle Time: {candle_time}

Trend: {trend}

Confidence: {confidence}%

Signal: {signal}

Reason:
- {'\n- '.join(reasons)}
"""
