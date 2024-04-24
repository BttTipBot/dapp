import asyncio
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from steps.command_steps import is_in_steps, get_step, get_arguments, add_step
from utils.convert import is_int, convert_to_int, human_format
from utils.qr_image import qrcode_create
from utils.wallet import get_wallet_full_name, get_url_by_tx, get_my_wallet_t
from blockchain.wallet import get_balance, transfer_eth
from blockchain.tip_contract import get_tip_balance, deposit_tip, deposit_erc20, withdraw_tip, withdraw_erc20, top_up_tip, top_up_erc20, get_tip_erc20_balance
from blockchain.token_erc20 import get_erc20_balance, transfer_erc20_balance
from blockchain.tx import check_tx_status
from db.transactions import top_up_balance_by_t_username
from db.wallets import get_all_wallets_by_t_username, add_wallet_by_t_username
from db.users import set_command_by_t_username, get_command_by_t_username
from db.wallets import delete_wallet_name_by_t_username
from db.parameters import get_param
from utils.tokens import get_whitelist_addresses, get_whitelist_token_by_symbol
from constants.globals import (
    WALLET_BUTTON,
    WALLET_NEW_BUTTON,
    WALLET_SELECT_BUTTON,
    WALLET_EXPORT_BUTTON,
    WALLET_DEPOSIT_BUTTON,
    WALLET_WITHDRAW_BUTTON,
    WALLET_TOPUP_BUTTON,
    WALLET_DELETE_BUTTON,
    WALLET_ONCHAIN_TRANSFER_BUTTON,
    MESSAGE_WALLET_TRANSFER_ON_CHAIN,
    MESSAGE_WALLET_TOP_UP,
    MESSAGE_CHOSE_WALLET,
    MESSAGE_WALLET_NOT_FOUND,
    MESSAGE_WALLET_MENU,
    MESSAGE_WALLET_INSUFFICIENT_FEE,
    MESSAGE_WALLET_INSUFFICIENT_BALANCE,
    MESSAGE_WALLET_DEPOSIT,
    MESSAGE_WALLET_WITHDRAW,
    MESSAGE_WALLET_INSUFFICIENT_TIP,
    USER_MAIN_MENU_BUTTON
)
from constants.responses import (
    TEXT_INVALID_AMOUNT,
    TEXT_INVALID_TOKEN_SYMBOL,
    EXAMPLE_AMOUNT,
    RESPONSE_WALLET_TOPUP_SUCCESS,
    RESPONSE_WALLET_DEPOSIT_SUCCESS,
    RESPONSE_WALLET_WITHDRAW_SUCCESS,
    RESPONSE_WALLET_TRANSFER_SUCCESS,
    RESPONSE_WALLET_TOPUP_FAILED,
    RESPONSE_WALLET_EXPORT,
    RESPONSE_WALLET_DEPOSIT_FAILED,
    RESPONSE_WALLET_WITHDRAW_FAILED,
    RESPONSE_WALLET_TRANSFER_FAILED,
    RESPONSE_WALLET_DELETE_SUCCESS,
    RESPONSE_BALANCE_ERC20,
    RESPONSE_BALANCE_ERC20_TIPBOT,
    RESPONSE_BALANCE_MAIN_ONCHAIN_TIPBOT,

)

from constants.responses_wallet import (
    RESPONSE_WALLET_MENU,
    RESPONSE_WALLET_DEPOSIT,
    RESPONSE_WALLET_WITHDRAW,
    RESPONSE_WALLET_TOPUP,
    RESPONSE_WALLET_TRANSFER,
    
)

from constants.parameters import PARAMETER_MINIMUM_FEES

from .telegram_send import send_photo, send_animation, send_text, send_html

btt_symbol = 'BTT'


#   1.2. Your wallet options (wallet_options) -  Checks on previous command - fallback - WALLET_BUTTON
#     1.2.1. Deposit (wallet_deposit)
#     1.2.2. Withdraw (wallet_withdraw)
#     1.2.3. Delete (wallet_delete)
#     1.2.4. Topup (wallet_topup)
#     1.2.5. Transfer (wallet_onchain_transfer)
#   1.3. Main Menu (wallet_main_menu)

# _response goes to the response of the previous command and usually comes from a fallback command
# The fallback command is used to handle unmatched commands based on the previous state

# Wallet goes to
async def wallet_private(update, context):
    user = update.effective_user
    set_command_by_t_username(user.username, WALLET_BUTTON)
    # Check if the command was sent in a private chat
    if update.message.chat.type == 'private':
        # Now let's send a private message to the user
        # We must select the avaialable wallets for the user and let the user choose one or create a new one
        wallets = get_all_wallets_by_t_username(user.username)
        if wallets == []:
            keyboard = [[WALLET_NEW_BUTTON]]
        else:
            keyboard = [[WALLET_NEW_BUTTON]]
            for wallet in wallets:
                keyboard.append([get_wallet_full_name(wallet)])
        keyboard.append([USER_MAIN_MENU_BUTTON])

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await context.bot.send_message(user.id, MESSAGE_CHOSE_WALLET, reply_markup=reply_markup)

# Each unique wallet has its own options
async def wallet_options(update, context):
    user = update.effective_user
    command = get_command_by_t_username(user.username)
    set_command_by_t_username(user.username, WALLET_SELECT_BUTTON)
    # Check if the command was sent in a private chat
    if update.message.chat.type == 'private':
        # Get the name of the wallet from the user's response

        wallets = get_all_wallets_by_t_username(user.username)

        if command.startswith(WALLET_SELECT_BUTTON):
            wallet_name = command.replace(WALLET_SELECT_BUTTON, "")
            my_wallet = next((wallet for wallet in wallets if wallet['name'] == wallet_name), None)
        else:
            wallet_name = update.message.text
            my_wallet = next((wallet for wallet in wallets if get_wallet_full_name(wallet) == wallet_name), None)

        if my_wallet is None or wallets == []:
            await send_text(update, MESSAGE_WALLET_NOT_FOUND.format(wallet=wallet_name))
        else:
            loading_path = "assets/gif/loading.gif"
            file = open(loading_path, 'rb')
            # a wait message as query to Blockchain will take a while
            keyboard = [
                [WALLET_DEPOSIT_BUTTON + my_wallet['name'], WALLET_TOPUP_BUTTON + my_wallet['name'], WALLET_WITHDRAW_BUTTON + my_wallet['name']],
                [WALLET_EXPORT_BUTTON + my_wallet['name'], WALLET_ONCHAIN_TRANSFER_BUTTON + my_wallet['name'], WALLET_DELETE_BUTTON + my_wallet['name']],
                [WALLET_BUTTON]
            ] 
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            try:
                msg_wait = await send_animation(
                    update, 
                    animation=file,
                    caption="\n\n Please wait while we query the #BttNetwork ... \n\n ",
                    reply_markup=reply_markup
                )
            except Exception as e:
                msg_wait = None
                print(f"wallet_options msg_wait Error: {e}")

            img = qrcode_create(my_wallet['address'])

            # Let's get the balance of the wallet
            balance = get_balance(my_wallet['address'])
            balance_tips = get_tip_balance(my_wallet['address'])


            msg = RESPONSE_WALLET_MENU.format(wallet=my_wallet['name'], address=my_wallet['address'], balance=human_format(balance), balance_tips=human_format(balance_tips))
                                              
            erc20_tokens = get_whitelist_addresses()
            for token in erc20_tokens:
                balance_token = get_erc20_balance(token['address'], my_wallet['address'])
                msg += RESPONSE_BALANCE_ERC20.format(balance=human_format(balance_token), symbol=token['symbol'])

            balance_tip = get_tip_balance(my_wallet['address'])
            msg += RESPONSE_BALANCE_MAIN_ONCHAIN_TIPBOT.format(balance=human_format(balance_tip))

            for token in erc20_tokens:
                balance_token = get_tip_erc20_balance(token['address'], my_wallet['address'])
                msg += RESPONSE_BALANCE_ERC20_TIPBOT.format(balance=human_format(balance_token), symbol=token['symbol'])


            # Edit previous message with the new media and caption
            await send_photo(update, 
                             photo=img, 
                             caption=msg,
                             parse_mode='Markdown',
                             reply_markup=reply_markup)
            
            if msg_wait != None:
                    await msg_wait.delete()

# Each unique wallet has its own options
async def wallet_export(update, context):
    user = update.effective_user
    # Check if the command was sent in a private chat
    if update.message.chat.type == 'private':
        # Get the name of the wallet from the user's response
        wallets = get_all_wallets_by_t_username(user.username)
        wallet_name = update.message.text.replace(WALLET_EXPORT_BUTTON, "")
        my_wallet = get_my_wallet_t(user.username, wallet_name)

        if my_wallet is None or wallets == []:
            await send_text(update, MESSAGE_WALLET_NOT_FOUND.format(wallet=wallet_name))
        else:
            # Let's get the balance of the wallet
            keyboard = [
                [WALLET_DEPOSIT_BUTTON + my_wallet['name'], WALLET_TOPUP_BUTTON + my_wallet['name'], WALLET_WITHDRAW_BUTTON + my_wallet['name']],
                [WALLET_EXPORT_BUTTON + my_wallet['name'], WALLET_ONCHAIN_TRANSFER_BUTTON + my_wallet['name'], WALLET_DELETE_BUTTON + my_wallet['name']],
                [WALLET_BUTTON]
            ]

            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

            # Send an message and delete the message after 10 seconds
            ret = await send_text(update, RESPONSE_WALLET_EXPORT.format(pk=my_wallet['pk']), reply_markup=reply_markup)
            asyncio.create_task(delete_message_after_delay(update, context, ret, 10))

async def delete_message_after_delay(update, context, message, delay):
    await asyncio.sleep(delay)
    await message.delete()
    await wallet_private(update, context)
    

async def wallet_deposit(update, context):
    user = update.effective_user
    # Check if the command was sent in a private chat
    if update.message.chat.type == 'private':
        command = get_command_by_t_username(user.username)
        print(f"wallet_deposit: command: {command}")
        wallets = get_all_wallets_by_t_username(user.username)
        if is_in_steps(command):
            step = get_step(command)
            arguments = get_arguments(command)
            if step == 1:
                input = update.message.text

                if " " in input:
                    deposited_amount = input.split(" ")[0]
                    symbol_name = input.split(" ")[1]
                else:
                    deposited_amount = input
                    symbol_name = "btt"
                whitelist_token = get_whitelist_token_by_symbol(symbol_name)

                # Check if the amount is a valid number or contains digits and b,
                if is_int(deposited_amount) == False:
                    await send_text(update, TEXT_INVALID_AMOUNT.format(text=deposited_amount) + EXAMPLE_AMOUNT)
                elif whitelist_token is None:
                    await send_text(update, TEXT_INVALID_TOKEN_SYMBOL.format(text=symbol_name) + EXAMPLE_AMOUNT)
                else:
                    wallet_name = arguments[0].replace(WALLET_DEPOSIT_BUTTON, "")
                    my_wallet = next((wallet for wallet in wallets if wallet['name'] == wallet_name), None)
                    fee_needed = int(get_param(PARAMETER_MINIMUM_FEES))

                    # Waiting message
                    sending_path = "assets/gif/send.gif"
                    file = open(sending_path, 'rb')
                    
                    try:
                        msg_wait = await send_animation( update,
                            animation=file,
                            caption="\n\n Broadcasting ... \n\n "
                        )
                    except Exception as e:
                        msg_wait = None
                        print(f"wallet_deposit msg_wait Error: {e}")
                    
                    print(f"whitelist_token['symbol']: {whitelist_token['symbol']}")    
                    if whitelist_token['symbol'] == btt_symbol:
                        balance = get_balance(my_wallet['address'])
                    else:
                        balance = get_erc20_balance(whitelist_token['address'], my_wallet['address'])
                    deposited_amount_int = convert_to_int(deposited_amount)
                    if deposited_amount_int > balance:
                        await send_text(update, MESSAGE_WALLET_INSUFFICIENT_BALANCE.format(balance=human_format(balance), symbol = whitelist_token['symbol']))
                    else:

                        # Deposit the amount to the wallet
                        if whitelist_token['symbol'] == btt_symbol:
                            tx = deposit_tip(deposited_amount_int, my_wallet['address'], my_wallet['pk'])
                        else:
                            tx = deposit_erc20(deposited_amount_int, my_wallet['address'], my_wallet['pk'], whitelist_token['address'])

                        set_command_by_t_username(user.username, WALLET_SELECT_BUTTON + wallet_name)

                        url = get_url_by_tx(tx)
                        reply_markup = ReplyKeyboardMarkup([[get_wallet_full_name(my_wallet)], [USER_MAIN_MENU_BUTTON, WALLET_BUTTON]], resize_keyboard=True)

                        if check_tx_status(tx) == True:
                            await send_html( update,
                                RESPONSE_WALLET_DEPOSIT_SUCCESS.format(amount=deposited_amount_int, symbol = whitelist_token['symbol'], url=url),
                                reply_markup=reply_markup)
                        else:
                            await send_html( update,
                                RESPONSE_WALLET_DEPOSIT_FAILED.format(amount=deposited_amount_int, symbol = whitelist_token['symbol'], url=url),
                                reply_markup=reply_markup)        
                    if msg_wait != None:
                        await msg_wait.delete()        
        
        else:
            command = add_step(update.message.text, "STARTED_DEPOSIT")
            set_command_by_t_username(user.username, command)
            # STEP 0 - Get the wallet name from the user's response
            # Get the name of the wallet from the user's response
            wallet_name = update.message.text.replace(WALLET_DEPOSIT_BUTTON, "")
            
            # We must select the available wallets for the user to check if the wallet name exists
            my_wallet = next((wallet for wallet in wallets if wallet['name'] == wallet_name), None)

            if my_wallet is None or wallets == []:
                await send_text(update, MESSAGE_WALLET_NOT_FOUND.format(wallet=wallet_name))
            else:
                balance = get_balance(my_wallet['address'])
                fee_needed = int(get_param(PARAMETER_MINIMUM_FEES))

                if fee_needed > balance:
                    await send_text(update, MESSAGE_WALLET_INSUFFICIENT_FEE.format(fee=human_format(fee_needed)))
                else:
                    await send_text(update, RESPONSE_WALLET_DEPOSIT)


async def wallet_withdraw(update, context):
    user = update.effective_user
    # Check if the command was sent in a private chat
    if update.message.chat.type == 'private':
        command = get_command_by_t_username(user.username)
        wallets = get_all_wallets_by_t_username(user.username)
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
                    # Your code here to deposit the amount
                    wallet_name = arguments[0].replace(WALLET_WITHDRAW_BUTTON, "")
                    my_wallet = next((wallet for wallet in wallets if wallet['name'] == wallet_name), None)
                    if my_wallet is not None:

                        # Waiting message
                        try:
                            sending_path = "assets/gif/send.gif"
                            file = open(sending_path, 'rb')
                            msg_wait = await send_animation( update,
                                animation=file,
                                caption="\n\n Broadcasting ... \n\n "
                            )
                        except Exception as e:
                            msg_wait = None
                            print(f"wallet_withdraw msg_wait Error: {e}")

                        if whitelist_token['symbol'] == btt_symbol:
                            balance = get_tip_balance(my_wallet['address'])
                        else:
                            balance = get_erc20_balance(whitelist_token['address'], my_wallet['address'])
                        withdraw_amount_int = convert_to_int(withdraw_amount)
                        if withdraw_amount_int > balance:
                            max = balance
                            await send_text(update, MESSAGE_WALLET_INSUFFICIENT_TIP.format(balance=human_format(balance), symbol = whitelist_token['symbol']))
                        else:
                            # Deposit the amount to the wallet
                            if whitelist_token['symbol'] == btt_symbol:
                                tx = withdraw_tip(withdraw_amount_int, my_wallet['address'], my_wallet['pk'])
                            else:
                                tx = withdraw_erc20(withdraw_amount_int, my_wallet['address'], my_wallet['pk'], whitelist_token['address'])

                            set_command_by_t_username(user.username, WALLET_SELECT_BUTTON + wallet_name)

                            # Add inline link to the transaction
                            url = get_url_by_tx(tx)
                            reply_markup = ReplyKeyboardMarkup([[get_wallet_full_name(my_wallet)], [USER_MAIN_MENU_BUTTON, WALLET_BUTTON]], resize_keyboard=True)

                            if check_tx_status(tx) == True:
                                await send_html( update,
                                    RESPONSE_WALLET_WITHDRAW_SUCCESS.format(amount=human_format(withdraw_amount_int), symbol = whitelist_token['symbol'], url=url),
                                    reply_markup=reply_markup)
                            else:
                                await send_html( update,
                                    RESPONSE_WALLET_WITHDRAW_FAILED.format(amount=human_format(withdraw_amount_int), symbol = whitelist_token['symbol'], url=url),
                                    reply_markup=reply_markup)
                        if msg_wait != None: 
                            await msg_wait.delete()
                    else:
                        await send_text(update, f"Wallet not found {wallet_name}. Please select one of the available wallets or create a new one.")
        else:
            command = add_step(update.message.text, "STARTED_WITHDRAW")
            set_command_by_t_username(user.username, command)
            # STEP 0 - Get the wallet name from the user's response
            # Get the name of the wallet from the user's response
            wallet_name = update.message.text.replace(WALLET_WITHDRAW_BUTTON, "")
            
            # We must select the available wallets for the user to check if the wallet name exists
            my_wallet = next((wallet for wallet in wallets if wallet['name'] == wallet_name), None)

            if my_wallet is None or wallets == []:
                await send_text(update, MESSAGE_WALLET_NOT_FOUND.format(wallet=wallet_name))
            else:
                balance = get_balance(my_wallet['address'])
                fee_needed = int(get_param(PARAMETER_MINIMUM_FEES))

                if fee_needed > balance:
                    await send_text(update, MESSAGE_WALLET_INSUFFICIENT_FEE.format(fee=human_format(fee_needed)))
                else:
                    await send_text(update, RESPONSE_WALLET_WITHDRAW)

async def wallet_onchain_transfer(update, context):
    user = update.effective_user
    # Check if the command was sent in a private chat
    if update.message.chat.type == 'private':
        command = get_command_by_t_username(user.username)
        wallets = get_all_wallets_by_t_username(user.username)
        if is_in_steps(command):
            step = get_step(command)
            arguments = get_arguments(command)

            input = update.message.text
            if step == 1:
                if " " in input and len(input.split(" ")) == 3:
                    amount = input.split(" ")[0]
                    symbol_name = input.split(" ")[1]
                    address = input.split(" ")[2]
                else:
                    amount = input
                    symbol_name = "btt"
                    address = ""
                whitelist_token = get_whitelist_token_by_symbol(symbol_name)

                if is_int(amount) == False or len(address) != 42 or address[:2] != "0x":
                    await send_text(update, "Please input a valid address and amount to transfer")
                elif whitelist_token is None:
                    await send_text(update, TEXT_INVALID_TOKEN_SYMBOL.format(text=symbol_name) + EXAMPLE_AMOUNT)
                else:
                    wallet_name = arguments[0].replace(WALLET_ONCHAIN_TRANSFER_BUTTON, "")
                    my_wallet = next((wallet for wallet in wallets if wallet['name'] == wallet_name), None)
                    fee_needed = int(get_param(PARAMETER_MINIMUM_FEES))

                    # Waiting message
                    sending_path = "assets/gif/send.gif"
                    file = open(sending_path, 'rb')
                    try:
                        msg_wait = await send_animation( update,
                            animation=file,
                            caption="\n\n Broadcasting ... \n\n "
                        )
                    except Exception as e:
                        msg_wait = None
                        print(f"wallet_onchain_transfer msg_wait Error: {e}")

                    if whitelist_token['symbol'] == btt_symbol:
                        balance = balance = get_balance(my_wallet['address'])
                    else:
                        balance = get_erc20_balance(whitelist_token['address'], my_wallet['address'])
                    amount_int = convert_to_int(amount)

                    if amount_int > balance:
                        await send_text(update, MESSAGE_WALLET_INSUFFICIENT_BALANCE.format(balance=human_format(balance), symbol = whitelist_token['symbol']))
                    else:
                        # Deposit the amount to the wallet
                        if whitelist_token['symbol'] == btt_symbol:
                            tx = transfer_eth(my_wallet['address'], address, amount_int, my_wallet['pk'])
                        else:
                            tx = transfer_erc20_balance(whitelist_token['address'], my_wallet['address'], address, amount_int, my_wallet['pk'])

                        set_command_by_t_username(user.username, WALLET_SELECT_BUTTON + wallet_name)

                        # Add inline link to the transaction
                        url = get_url_by_tx(tx)
                        reply_markup = ReplyKeyboardMarkup([[get_wallet_full_name(my_wallet)], [USER_MAIN_MENU_BUTTON, WALLET_BUTTON]], resize_keyboard=True)

                        if check_tx_status(tx) == True:
                            await send_html( update,
                                RESPONSE_WALLET_TRANSFER_SUCCESS.format(amount=human_format(amount_int), symbol = whitelist_token['symbol'], url=url),
                                reply_markup=reply_markup)
                        else:
                            await send_html( update,
                                RESPONSE_WALLET_TRANSFER_FAILED.format(amount=human_format(amount_int), symbol = whitelist_token['symbol'], url=url),
                                reply_markup=reply_markup)

                    if msg_wait != None:
                        await msg_wait.delete()
                            
        else:
            command = add_step(update.message.text, "STARTED_TRANSFER")
            set_command_by_t_username(user.username, command)
            # STEP 0 - Get the wallet name from the user's response
            # Get the name of the wallet from the user's response
            wallet_name = update.message.text.replace(WALLET_ONCHAIN_TRANSFER_BUTTON, "")
            
            # We must select the available wallets for the user to check if the wallet name exists
            my_wallet = next((wallet for wallet in wallets if wallet['name'] == wallet_name), None)

            if my_wallet is None or wallets == []:
                await send_text(update, MESSAGE_WALLET_NOT_FOUND.format(wallet=wallet_name))
            else:
                balance = get_balance(my_wallet['address'])
                fee_needed = int(get_param(PARAMETER_MINIMUM_FEES))

                if fee_needed > balance:
                    await send_text(update, MESSAGE_WALLET_INSUFFICIENT_FEE.format(fee=human_format(fee_needed)))
                else:
                    await send_text(update, RESPONSE_WALLET_TRANSFER)

async def wallet_topup(update, context):
    user = update.effective_user
    # Check if the command was sent in a private chat
    if update.message.chat.type == 'private':
        command = get_command_by_t_username(user.username)
        wallets = get_all_wallets_by_t_username(user.username)
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
                    wallet_name = arguments[0].replace(WALLET_TOPUP_BUTTON, "")
                    my_wallet = next((wallet for wallet in wallets if wallet['name'] == wallet_name), None)
                    if whitelist_token['symbol'] == btt_symbol:
                        balance = get_tip_balance(my_wallet['address'])
                    else:
                        balance = get_tip_erc20_balance(whitelist_token['address'], my_wallet['address'])
                    withdraw_amount_int = convert_to_int(withdraw_amount)
                    if withdraw_amount_int > balance:
                        await send_text(update, MESSAGE_WALLET_INSUFFICIENT_TIP.format(balance=human_format(balance), symbol = whitelist_token['symbol']))
                    else:
                        # Waiting message
                        sending_path = "assets/gif/send.gif"
                        file = open(sending_path, 'rb')
                        try:
                            msg_wait = await send_animation( update,
                                animation=file,
                                caption="\n\n Broadcasting ... \n\n "
                            )
                        except Exception as e:
                            msg_wait = None
                            print(f"wallet_topup msg_wait Error: {e}")

                        # Deposit the amount to the wallet
                        set_command_by_t_username(user.username, WALLET_SELECT_BUTTON + wallet_name)
                        if whitelist_token['symbol'] == btt_symbol:
                            tx = top_up_tip(withdraw_amount_int, my_wallet['address'], my_wallet['pk'])
                        else:
                            tx = top_up_erc20(withdraw_amount_int, my_wallet['address'], my_wallet['pk'], whitelist_token['address'])
                        url = get_url_by_tx(tx)
                        reply_markup = ReplyKeyboardMarkup([[get_wallet_full_name(my_wallet)], [USER_MAIN_MENU_BUTTON, WALLET_BUTTON]], resize_keyboard=True)
                        if check_tx_status(tx) == True:
                            top_up_balance_by_t_username(tx, user.username, withdraw_amount_int, whitelist_token['symbol'])
                            await send_html( update,RESPONSE_WALLET_TOPUP_SUCCESS.format(amount=human_format(withdraw_amount_int), symbol = whitelist_token['symbol'], url=url), reply_markup=reply_markup)
                        else:
                            await send_html( update,RESPONSE_WALLET_TOPUP_FAILED.format(amount=human_format(withdraw_amount_int), symbol = whitelist_token['symbol'], url=url), reply_markup=reply_markup)
                        
                        if msg_wait != None:
                            await msg_wait.delete()
        else:
            command = add_step(update.message.text, "STARTED_TRANSFER")
            set_command_by_t_username(user.username, command)
            # STEP 0 - Get the wallet name from the user's response
            # Get the name of the wallet from the user's response
            wallet_name = update.message.text.replace(WALLET_TOPUP_BUTTON, "")

            # We must select the available wallets for the user to check if the wallet name exists
            my_wallet = next((wallet for wallet in wallets if wallet['name'] == wallet_name), None)

            if my_wallet is None or wallets == []:
                await send_text(update, MESSAGE_WALLET_NOT_FOUND.format(wallet=wallet_name))
            else:
                balance = get_balance(my_wallet['address'])
                fee_needed = int(get_param(PARAMETER_MINIMUM_FEES))

                if fee_needed > balance:
                    await send_text(update, MESSAGE_WALLET_INSUFFICIENT_FEE.format(fee=human_format(fee_needed)))
                else:
                    await send_text(update, RESPONSE_WALLET_TOPUP)


async def wallet_delete(update, context):
    user = update.effective_user
    # Check if the command was sent in a private chat
    if update.message.chat.type == 'private':
        command = get_command_by_t_username(user.username)
        
        wallet_name = update.message.text.replace(WALLET_DELETE_BUTTON, "")
        
        # We must select the available wallets for the user to check if the wallet name exists
        delete_wallet_name_by_t_username(user.username, wallet_name)

        reply_markup = ReplyKeyboardMarkup([[USER_MAIN_MENU_BUTTON, WALLET_BUTTON]], resize_keyboard=True)

        await send_text(update, RESPONSE_WALLET_DELETE_SUCCESS.format(wallet=wallet_name), reply_markup=reply_markup)
