Worker.py
import os
import logging
from telegram import Update, ChatPermissions
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 WELCOME TO XTREME BOT 🔥\n\n"
        "Your powerful Telegram community assistant!\n\n"
        "Commands:\n"
        "/start - Start bot\n"
        "/help - Help menu\n"
        "/id - Get chat ID\n"
        "/rules - Group rules"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 XTREME BOT COMMANDS 🔥\n\n"
        "GENERAL\n"
        "/start\n"
        "/help\n"
        "/id\n"
        "/rules\n\n"
        "ADMIN\n"
        "/announce <message>\n"
        "/ban (reply to user)\n"
        "/mute (reply to user)\n"
        "/unmute (reply to user)"
    )


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Your Chat ID: {update.effective_chat.id}"
    )


async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 XTREME GROUP RULES\n\n"
        "1. Respect everyone.\n"
        "2. No spam.\n"
        "3. No unwanted links.\n"
        "4. No unnecessary arguments.\n"
        "5. Follow admin instructions."
    )


async def is_admin(update, context):
    member = await context.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id
    )
    return member.status in ("administrator", "creator")


async def announce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return

    message = " ".join(context.args)

    if message:
        await update.effective_chat.send_message(
            f"📢 XTREME ANNOUNCEMENT\n\n{message}"
        )


async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return

    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await context.bot.ban_chat_member(
            update.effective_chat.id,
            user.id
        )
        await update.message.reply_text("🚫 User banned.")


async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return

    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user

        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            user.id,
            ChatPermissions(can_send_messages=False)
        )

        await update.message.reply_text("🔇 User muted.")


async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return

    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user

        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            user.id,
            ChatPermissions(
                can_send_messages=True,
                can_send_other_messages=True
            )
        )

        await update.message.reply_text("🔊 User unmuted.")


async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for user in update.message.new_chat_members:
        await update.message.reply_text(
            f"🔥 Welcome {user.first_name} to XTREME COMMUNITY!\n"
            "Enjoy your stay!"
        )


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is missing.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(CommandHandler("rules", rules))
    app.add_handler(CommandHandler("announce", announce))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))

    app.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome)
    )

    print("🔥 XTREME BOT IS RUNNING!")

    app.run_polling()


if __name__ == "__main__":
    main()
