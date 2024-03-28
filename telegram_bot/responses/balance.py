
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from db.balances import get_balance_by_t_username
from constants.responses import RESPONSE_BALANCE_MAIN

# Define the balance command
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check the balance of the user."""
    message_text = update.message.text

    # Check if the bot is tagged in the message or the message is in a private chat
    if context.bot.username in message_text or update.message.chat.type == 'private':
        user = update.message.from_user
        balance = get_balance_by_t_username(user.username)
        await update.message.reply_text(RESPONSE_BALANCE_MAIN.format(balance=balance))
