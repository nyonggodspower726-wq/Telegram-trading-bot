from market import get_market_data


def analyze_market(pair):

    timeframe = "5M"
    expiry = "5 Minutes"

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

    # Last CLOSED candle
    c1 = candles[1]

    candle_time = c1["datetime"]

    o1 = float(c1["open"])
    h1 = float(c1["high"])
    l1 = float(c1["low"])
    cl1 = float(c1["close"])

    trend = "Sideways 🟡"
    confidence = 0
    reasons = []
    signal = "WAIT ⏳"

    # ----------------------------
    # Find last bearish candle
    # ----------------------------

    last_bear_high = None

    for candle in candles[2:20]:

        o = float(candle["open"])
        c = float(candle["close"])

        if c < o:
            last_bear_high = float(candle["high"])
            break

    # ----------------------------
    # Find last bullish candle
    # ----------------------------

    last_bull_low = None

    for candle in candles[2:20]:

        o = float(candle["open"])
        c = float(candle["close"])

        if c > o:
            last_bull_low = float(candle["low"])
            break

    # ----------------------------
    # Bullish Trend
    # ----------------------------

    bullish = cl1 > o1

    # ----------------------------
    # Bearish Trend
    # ----------------------------

    bearish = cl1 < o1

    # ----------------------------
    # BUY
    # ----------------------------

    if bullish:

        trend = "Bullish 🟢"

        if last_bear_high is not None:

            if cl1 > last_bear_high:

                signal = "BUY 🟢"
                confidence = 100

                reasons.append("5M Candle Breakout")
                reasons.append("Closed above last bearish candle")

        else:

            prev_high = float(candles[2]["high"])

            if cl1 > prev_high:

                signal = "BUY 🟢"
                confidence = 100

                reasons.append("Strong bullish impulse")
                reasons.append("Closed above previous bullish candle")

    # ----------------------------
    # SELL
    # ----------------------------

    elif bearish:

        trend = "Bearish 🔴"

        if last_bull_low is not None:

            if cl1 < last_bull_low:

                signal = "SELL 🔴"
                confidence = 100

                reasons.append("5M Candle Breakout")
                reasons.append("Closed below last bullish candle")

        else:

            prev_low = float(candles[2]["low"])

            if cl1 < prev_low:

                signal = "SELL 🔴"
                confidence = 100

                reasons.append("Strong bearish impulse")
                reasons.append("Closed below previous bearish candle")

    return f"""
📊 PipsPilot V3

Pair: {pair}
Timeframe: {timeframe}
Expiry: {expiry}
Candle Time: {candle_time}

Trend: {trend}

Confidence: {confidence}%

Signal: {signal}

Reason:
- {'\n- '.join(reasons) if reasons else "No breakout"}
"""
