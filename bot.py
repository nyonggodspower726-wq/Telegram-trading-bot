
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8892992589:AAHJaYwKpyNj3Kp7-oYnreE3WEvdvxEkGKw"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Your Telegram bot is working.")
    async def analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("EUR/USD Analysis is coming soon.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
