
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from db.transactions import record_welcome_bonus_by_t_username
from db.activity import get_unique_chat_ids

from db.users import setup_user, set_command_by_t_username
from constants.globals import (
    WALLET_BUTTON,
    WITHDRAW_BUTTON,
    USER_HELP_BUTTON,
    USER_BALANCE_BUTTON,
    USER_HISTORY_BUTTON,
    USER_NEW_USER_ADDED,
    DEFAULT_WELCOME_BACK_MESSAGE,
    DEFAULT_WELCOME_MESSAGE
)

from .telegram_send import send_html, send_html_noreply

# Define the start function 
# If the user is new, add the user to the database and send a welcome message
# If the user is not new, send a welcome back message
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user.username 
    
    if user != 'constantin_pricope':
        await send_html(update, f"You are not authorized to use this command {user}")
        return
    
    # get all the chat ids
    chat_ids = get_unique_chat_ids()
    
    print(f"chat_ids = {chat_ids}")
    
    #Iterate over the chat ids and send the message
    for chat_id in chat_ids:
        # If this is a reply to a message, get the message text from the reply
        if update.message.reply_to_message.text:
            message = update.message.reply_to_message.text
        else:
            print(context.args)
            message = " ".join(context.args)
            print(message)
        
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")

    
    