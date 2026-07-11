from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from strategy import analyze_market

TOKEN = "8892992589:AAHJaYwKpyNj3Kp7-oYnreE3WEvdvxEkGKw"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Your Telegram bot is working.")


async def analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = analyze_market()
    await update.message.reply_text(result)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analysis", analysis))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
