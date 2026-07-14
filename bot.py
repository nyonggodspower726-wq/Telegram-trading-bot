from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import asyncio

from strategy import analyze_market
from scanner import start_scanner


TOKEN = "YOUR_BOT_TOKEN"


PAIRS = [
    "EUR/USD",
    "GBP/USD",
    "USD/JPY",
    "XAU/USD"
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 PipsPilot V2 Online\n\n"
        "✅ Automatic Scanner Running\n"
        "📊 Monitoring:\n"
        "• EUR/USD\n"
        "• GBP/USD\n"
        "• USD/JPY\n"
        "• XAU/USD\n\n"
        "Timeframe: 5 Minutes\n"
        "Expiry: 5 Minutes"
    )


async def analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = ""

    for pair in PAIRS:
        message += analyze_market(pair)
        message += "\n\n"

    await update.message.reply_text(message)


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analysis", analysis))

    print("🤖 PipsPilot V2 Running...")

    # Start background scanner
    asyncio.get_event_loop().create_task(start_scanner(app))

    app.run_polling()


if __name__ == "__main__":
    main()
