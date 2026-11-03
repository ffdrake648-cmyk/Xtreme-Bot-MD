import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Welcome to XTREME BOT MD!\n\n"
        "Your bot is online!"
    )

def main():
    token = os.environ.get("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN is missing!")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))

    print("XTREME BOT MD is running!")

    app.run_polling()

if __name__ == "__main__":
    main()
