from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = 8892992589:AAFfx5dwCizTvMOEe_uKJSE2y1a9qqrXPBQ

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Your Telegram trading bot is now running.")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()
