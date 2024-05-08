
import random
import os

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from .telegram_send import send_html
from constants.responses_gives import RESPONSE_HOW_TO_DEPOSIT, RESPONSE_HOW_TO_TOP_UP


# Define the start function
async def how_to_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text

    TIP_BOT_URL = os.getenv('TIP_BOT_URL')
    await send_html(update, RESPONSE_HOW_TO_DEPOSIT.format(url=TIP_BOT_URL))

async def how_to_top_up(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text

    TIP_BOT_URL = os.getenv('TIP_BOT_URL')
    await send_html(update, RESPONSE_HOW_TO_TOP_UP.format(url=TIP_BOT_URL))
