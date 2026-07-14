import asyncio
from datetime import datetime

from strategy import analyze_market


CHAT_ID = "6588451803"

PAIRS = [
    "EUR/USD",
    "GBP/USD",
    "USD/JPY",
    "XAU/USD"
]


async def start_scanner(app):

    last_signals = {}

    while True:

        now = datetime.utcnow()

        # Wait until the next 5-minute candle closes
        wait = 300 - (now.minute % 5) * 60 - now.second

        if wait > 0:
            await asyncio.sleep(wait)

        print("Scanning closed 5M candle...")

        for pair in PAIRS:

            result = analyze_market(pair)

            if "BUY 🟢" in result or "SELL 🔴" in result:

                if last_signals.get(pair) != result:

                    await app.bot.send_message(
                        chat_id=CHAT_ID,
                        text=result
                    )

                    last_signals[pair] = result

                    print(f"{pair} signal sent")

            else:
                print(f"{pair}: No setup")
