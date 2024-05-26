
import os

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from blockchain.tip_contract import tip_call, tip_erc20_call
from db.transactions import record_tip_by_t_username
from db.wallets import get_all_wallets_by_t_username
from blockchain.tip_contract import withdraw_tip_top_up, withdraw_top_up_erc20_tip
from blockchain.token_erc20 import transfer_erc20_balance, get_erc20_balance
from blockchain.tx import check_tx_status
from blockchain.wallet import get_balance, transfer_eth
from utils.wallet import is_address, get_url_by_tx
from utils.convert import is_int, convert_to_int, human_format
from utils.jokes import get_tip_joke_text_and_animation
from utils.tokens import get_whitelist_token_by_symbol
from constants.parameters import PARAMETER_MIN_AMOUNT_JOKE
from db.parameters import get_param
from db.balances import get_balance_by_t_username
from db.transactions import record_burn_by_t_username, reset_burn
from constants.parameters import PARAMETER_TIP_FEE_BTT
from constants.globals import TIP_INSUFFICIENT_BALANCE, BTT_SYMBOL
from constants.responses_gives import RESPONSE_NOT_ENOUGH_BALANCE_ON_CHAIN, RESPONSE_NOT_ENOUGH_BALANCE_ON_TELEGRAM

from .telegram_send import send_animation, send_text, send_html


async def burn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    burn_username = "OnChainVision"
    sender = update.message.from_user.username
    
    # Get the reply message sender
    if len(context.args) == 2:
        amount = context.args[0]
        symbol_name = context.args[1]
    else:
        print("context.args", context.args)
        await send_text(update, 'Usage: /burn amount symbol')
        return
    
    
    whitelist_token = get_whitelist_token_by_symbol(symbol_name)
    amount_int = convert_to_int(amount)
    balance_sender = get_balance_by_t_username(sender, whitelist_token['symbol'])
    
    # Check if the user has enough balance
    if balance_sender < amount_int:
        TIP_BOT_URL = os.getenv('TIP_BOT_URL')
        await send_text(update, f"Not enough balance. 🤕 \n\n Balance: {human_format(balance_sender)} {whitelist_token['symbol']}")
        return

    record_burn_by_t_username(sender, burn_username, amount_int, whitelist_token['symbol'])
    balance_burn = get_balance_by_t_username(burn_username, whitelist_token['symbol'])

    result = f"Burn successful 🔥✅ \n\n {human_format(amount_int)} {whitelist_token['symbol']} \n\n @{sender} \n\n Burned 🔥 so far {human_format(balance_burn)} {whitelist_token['symbol']}"
    burn_animation = "assets/gif/burn.mp4"
    file = open(burn_animation, 'rb')
    await send_animation(update,
                        file,
                        caption=f"{result} \n\n 🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥")




async def trigger_burn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sender = update.message.from_user.username
    burn_username = "OnChainVision"
    receiver_wallet = "0x000000000000000000000000000000000000dEaD"
    
    if sender != "constantin_pricope":
        await send_text(update, 'You are not authorized to burn tokens on chain.')
        return

    if len(context.args) == 1:
        symbol_name = context.args[0]
    else:
        await send_text(update, 'Usage: /trigger_burn symbol')
        return
    
    whitelist_token = get_whitelist_token_by_symbol(symbol_name)
    balance_burn = get_balance_by_t_username(burn_username, whitelist_token['symbol'])
    
    if whitelist_token['symbol'] == BTT_SYMBOL:
        tx = withdraw_tip_top_up(receiver_wallet, balance_burn)
    else:
        tx = withdraw_top_up_erc20_tip(receiver_wallet, balance_burn, whitelist_token['address'])
    url = get_url_by_tx(tx)
    
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Explorer", url=url)]])
    if check_tx_status(tx) == True:
        
        reset_burn(burn_username, balance_burn, whitelist_token['symbol'])
        
        burn_animation = "assets/gif/burn.mp4"
        file = open(burn_animation, 'rb')

        result = f"Burn successful from topUp balance🔥✅ \n\n {human_format(balance_burn)} {whitelist_token['symbol']}"
        await send_animation(update,
                                file,
                                caption=f"{result} \n\n 🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥",
                                reply_markup=reply_markup)

    else:
        await send_html(update, f"Burn unsuccessful!", reply_markup=reply_markup)

    

# Define the tip function
async def BurnOnChain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    receiver_wallet = "0x000000000000000000000000000000000000dEaD"

    # Get the reply message sender
    if len(context.args) == 2:
        amount = context.args[0]
        symbol_name = context.args[1]
    else:
        print("context.args", context.args)
        await send_text(update, 'Usage: /burnOnChain amount symbol')
        return

    if is_int(amount) == False:
        await send_text(update, 'Invalid amount')
        return

    sender = update.message.from_user

    whitelist_token = get_whitelist_token_by_symbol(symbol_name)
    amount_int = convert_to_int(amount)
    
    # Get all the user's wallets
    wallets = get_all_wallets_by_t_username(sender.username)
    
    # If the user has no wallets, return an error message
    if wallets == []:
        await send_text(update, 'You have no wallets. Please create a wallet first.')
        return

    my_wallet = None

    for wallet in wallets:
        if BTT_SYMBOL == whitelist_token['symbol']:
            balance = get_balance(wallet['address'])
        else:   
            balance = get_erc20_balance(whitelist_token['address'], wallet['address'])
        if balance >= amount_int:
            my_wallet = wallet

    if my_wallet is None:
        TIP_BOT_URL = os.getenv('TIP_BOT_URL')
        await send_text(update, RESPONSE_NOT_ENOUGH_BALANCE_ON_CHAIN.format(url=TIP_BOT_URL))
        return
    else:
        print(f"burnOnChain by username: sender={sender} amount={amount} receiver={receiver_wallet}")

        if whitelist_token['symbol'] == BTT_SYMBOL:
            tx = transfer_eth(my_wallet['address'], receiver_wallet, amount_int, my_wallet['pk'])
        else:
            tx = transfer_erc20_balance(whitelist_token['address'], my_wallet['address'], receiver_wallet, amount_int, my_wallet['pk'])
        url = get_url_by_tx(tx)
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Explorer", url=url)]])
        if check_tx_status(tx) == True:
            burn_animation = "assets/gif/burn.mp4"
            file = open(burn_animation, 'rb')
            
            
            result = f"Burn successful 🔥✅ \n\n {human_format(amount_int)} {whitelist_token['symbol']} \n\n @{sender.username} wallet #{my_wallet['name']}"
            await send_animation(update,
                                 file,
                                 caption=f"{result} \n\n 🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥",
                                 reply_markup=reply_markup)

        else:
            await send_html(update, f"Burn unsuccessful for user @{receiver_wallet}!", reply_markup=reply_markup)
