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

    # Last 4 CLOSED candles
    c1 = candles[1]
    c2 = candles[2]
    c3 = candles[3]
    c4 = candles[4]

    candle_time = c1["datetime"]

    o1, h1, l1, cl1 = map(float, [c1["open"], c1["high"], c1["low"], c1["close"]])
    o2, h2, l2, cl2 = map(float, [c2["open"], c2["high"], c2["low"], c2["close"]])
    o3, h3, l3, cl3 = map(float, [c3["open"], c3["high"], c3["low"], c3["close"]])
    o4, h4, l4, cl4 = map(float, [c4["open"], c4["high"], c4["low"], c4["close"]])

    reasons = []
    confidence = 0

    signal = "WAIT ⏳"
    trend = "Sideways 🟡"

    # Strong candle
    body = abs(cl1 - o1)
    rng = h1 - l1

    strong = False
    if rng > 0 and body / rng >= 0.60:
        strong = True
        confidence += 20
        reasons.append("Strong momentum candle")

    # Trend
    bullish_trend = (
        cl1 > cl2 and
        cl2 > cl3
    )

    bearish_trend = (
        cl1 < cl2 and
        cl2 < cl3
    )

    if bullish_trend:
        trend = "Bullish 🟢"
        confidence += 30
        reasons.append("Bullish trend")

    elif bearish_trend:
        trend = "Bearish 🔴"
        confidence += 30
        reasons.append("Bearish trend")

    # Breakout
    bullish_break = (
        cl1 > o1 and
        cl1 > h2
    )

    bearish_break = (
        cl1 < o1 and
        cl1 < l2
    )

    # Continuation
    bullish_continuation = (
        bullish_break and
        body > abs(cl2 - o2)
    )

    bearish_continuation = (
        bearish_break and
        body > abs(cl2 - o2)
    )

    if bullish_continuation and bullish_trend and strong:
        signal = "BUY 🟢"
        confidence += 50
        reasons.append("Bullish breakout continuation")

    elif bearish_continuation and bearish_trend and strong:
        signal = "SELL 🔴"
        confidence += 50
        reasons.append("Bearish breakout continuation")

    return f"""
📊 PipsPilot V2

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
