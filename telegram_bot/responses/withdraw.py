
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from steps.command_steps import is_in_steps, get_step, get_arguments, add_step
from utils.convert import is_int, convert_to_int, human_format
from utils.wallet import get_wallet_full_name, get_url_by_tx, get_my_wallet_t, is_address
from utils.qr_image import qrcode_create
from blockchain.wallet import create_wallet, get_address_and_private_key, get_balance, transfer_eth
from blockchain.tip_contract import withdraw_tip_top_up, withdraw_top_up_erc20_tip
from blockchain.tx import check_tx_status
from db.transactions import top_up_balance_by_t_username, withdraw_balance_by_t_username
from utils.wallet import get_my_wallet_t
from db.users import set_command_by_t_username, get_command_by_t_username
from db.wallets import get_all_wallets_by_t_username
from db.balances import get_balance_by_t_username
from db.parameters import get_param
from utils.tokens import get_whitelist_token_by_symbol
from constants.globals import (
    USER_MAIN_MENU_BUTTON,
    WITHDRAW_BUTTON_ON_ADDRESS,
    WITHDRAW_BUTTON_ON_ACCOUNT,
    WALLET_SELECT_BUTTON,
    BTT_SYMBOL
    
)

from constants.responses import (
    TEXT_INVALID_TOKEN_SYMBOL,
    RESPONSE_WITHDRAW_SUCCESS,
    RESPONSE_WITHDRAW_FAILED,
    TEXT_INVALID_AMOUNT,
    EXAMPLE_AMOUNT,
    TEXT_INVALID_AMOUNT_ADDRESS,
    TEXT_INVALID_AMOUNT_ADDRESS_SYMBOL,
    EXAMPLE_ADDRESS_AMOUNT,
    EXAMPLE_ADDRESS_AMOUNT_SYMBOL,
    WALLET_NOT_FOUND,
    RESPONSE_WITHDRAW_INPUT_AMOUNT_ADDRESS_SYMBOL,
    RESPONSE_WITHDRAW_INPUT_AMOUNT_SYMBOL,
    RESPONSE_WITHDRAW_MINIMUM,
    RESPONSE_WITHDRAW_OPTIONS,
)


from constants.parameters import PARAMETER_MINIMUM_WITHDRAW_BTT

from .telegram_send import send_text, send_html

# Wallet goes to
async def withdraw_btt(update, context):
    user = update.effective_user
    # Check if the command was sent in a private chat
    if update.message.chat.type == 'private':
        balance = get_balance_by_t_username(user.username)
        min_balance = int(get_param(PARAMETER_MINIMUM_WITHDRAW_BTT))

        if balance < min_balance:
            await context.bot.send_message(user.id, RESPONSE_WITHDRAW_MINIMUM.format(amount=human_format(min_balance), balance=human_format(balance)))
        else:
            wallets = get_all_wallets_by_t_username(user.username)
            if wallets == []:
                keyboard = [[WITHDRAW_BUTTON_ON_ADDRESS]]
            else:
                keyboard = [ [WITHDRAW_BUTTON_ON_ADDRESS] ]
                for wallet in wallets:
                    keyboard.append([ WITHDRAW_BUTTON_ON_ACCOUNT + get_wallet_full_name(wallet) ])
            keyboard.append([USER_MAIN_MENU_BUTTON])

            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await context.bot.send_message(user.id, RESPONSE_WITHDRAW_OPTIONS, reply_markup=reply_markup)


async def withdraw_btt_in_wallet(update, context):
    user = update.effective_user
    # Check if the command was sent in a private chat
    if update.message.chat.type == 'private':
        command = get_command_by_t_username(user.username)
        if is_in_steps(command):
            step = get_step(command)
            arguments = get_arguments(command)
            if step == 1:
                input = update.message.text

                if " " in input:
                    withdraw_amount = input.split(" ")[0]
                    symbol_name = input.split(" ")[1]
                else:
                    withdraw_amount = input
                    symbol_name = "btt"
                whitelist_token = get_whitelist_token_by_symbol(symbol_name)

                if is_int(withdraw_amount) == False:
                    await send_text(update, TEXT_INVALID_AMOUNT.format(text=withdraw_amount) + EXAMPLE_AMOUNT)
                elif whitelist_token is None:
                    await send_text(update, TEXT_INVALID_TOKEN_SYMBOL.format(text=symbol_name) + EXAMPLE_AMOUNT)
                else:
                    wallet_name = arguments[1]
                    my_wallet = get_my_wallet_t(user.username, wallet_name)
                    
                    if my_wallet is not None:
                        withdraw_amount_int = convert_to_int(withdraw_amount)
                        if whitelist_token['symbol'] == BTT_SYMBOL:
                            balance = get_balance_by_t_username(user.username)
                        else:
                            balance = get_balance_by_t_username(user.username, whitelist_token['symbol'])
                        min_balance = int(get_param(PARAMETER_MINIMUM_WITHDRAW_BTT))
                        if balance < min_balance or withdraw_amount_int > balance or withdraw_amount_int < min_balance:
                            reply_markup = ReplyKeyboardMarkup([[USER_MAIN_MENU_BUTTON]], resize_keyboard=True)
                            await context.bot.send_message(user.id, RESPONSE_WITHDRAW_MINIMUM.format(amount=human_format(min_balance), balance=human_format(balance)), reply_markup=reply_markup)
                        else:
                            # Withdraw the amount
                            set_command_by_t_username(user.username, WALLET_SELECT_BUTTON + my_wallet['name'])
                            if whitelist_token['symbol'] == BTT_SYMBOL:
                                tx = withdraw_tip_top_up(my_wallet['address'], withdraw_amount_int)
                            else:
                                tx = withdraw_top_up_erc20_tip(my_wallet['address'], withdraw_amount_int, whitelist_token['address'])
                            url = get_url_by_tx(tx)
                            
                            if check_tx_status(tx) == True:
                                withdraw_balance_by_t_username(tx, user.username, withdraw_amount_int, whitelist_token['address'])
                                reply_markup = ReplyKeyboardMarkup([[USER_MAIN_MENU_BUTTON]], resize_keyboard=True)
                                await send_html(update, RESPONSE_WITHDRAW_SUCCESS.format(amount=human_format(withdraw_amount_int), symbol = whitelist_token['symbol'], url=url), reply_markup=reply_markup)
                            else:
                                reply_markup = ReplyKeyboardMarkup([[USER_MAIN_MENU_BUTTON]], resize_keyboard=True)
                                await send_text(update, RESPONSE_WITHDRAW_FAILED.format(amount=human_format(withdraw_amount_int), symbol = whitelist_token['symbol'], url=url), reply_markup=reply_markup)

        else:
            wallet_name = update.message.text.replace(WITHDRAW_BUTTON_ON_ACCOUNT, "")
            my_wallet = get_my_wallet_t(user.username, wallet_name)
            command = add_step(update.message.text, my_wallet['name'])
            set_command_by_t_username(user.username, command)

            if my_wallet is not None:
                await context.bot.send_message(user.id, RESPONSE_WITHDRAW_INPUT_AMOUNT_SYMBOL)
            else:
                await context.bot.send_message(user.id, WALLET_NOT_FOUND.format(wallet=wallet_name))


async def withdraw_btt_in_address(update, context):
    user = update.effective_user
    # Check if the command was sent in a private chat
    if update.message.chat.type == 'private':
        command = get_command_by_t_username(user.username)
        print(f"wallet_deposit: command: {command}")
        if command == WITHDRAW_BUTTON_ON_ADDRESS:
            
            # Check the input
            input  = update.message.text

            if len(update.message.text.split(" "))  == 3:
                address = update.message.text.split(" ")[0]
                withdraw_amount = update.message.text.split(" ")[1]
                symbol_name = update.message.text.split(" ")[2]
            elif len(update.message.text.split(" "))  == 2:
                address = update.message.text.split(" ")[0]
                withdraw_amount = update.message.text.split(" ")[1]
                symbol_name = "btt"
            else:
                await send_text(update, TEXT_INVALID_AMOUNT_ADDRESS_SYMBOL.format(text=update.message.text) + EXAMPLE_ADDRESS_AMOUNT_SYMBOL)
                return
            whitelist_token = get_whitelist_token_by_symbol(symbol_name)

            if is_int(withdraw_amount) == False or is_address(address) == False:
                await send_text(update, TEXT_INVALID_AMOUNT.format(text=update.message.text) + EXAMPLE_ADDRESS_AMOUNT)
            elif whitelist_token is None:
                await send_text(update, TEXT_INVALID_TOKEN_SYMBOL.format(text=symbol_name) + EXAMPLE_AMOUNT)
            else:
                withdraw_amount_int = convert_to_int(withdraw_amount)
                if whitelist_token['symbol'] == BTT_SYMBOL:
                    balance = get_balance_by_t_username(user.username)
                else:
                    balance = get_balance_by_t_username(user.username, whitelist_token['symbol'])
                min_balance = int(get_param(PARAMETER_MINIMUM_WITHDRAW_BTT))
                if balance < min_balance or withdraw_amount_int > balance or withdraw_amount_int < min_balance:
                    reply_markup = ReplyKeyboardMarkup([[USER_MAIN_MENU_BUTTON]], resize_keyboard=True)
                    await context.bot.send_message(user.id, RESPONSE_WITHDRAW_MINIMUM.format(amount=human_format(min_balance), balance=human_format(balance)), reply_markup=reply_markup)
                else:
                    # Withdraw the amount
                    set_command_by_t_username(user.username, USER_MAIN_MENU_BUTTON)
                    if whitelist_token['symbol'] == BTT_SYMBOL:
                        tx = withdraw_tip_top_up(address, withdraw_amount_int)
                    else:
                        tx = withdraw_top_up_erc20_tip(address, withdraw_amount_int, whitelist_token['address'])
                    url = get_url_by_tx(tx)
                    if check_tx_status(tx) == True:
                        withdraw_balance_by_t_username(tx, user.username, withdraw_amount_int, whitelist_token['address'])
                        reply_markup = ReplyKeyboardMarkup([[USER_MAIN_MENU_BUTTON]], resize_keyboard=True)
                        await send_html(update, RESPONSE_WITHDRAW_SUCCESS.format(amount=human_format(withdraw_amount_int), symbol = whitelist_token['symbol'], url=url), reply_markup=reply_markup)
                    else:
                        reply_markup = ReplyKeyboardMarkup([[USER_MAIN_MENU_BUTTON]], resize_keyboard=True)
                        await send_text(update, RESPONSE_WITHDRAW_FAILED.format(amount=human_format(withdraw_amount_int), symbol = whitelist_token['symbol'], url=url), reply_markup=reply_markup)

        else:
            set_command_by_t_username(user.username, WITHDRAW_BUTTON_ON_ADDRESS)
            await context.bot.send_message(user.id, RESPONSE_WITHDRAW_INPUT_AMOUNT_ADDRESS_SYMBOL)