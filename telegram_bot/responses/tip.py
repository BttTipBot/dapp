
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
from constants.parameters import PARAMETER_MIN_AMOUNT_JOKE
from db.parameters import get_param
from db.balances import get_balance_by_t_username
from constants.parameters import PARAMETER_TIP_FEE_BTT
from constants.globals import TIP_INSUFFICIENT_BALANCE


# Define the tip function
async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # If the context args length is less than 2, return an error message
    if len(context.args) < 2:
        await update.message.reply_text('Usage: /tip amount @user')
        return

    # Get the user and amount
    sender = update.message.from_user
    amount = context.args[0]
    receiver = context.args[1][1:]

    if is_int(amount) == False:
        await update.message.reply_text('Invalid amount')
        return

    if context.args[1][0] != '@':
        await update.message.reply_text("You must include the @ to send to a user \n\n Usage: /tip amount @user")
        return
    
    if sender.username == receiver:
        await update.message.reply_text("You can't tip yourself! 🤦‍♂️")
        return

    amount_int = convert_to_int(amount)
    balance_sender = get_balance_by_t_username(sender.username)
    fee = int(get_param(PARAMETER_TIP_FEE_BTT))

    if balance_sender + fee < amount_int:
        await update.message.reply_text(TIP_INSUFFICIENT_BALANCE.format(balance=human_format(balance_sender), max=human_format(balance_sender)))
        return

    result = record_tip_by_t_username(sender.username, receiver, amount_int)
    min_joke_amount = get_param(PARAMETER_MIN_AMOUNT_JOKE)

    if amount_int >= min_joke_amount:
        tip_animation = get_tip_joke_text_and_animation(amount_int)
        joke_animation = tip_animation['animation']
        joke = tip_animation['joke']
        await update.message.reply_animation(
            animation=joke_animation,
            caption=f"{result} \n\n {joke}",
        )
    else:
        await update.message.reply_text(result)
        

# Define the tip function
async def tipOnChain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # If the context args length is less than 2, return an error message
    if len(context.args) < 2:
        await update.message.reply_text('Usage: /tipOnChain <amount> <address>')
        return

    # Get the user and amount
    sender = update.message.from_user
    amount = context.args[0]
    receiver = context.args[1]

    # Get all the user's wallets
    wallets = get_all_wallets_by_t_username(sender.username)

    if is_address(receiver) == False:
        await update.message.reply_text('Invalid address')
        return

    if is_int(amount) == False:
        await update.message.reply_text('Invalid amount')
        return

    amount_int = convert_to_int(amount)


    # If the user has no wallets, return an error message
    if wallets == []:
        await update.message.reply_text('You have no wallets. Please create a wallet first.')
        return
    else:
        my_wallet = None
        # Iterate through the wallets and get the $TIP balance
        for wallet in wallets:
            balance = get_tip_balance(wallet['address'])
            if balance >= amount_int:
                my_wallet = wallet
        
        if my_wallet is None:
            await update.message.reply_text('You do not have enough $TIP to send')
            return
        else:
            print(f"Tip: sender={sender} amount={amount} receiver={receiver}")

            tx = tip_call(my_wallet['address'],receiver, amount_int, my_wallet['pk'])
            url = get_url_by_tx(tx)
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Explorer", url=url)]])
            if check_tx_status(tx) == True:
                await update.message.reply_html(f"Tip successful! Transaction hash: {tx}", reply_markup=reply_markup)
            else:
                await update.message.reply_html(f"Tip failed! Transaction hash: {tx}", reply_markup=reply_markup)

