
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from blockchain.tip_contract import tip_call
from db.transactions import record_tip_by_t_username
from db.wallets import get_all_wallets_by_t_username
from blockchain.tip_contract import get_tip_balance
from blockchain.tx import check_tx_status
from utils.wallet import is_address, get_url_by_tx
from utils.convert import is_int, convert_to_int, human_format
from utils.jokes import get_tip_joke_text_and_animation
from utils.tokens import get_whitelist_token_by_symbol
from constants.parameters import PARAMETER_MIN_AMOUNT_JOKE
from db.parameters import get_param
from db.balances import get_balance_by_t_username
from constants.parameters import PARAMETER_TIP_FEE_BTT
from constants.globals import TIP_INSUFFICIENT_BALANCE

from .telegram_send import send_animation, send_text, send_html


# Define the tip function
async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # If the context args length is less than 2, return an error message
    
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
    
    whitelist_token = get_whitelist_token_by_symbol(symbol_name)
    amount_int = convert_to_int(amount)
    balance_sender = get_balance_by_t_username(sender.username, whitelist_token['symbol'])
    fee = int(get_param(PARAMETER_TIP_FEE_BTT))

    if balance_sender + fee < amount_int:
        await send_text(update, TIP_INSUFFICIENT_BALANCE.format(balance=human_format(balance_sender), symbol=whitelist_token['symbol'], max=human_format(balance_sender)))
        return

    result = record_tip_by_t_username(sender.username, receiver, amount_int, whitelist_token['symbol'])
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
        balance = get_tip_balance(wallet['address'])
        if balance >= amount_int:
            my_wallet = wallet

    if my_wallet is None:
        await send_text(update, 'You do not have enough $TIP to send')
        return
    else:
        print(f"TipOnChain by username: sender={sender} amount={amount} receiver={receiver_wallet}")

        tx = tip_call(my_wallet['address'], receiver_wallet['address'], amount_int, my_wallet['pk'])
        url = get_url_by_tx(tx)
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Explorer", url=url)]])
        if check_tx_status(tx) == True:
            await send_html(update, f"Tip successful from user @{sender.username} from his wallet #{my_wallet['name']} to user @{receiver}! to wallet #{receiver_wallet['name']}", reply_markup=reply_markup)
        else:
            await send_html(update, f"Tip failed for user @{receiver}!", reply_markup=reply_markup)


# Define the rain function
async def rain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # If the context args length is less than 2, return an error message
    if len(context.args) < 1:
        await send_text(update, 'Usage: /rain amount')
        return

    # Get the user and amount
    sender = update.message.from_user
    amount = context.args[0]
    receiver = context.args[1][1:]

    if is_int(amount) == False:
        await send_text(update, 'Invalid amount')
        return

    # Get all the users in the group
    users = update.message.chat.get_members_count()

    # Get a list of the usersname in the group
    return
    


