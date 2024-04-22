
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from db.activity import get_activity_by_t_username

from .telegram_send import send_text


async def points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text

    # Check if the bot is tagged in the message or the message is in a private chat
    if context.bot.username in message_text:
        user = update.effective_user
        points = get_activity_by_t_username(user.username)
        message_text = f"Hello {user.username}! You have {points} points."
        await send_text(update, message_text)
        return