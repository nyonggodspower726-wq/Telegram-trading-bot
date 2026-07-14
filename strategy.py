from market import get_market_data


def analyze_market():
    data = get_market_data()

    if data.get("status") == "CLOSED":
        return f"""
📊 PipsPilot CRT

🛑 Market CLOSED

{data.get("message")}
"""

    if "values" not in data:
        return f"API Error:\n{data}"

    candles = data["values"]

    current = candles[0]
    previous = candles[1]

    co = float(current["open"])
    cc = float(current["close"])

    po = float(previous["open"])
    pc = float(previous["close"])

    signal = "WAIT ⏳"
    confidence = 0
    reason = "No valid setup"

    # Bullish Engulfing
    if (
        pc < po and
        cc > co and
        co <= pc and
        cc >= po
    ):
        signal = "BUY 🟢"
        confidence = 80
        reason = "Bullish Engulfing"

    # Bearish Engulfing
    elif (
        pc > po and
        cc < co and
        co >= pc and
        cc <= po
    ):
        signal = "SELL 🔴"
        confidence = 80
        reason = "Bearish Engulfing"

    return f"""
📊 PipsPilot CRT

Pair: EUR/USD
Timeframe: 5M
Expiry: 15 Minutes

Signal: {signal}
Confidence: {confidence}%

Reason:
{reason}
"""
