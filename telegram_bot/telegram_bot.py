# Import the required libraries
import os
import logging
from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, CallbackContext, ContextTypes, MessageHandler, filters
import asyncio

# Local imports
from charts.my_charts import create_chart
from constants.globals import (
    WALLET_BUTTON,
    WITHDRAW_BUTTON,
    USER_HELP_BUTTON,
    USER_BALANCE_BUTTON,
    USER_HISTORY_BUTTON,
    WALLET_NEW_BUTTON,
    USER_MAIN_MENU_BUTTON,
    WALLET_IMPORT_BUTTON,
    WALLET_GENERATE_BUTTON,
    WALLET_DEPOSIT_BUTTON,
    WALLET_EXPORT_BUTTON,
    WALLET_TOPUP_BUTTON,
    WALLET_WITHDRAW_BUTTON,
    WALLET_ONCHAIN_TRANSFER_BUTTON,
    WALLET_DELETE_BUTTON,
    WITHDRAW_BUTTON_ON_ADDRESS,
    WITHDRAW_BUTTON_ON_ACCOUNT,

)

# Import the required responses
from .responses.start import start
from .responses.wallet import wallet_private, wallet_delete, wallet_deposit, wallet_topup, wallet_withdraw, wallet_onchain_transfer, wallet_export
from .responses.wallet_new import wallet_new, wallet_import_address, wallet_generate_address
from .responses.tip import tip, tipOnChain
from .responses.points import points
from .responses.rain import rain
from .responses.airdrop import airdrop
from .responses.hi import good_morning, good_night, hello
from .responses.balance import balance, balance_telegram
from .responses.history import history
from .responses.withdraw import withdraw_user, withdraw_user_in_address, withdraw_user_in_wallet
from .responses.help import help_command
from .responses.fallback import fallback_handler
from .responses.howto import how_to_deposit, how_to_top_up
from .responses.burn import BurnOnChain, burn, trigger_burn
from .responses.dice import dice
from .responses.broadcast import broadcast
from .responses.admin import admin_PUT_fee, admin_set_TOP_UP_address

# Load the environment variables
load_dotenv()

# Set the logging level
logging.basicConfig(level=logging.INFO)

# Set the bot token
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Define the main function
def run_bot_telegram() -> None:
    # Create the event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Create the Updater and pass it the bot's token
    print(f"Bot started with token: {TELEGRAM_TOKEN}")
    application = Application.builder().token(f"{TELEGRAM_TOKEN}").build()

    # Register the handlers commands
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('wallets', wallet_private))
    application.add_handler(CommandHandler('hi', hello))
    application.add_handler(CommandHandler('gm', good_morning))
    application.add_handler(CommandHandler('gn', good_night))
    application.add_handler(CommandHandler('balance', balance_telegram))
    application.add_handler(CommandHandler('burnOnChain', BurnOnChain))
    application.add_handler(CommandHandler('burn', burn))
    application.add_handler(CommandHandler('triggerBurn', trigger_burn))
    application.add_handler(CommandHandler('balanceAll', balance))
    application.add_handler(CommandHandler('history', history))
    application.add_handler(CommandHandler('howtodeposit', how_to_deposit))
    application.add_handler(CommandHandler('howtotopup', how_to_top_up))
    application.add_handler(CommandHandler('adminPUTfee', admin_PUT_fee))
    application.add_handler(CommandHandler('adminSETtopupaddress', admin_set_TOP_UP_address))

    # Register the tip function
    application.add_handler(CommandHandler('tip', tip))
    application.add_handler(CommandHandler('tipOnChain', tipOnChain))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('commands', help_command))
    application.add_handler(CommandHandler('list', help_command))
    application.add_handler(CommandHandler('lst', help_command))
    application.add_handler(CommandHandler('points', points))
    application.add_handler(CommandHandler('rain', rain))
    application.add_handler(CommandHandler('airdrop', airdrop))
    application.add_handler(CommandHandler('dice', dice))
    application.add_handler(CommandHandler('broadcastTippers', broadcast))

    # Register all the buttons handlers
    application.add_handler(MessageHandler(filters.Regex(f'^{USER_MAIN_MENU_BUTTON}$'), start))
    application.add_handler(MessageHandler(filters.Regex(f'^{USER_HELP_BUTTON}$'), help_command))
    application.add_handler(MessageHandler(filters.Regex(f'^{USER_BALANCE_BUTTON}$'), balance))
    application.add_handler(MessageHandler(filters.Regex(f'^{USER_HISTORY_BUTTON}$'), history))
    application.add_handler(MessageHandler(filters.Regex(f'{WITHDRAW_BUTTON}'), withdraw_user))

    #Wallet
    application.add_handler(MessageHandler(filters.Regex(f'^{WALLET_BUTTON}$'), wallet_private))

    application.add_handler(MessageHandler(filters.Regex(f'{WALLET_EXPORT_BUTTON}'), wallet_export))
    application.add_handler(MessageHandler(filters.Regex(f'{WALLET_DEPOSIT_BUTTON}'), wallet_deposit))
    application.add_handler(MessageHandler(filters.Regex(f'{WALLET_TOPUP_BUTTON}'), wallet_topup))
    application.add_handler(MessageHandler(filters.Regex(f'{WALLET_WITHDRAW_BUTTON}'), wallet_withdraw))
    application.add_handler(MessageHandler(filters.Regex(f'{WALLET_ONCHAIN_TRANSFER_BUTTON}'), wallet_onchain_transfer))
    application.add_handler(MessageHandler(filters.Regex(f'{WALLET_DELETE_BUTTON}'), wallet_delete))



    application.add_handler(MessageHandler(filters.Regex(f'^{WALLET_NEW_BUTTON}$'), wallet_new))
    application.add_handler(MessageHandler(filters.Regex(f'^{WALLET_GENERATE_BUTTON}$'), wallet_generate_address))
    application.add_handler(MessageHandler(filters.Regex(f'^{WALLET_IMPORT_BUTTON}$'), wallet_import_address))

    application.add_handler(MessageHandler(filters.Regex(f'^{WITHDRAW_BUTTON_ON_ADDRESS}$'), withdraw_user_in_address))
    application.add_handler(MessageHandler(filters.Regex(f'{WITHDRAW_BUTTON_ON_ACCOUNT}'), withdraw_user_in_wallet))


    # application.add_handler(MessageHandler(filters.Regex(f'^{WALLET_IMPORT_BUTTON}$'), wallet_import_address))

    # Add a fallback handler to handle unmatched commands which might be previous commands inputs
    application.add_handler(MessageHandler(filters.Regex(f'.*'), fallback_handler))

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)
