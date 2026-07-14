import asyncio

from strategy import analyze_market


CHAT_ID = "6588451803"


async def start_scanner(app):

    last_signal = None

    while True:
        print("Scanner running... checking market")

        result = analyze_market()

        # Send only BUY or SELL signals
        if "BUY 🟢" in result or "SELL 🔴" in result:

            # Prevent duplicate messages
            if result != last_signal:

                await app.bot.send_message(
                    chat_id=CHAT_ID,
                    text=result
                )

                last_signal = result

                print("Trade signal sent to Telegram")

        await asyncio.sleep(300)
