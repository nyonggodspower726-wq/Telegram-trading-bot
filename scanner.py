import asyncio

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
        print("Scanner running... checking market")

        for pair in PAIRS:

            result = analyze_market(pair)

            # Send only BUY or SELL signals
            if "BUY 🟢" in result or "SELL 🔴" in result:

                # Prevent duplicate messages for each pair
                if last_signals.get(pair) != result:

                    await app.bot.send_message(
                        chat_id=CHAT_ID,
                        text=result
                    )

                    last_signals[pair] = result

                    print(f"{pair} trade signal sent to Telegram")

            else:
                print(f"{pair}: No setup")

        await asyncio.sleep(300)
