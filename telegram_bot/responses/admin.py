
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from db.transactions import record_welcome_bonus_by_t_username
from db.activity import get_unique_chat_ids
from db.parameters import get_param
from utils.wallet import is_address, get_url_by_tx
from utils.convert import is_int, convert_to_int

from blockchain.tip_contract import admin_set_TopUp_address, admin_set_fee
from blockchain.tx import check_tx_status

from db.users import setup_user, set_command_by_t_username
from constants.parameters import (
    PARAMETER_ADMIN_LIST,
    PARAMETER_TOP_UP_ADDRESS
)


from .telegram_send import send_html, send_html_noreply, send_text

async def admin_set_TOP_UP_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    """Set a topUp address called only once."""
    user = update.effective_user.username 
    
    
    admin_list_string = get_param(PARAMETER_ADMIN_LIST)
    admin_list =  admin_list_string.split('|')
    
    # Check if user is in admin list
    if user not in admin_list:
        await send_html(update, "You are not an admin.")
        
    # Call
    tx = admin_set_TopUp_address()
    
    url = get_url_by_tx(tx)
    
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Explorer", url=url)]])
    
    if check_tx_status(tx) == True:
        await send_html(update, f"TopUp address set successfully!", reply_markup=reply_markup)
    else:
        await send_html(update, f"TopUp address set failed!", reply_markup=reply_markup)

async def admin_PUT_fee(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Set a fee called only once."""
    user = update.effective_user.username

    admin_list_string = get_param(PARAMETER_ADMIN_LIST)
    admin_list =  admin_list_string.split('|')

    # Check if user is in admin list
    if user not in admin_list:
        await send_html(update, "You are not an admin.")
        
    # Get fee from args
    if len(context.args) == 1:
        fee = context.args[0]
        # Fee must be between 0 to 100
        if is_int(fee) == False or int(fee) < 0 or int(fee) > 100:
            await send_text(update, 'Invalid fee')
            return 
         
    else:
        await send_text(update, 'Usage: /adminSetFee feeProcent')
        return

    # Call
    tx = admin_set_fee()

    url = get_url_by_tx(tx)

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Explorer", url=url)]])

    if check_tx_status(tx) == True:
        await send_html(update, f"Fee set successfully!", reply_markup=reply_markup)
    else:
        await send_html(update, f"Fee set failed!", reply_markup=reply_markup)
    


