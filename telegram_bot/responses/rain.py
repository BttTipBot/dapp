import random

from telegram import Update, ReplyKeyboardMarkup, Chat, Bot
from telegram.ext import ContextTypes

from db.activity import get_activity_by_chat_id, get_activity_by_chat_id_timeback
from db.transactions import record_rain_by_t_username
from utils.convert import is_int, convert_to_int, human_format
from db.parameters import get_param
from db.balances import get_balance_by_t_username
from constants.parameters import PARAMETER_RAIN_FEE_BTT
from constants.globals import RAIN_INSUFFICIENT_BALANCE

from .telegram_send import send_text, send_animation


# Define the rain function
async def rain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # The rain is a feature available only in groups
    if update.message.chat.type == 'private':
        await send_text(update, "The rain feature is only available in groups.")
        return


    # Get the list of users in the group
    # users_count = await update.message.chat.get_member_count()
    
    if len(context.args) < 1:
        await send_text(update, 'Usage: /rain <amount> [5m/1h/1d]')
        return
    
    # Get the amount
    amount = context.args[0]
    print(f"amount = '{amount}'")

    amount_int = 0

    # Check if ammount is correct
    if is_int(amount):
        amount_int = convert_to_int(amount)
    else:
        await send_text(update, 'Invalid amount')
        return
    
    # Check if the user has the sufficient balance
    sender = update.message.from_user
    balance_sender = get_balance_by_t_username(sender.username)
    fee = int(get_param(PARAMETER_RAIN_FEE_BTT))

    if balance_sender + fee < amount_int and amount_int > 0:
        await send_text(update, RAIN_INSUFFICIENT_BALANCE.format(balance=human_format(balance_sender), max=human_format(balance_sender)))
        return

    if len(context.args) > 2:
        timeback = context.args[1]
    else:
        timeback = '1d'

    # Use get Activity by chat id
    users = get_activity_by_chat_id_timeback(update.message.chat.id, timeback)

    users = [user['t_username'] for user in users if user['t_username'] != sender.username]

    if len(users) == 0:
        await send_text(update, "☒ No active users in the group")
        return

    str = record_rain_by_t_username(sender.username, users, amount_int)

    # List of good night GIF URLs (replace with your own URLs)
    gif_urls = [
        "assets/gif/rain1.gif",
        "assets/gif/rain2.gif",
        "assets/gif/rain3.gif",
        "assets/gif/rain3.gif",
    ]

    # Randomly select a gif
    selected_gif_path = random.choice(gif_urls)

    file = open(selected_gif_path, 'rb')

    await send_animation(
                update,
                animation=file,
                caption= str,
                parse_mode="HTML"
            )



