
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from db.history import get_history_by_t_username

from .telegram_send import send_text

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text

    # Check if the bot is tagged in the message or the message is in a private chat
    if context.bot.username in message_text or update.message.chat.type == 'private':
        user = update.effective_user
        historyString = get_history_by_t_username(user.username)

        if len(historyString) == 0:
            historyString = "No history found"
        elif len(historyString) > 4096:
            historyString = historyString[:4090] + '''...'''

        await send_text(
            update,
            historyString,
            parse_mode="HTML"
            )