
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from db.balances import get_balance_by_t_username
from db.wallets import get_all_wallets_by_t_username
from blockchain.tip_contract import get_tip_balance, get_tip_erc20_balance
from blockchain.wallet import get_balance
from blockchain.token_erc20 import get_erc20_balance
from utils.convert import is_int, convert_to_int, human_format
from utils.tokens import get_whitelist_addresses
from constants.responses import (
    RESPONSE_BALANCE_MAIN,
    RESPONSE_BALANCE_MAIN_ONCHAIN,
    RESPONSE_BALANCE_MAIN_ONCHAIN_WALLET,
    RESPONSE_BALANCE_MAIN_ONCHAIN_TIPBOT,
    RESPONSE_BALANCE_ERC20,
    RESPONSE_BALANCE_ERC20_TELEGRAM,
    RESPONSE_BALANCE_ERC20_TIPBOT

)
from utils.convert import human_format
from constants.globals import MAIN_SYMBOL

from .telegram_send import send_animation, send_text


# Define the balance command
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check the balance of the user."""
    message_text = update.message.text

    # Check if the bot is tagged in the message or the message is in a private chat
    if context.bot.username in message_text or update.message.chat.type == 'private':
        user = update.message.from_user
        loading_path = "assets/gif/loading.gif"
        file = open(loading_path, 'rb')
        msg_wait = await send_animation(
            update,
            animation=file,
            caption="\n\n Please wait while we query the #" + MAIN_SYMBOL + "Network ... \n\n "
        )

        balance = get_balance_by_t_username(user.username)
        wallets = get_all_wallets_by_t_username(user.username)
        erc20_tokens = get_whitelist_addresses()

        # Offline balance
        main_balance =  RESPONSE_BALANCE_MAIN.format(balance=human_format(balance))
        for token in erc20_tokens:
            balance_token = get_balance_by_t_username(user.username, token['symbol'])
            main_balance += RESPONSE_BALANCE_ERC20_TELEGRAM.format(balance=human_format(balance_token), symbol=token['symbol'])


        if len(wallets) > 1:
            main_balance += RESPONSE_BALANCE_MAIN_ONCHAIN

            # Online balance
            for wallet in wallets:
                balance_wallet = get_balance(wallet['address'])
                main_balance += RESPONSE_BALANCE_MAIN_ONCHAIN_WALLET.format(wallet=wallet['name'], balance=human_format(balance_wallet))

                for token in erc20_tokens:
                    balance_token = get_erc20_balance(token['address'], wallet['address'])
                    main_balance += RESPONSE_BALANCE_ERC20.format(balance=human_format(balance_token), symbol=token['symbol'])

                balance_tip = get_tip_balance(wallet['address'])
                main_balance += RESPONSE_BALANCE_MAIN_ONCHAIN_TIPBOT.format(balance=human_format(balance_tip))

                for token in erc20_tokens:
                    balance_token = get_tip_erc20_balance(token['address'], wallet['address'])
                    main_balance += RESPONSE_BALANCE_ERC20_TIPBOT.format(balance=human_format(balance_token), symbol=token['symbol'])

        await send_text(update, main_balance)
        await msg_wait.delete()



# Define the balance command
async def balance_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check the balance of the user."""
    message_text = update.message.text

    # Check if the bot is tagged in the message or the message is in a private chat
    if context.bot.username in message_text or update.message.chat.type == 'private':
        user = update.message.from_user
        balance = get_balance_by_t_username(user.username)
        erc20_tokens = get_whitelist_addresses()

        # Offline balance
        main_balance =  RESPONSE_BALANCE_MAIN.format(balance=human_format(balance))
        for token in erc20_tokens:
            balance_token = get_balance_by_t_username(user.username, token['symbol'])
            main_balance += RESPONSE_BALANCE_ERC20_TELEGRAM.format(balance=human_format(balance_token), symbol=token['symbol'])

        await send_text(update, main_balance)