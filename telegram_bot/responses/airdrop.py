import random

from telegram import Update, ReplyKeyboardMarkup, Chat, Bot
from telegram.ext import ContextTypes

from db.activity import get_activity_by_chat_id, get_activity_by_chat_id_timeback
from db.transactions import record_airdrop_by_t_username
from utils.convert import is_int, convert_to_int, human_format
from db.parameters import get_param
from db.balances import get_balance_by_t_username
from constants.parameters import PARAMETER_AIRDROP_FEE_BTT
from constants.globals import AIRDROP_INSUFFICIENT_BALANCE

from .telegram_send import send_animation, send_text
from utils.tokens import get_whitelist_token_by_symbol


# Define the airdrop function
async def airdrop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # The airdrop is a feature available only in groups
    if update.message.chat.type == 'private':
        await send_text(update, "The airdrop feature is only available in groups.")
        return

    if len(context.args) == 2:
        amount = context.args[0]
        symbol_name = context.args[1]
    elif len(context.args) == 1:
        amount = context.args[0]
        symbol_name = 'BTT'
    else:
        await send_text(update, 'Usage: /airdrop <amount> <symbol>')
    whitelist_token = get_whitelist_token_by_symbol(symbol_name)
    
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
    balance_sender = get_balance_by_t_username(sender.username, whitelist_token['symbol'])

    if balance_sender < amount_int and amount_int > 0:
        await send_text(update, 
                        AIRDROP_INSUFFICIENT_BALANCE.format(balance=human_format(balance_sender),
                                                            symbol = whitelist_token['symbol'],
                                                            max=human_format(balance_sender)))
        return

    # Use get Activity by chat id
    users = get_activity_by_chat_id(update.message.chat.id)

    #If the sender is in the group, remove him from the list
    users = [user for user in users if user['t_username'] != sender.username]

    if len(users) == 0:
        await send_text(update, "☒ No active users in the group")
        return

    str = record_airdrop_by_t_username(sender.username, users, amount_int, whitelist_token['symbol'])

    # List of good night GIF URLs (replace with your own URLs)
    gif_urls = [
        "assets/gif/airdrop1.gif",
        "assets/gif/airdrop2.gif",
        "assets/gif/airdrop3.gif",
        "assets/gif/airdrop3.gif",
    ]

    # Randomly select a gif
    selected_gif_path = random.choice(gif_urls)

    file = open(selected_gif_path, 'rb')

    await send_animation(
                update, 
                animation=file,
                parse_mode="HTML",
                caption= str)



