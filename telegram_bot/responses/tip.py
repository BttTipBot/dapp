
import os

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from blockchain.tip_contract import tip_call, tip_erc20_call
from db.transactions import record_tip_by_t_username
from db.wallets import get_all_wallets_by_t_username
from blockchain.tip_contract import get_tip_balance, get_tip_erc20_balance
from blockchain.tx import check_tx_status
from utils.wallet import is_address, get_url_by_tx
from utils.convert import is_int, convert_to_int, human_format
from utils.jokes import get_tip_joke_text_and_animation
from utils.tokens import get_whitelist_token_by_symbol
from constants.parameters import PARAMETER_MIN_AMOUNT_JOKE
from db.parameters import get_param
from db.balances import get_balance_by_t_username
from constants.parameters import PARAMETER_TIP_FEE_BTT
from constants.globals import TIP_INSUFFICIENT_BALANCE, BTT_SYMBOL
from constants.responses_gives import RESPONSE_NOT_ENOUGH_BALANCE_ON_CHAIN, RESPONSE_NOT_ENOUGH_BALANCE_ON_TELEGRAM

from .telegram_send import send_animation, send_text, send_html


async def get_input_arguments(update, context):
    # Get the reply message sender
    if len(context.args) == 3:
        # 1. Case all the parameters are passed
        amount = context.args[0]
        symbol_name = context.args[1]
        receiver = context.args[2][1:]

        if(context.args[2][0] != '@'):
            await send_text(update, "You must include the @ to send to a user \n\n Usage: /tip amount $TIP @user")
            return
    elif len(context.args) == 2:
        amount = context.args[0]
        symbol_name = "btt"
        receiver = context.args[1][1:]
        
        # Case 2. Two arguments are passed 
        # Case 2.1 The user is replying to a message so is saying /tip amount $TIP
        # Case 2.2 The user is saying /tip amount @user
        
        # Note we assume that the user is using second case and if is not @ we assume is the first case

        if(context.args[1][0] != '@'):
            # it could be that the user is replying to a message
            if update.message.reply_to_message is None:
                await send_text(update, "You must include the @ to send to a user \n\n Usage: /tip amount @user")
                return
            else:
                reply_sender = update.message.reply_to_message.from_user
                receiver = reply_sender.username
                symbol_name = context.args[1]

    elif len(context.args) == 1 and update.message.reply_to_message is not None:
        print("context.args", context.args)
        amount = context.args[0]
        symbol_name = "btt"
        
        if update.message.reply_to_message is None:
            await send_text(update, 'Usage: /tip <amount> <symbol> @user')
            return
        else:
            reply_sender = update.message.reply_to_message.from_user
            receiver = reply_sender.username
    else:
        print("context.args", context.args)
        await send_text(update, 'Usage: /tip <amount> <symbol> @user')
        return

    if is_int(amount) == False:
        await send_text(update, 'Invalid amount')
        return

    sender = update.message.from_user
    if sender.username == receiver:
        await send_text(update, "You can't tip yourself! 🤦‍♂️")
        return 
    
    return { 'sender': sender.username,
            'amount': amount,
            'symbol_name': symbol_name,
            'receiver': receiver
            }

# Define the tip function
async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    # Get the input arguments
    input_arguments = await get_input_arguments(update, context)
    symbol_name = input_arguments['symbol_name']
    amount = input_arguments['amount']
    sender = input_arguments['sender']
    receiver = input_arguments['receiver']

    # Process the tip
    whitelist_token = get_whitelist_token_by_symbol(symbol_name)
    amount_int = convert_to_int(amount)
    balance_sender = get_balance_by_t_username(sender, whitelist_token['symbol'])
    fee = int(get_param(PARAMETER_TIP_FEE_BTT))

    # Check if the user has enough balance
    if balance_sender < amount_int:
        TIP_BOT_URL = os.getenv('TIP_BOT_URL')
        await send_text(update, RESPONSE_NOT_ENOUGH_BALANCE_ON_TELEGRAM.format(url=TIP_BOT_URL))
        return

    result = record_tip_by_t_username(sender, receiver, amount_int, whitelist_token['symbol'])
    min_joke_amount = get_param(PARAMETER_MIN_AMOUNT_JOKE)

    if amount_int >= min_joke_amount:
        tip_animation = get_tip_joke_text_and_animation(amount_int)
        joke_animation = tip_animation['animation']
        joke = tip_animation['joke']
        await send_animation( update,
            animation=joke_animation,
            caption=f"{result} \n\n {joke}",
        )
    else:
        await send_text(update, result)
        

# Define the tip function
async def tipOnChain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # Get the reply message sender
    if len(context.args) == 3:
        amount = context.args[0]
        symbol_name = context.args[1]
        receiver = context.args[2][1:]

        if(context.args[2][0] != '@'):
            await send_text(update, "You must include the @ to send to a user \n\n Usage: /tipOnChain amount $TIP @user")
            return
    elif len(context.args) == 2:
        amount = context.args[0]
        symbol_name = "btt"
        receiver = context.args[1][1:]

        if(context.args[1][0] != '@'):
            # it could be that the user is replying to a message
            if update.message.reply_to_message is None:
                await send_text(update, "You must include the @ to send to a user \n\n Usage: /tipOnChain amount @user")
                return
            else:
                reply_sender = update.message.reply_to_message.from_user
                receiver = reply_sender.username
                symbol_name = context.args[1]
    elif len(context.args) == 1 and update.message.reply_to_message is not None:
        print("context.args", context.args)
        amount = context.args[0]
        symbol_name = "btt"
        
        if update.message.reply_to_message is None:
            await send_text(update, 'Usage: /tipOnChain <amount> <symbol> @user')
            return
        else:
            reply_sender = update.message.reply_to_message.from_user
            receiver = reply_sender.username
    else:
        print("context.args", context.args)
        await send_text(update, 'Usage: /tipOnChain <amount> <symbol> @user')
        return

    if is_int(amount) == False:
        await send_text(update, 'Invalid amount')
        return

    sender = update.message.from_user
    if sender.username == receiver:
        await send_text(update, "You can't tip yourself! 🤦‍♂️")
        return

    whitelist_token = get_whitelist_token_by_symbol(symbol_name)
    amount_int = convert_to_int(amount)
    
    # Get all the user's wallets
    wallets = get_all_wallets_by_t_username(sender.username)
    
    # If the user has no wallets, return an error message
    if wallets == []:
        await send_text(update, 'You have no wallets. Please create a wallet first.')
        return

    # Get the user's wallets
    wallets_receiver = get_all_wallets_by_t_username(receiver)

    if wallets_receiver == []:
        await send_text(update, f'The receiver has no wallets. Please ask them to create a wallet first. \n\n User @{sender.username} wants to tip you @{receiver} \n\n Please create a wallet @{receiver} to receive OnChain Tips.')
        return

    receiver_wallet = wallets_receiver[0]
    my_wallet = None

    for wallet in wallets:
        if BTT_SYMBOL == whitelist_token['symbol']:
            balance = get_tip_balance(wallet['address'])
        else:   
            balance = get_tip_erc20_balance(whitelist_token['address'], wallet['address'])
        if balance >= amount_int:
            my_wallet = wallet

    if my_wallet is None:
        TIP_BOT_URL = os.getenv('TIP_BOT_URL')
        await send_text(update, RESPONSE_NOT_ENOUGH_BALANCE_ON_CHAIN.format(url=TIP_BOT_URL))
        return
    else:
        print(f"TipOnChain by username: sender={sender} amount={amount} receiver={receiver_wallet}")

        if BTT_SYMBOL == whitelist_token['symbol']:
            tx = tip_call(my_wallet['address'], receiver_wallet['address'], amount_int, my_wallet['pk'])
        else:
            tx = tip_erc20_call(amount_int, my_wallet['address'], receiver_wallet['address'], my_wallet['pk'], whitelist_token['address'])
        url = get_url_by_tx(tx)
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Explorer", url=url)]])
        if check_tx_status(tx) == True:
            min_joke_amount = get_param(PARAMETER_MIN_AMOUNT_JOKE)
            tip_animation = get_tip_joke_text_and_animation(amount_int)
            joke_animation = tip_animation['animation']
            joke = tip_animation['joke']
            result = f"Tip successful {human_format(amount_int)} {whitelist_token['symbol']} from user @{sender.username} from his wallet #{my_wallet['name']} to user @{receiver}! to wallet #{receiver_wallet['name']}"
            await send_animation(update,
                                 joke_animation,
                                 caption=f"{result} \n\n {joke}",
                                 reply_markup=reply_markup)

        else:
            await send_html(update, f"Tip failed for user @{receiver}!", reply_markup=reply_markup)
