
import random
import os
import asyncio

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from .telegram_send import send_animation, send_text
from utils.convert import is_int, convert_to_int, human_format
from db.balances import get_balance_by_t_username
from utils.tokens import get_whitelist_token_by_symbol
from db.transactions import record_dice_by_t_username, record_dice_winner_by_t_username
from constants.globals import MAIN_SYMBOL


# Define the start function
async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text
    user = update.effective_user
    dice_price_username = MAIN_SYMBOL.lower() + "_tip_bot"

    if len(context.args) == 3:
        # List of good night GIF URLs (replace with your own URLs)
        dice_options = [1, 2 ,3, 4, 5, 6]
        gif_urls = [
            "assets/tgs/AnimatedSticker1.tgs",
            "assets/tgs/AnimatedSticker2.tgs",
            "assets/tgs/AnimatedSticker3.tgs",
            "assets/tgs/AnimatedSticker4.tgs",
            "assets/tgs/AnimatedSticker5.tgs",
            "assets/tgs/AnimatedSticker6.tgs",
        ]
        
        # Randomly select a random number
        selected_number = int(context.args[0])
        amount = context.args[1]
        symbol_name = context.args[2]
        
        if is_int(amount) == False:
            await send_text(update, 'Invalid amount')
            return
        
        whitelist_token = get_whitelist_token_by_symbol(symbol_name)
        if whitelist_token == None:
            await send_text(update, 'Invalid symbol')
            return
        
        amount_int = convert_to_int(amount)
        balance_sender = get_balance_by_t_username(user.username, whitelist_token['symbol'])
        
        # Check if the user has enough balance
        if balance_sender < amount_int:
            TIP_BOT_URL = os.getenv('TIP_BOT_URL')
            await send_text(update, f"Not enough balance. 🤕 \n\n Balance: {human_format(balance_sender)} {whitelist_token['symbol']}")
            return
        prize_pool = get_balance_by_t_username(dice_price_username, whitelist_token['symbol'])
        winner_price = amount_int * 2
        
        if winner_price > prize_pool:
            await send_text(update, 'Not enough funds 💔 in prize pool \n\n Max bet 🤑🎰' + human_format(prize_pool/2) + ' ' + whitelist_token['symbol'] + '\n\n 💰 Prize pool: ' + human_format(prize_pool) + ' ' + whitelist_token['symbol'])
            return
        
        record_dice_by_t_username(user.username, dice_price_username, amount_int, whitelist_token['symbol'])

        dice_random_number = random.choice(dice_options)
        selected_gif_path = gif_urls[dice_random_number - 1]
        
        selected_message = f"🎰 You bet {selected_number}"
        selected_message += f"\n\n 🎲 The dice rolled a {dice_random_number} 🎲"
        
        if selected_number == dice_random_number:
            record_dice_winner_by_t_username(user.username, dice_price_username, winner_price, whitelist_token['symbol'])
            selected_message += "\n\n 🎉 Congratulations! You guessed the number correctly! 🎉"
            selected_message += "\n\n You won " + human_format(winner_price) + " " + whitelist_token['symbol'] + "! 🎉"
        else:
            selected_message += "\n\n 😢 Better luck next time! \n\n All amounts will be added in burn liquidity🚰🔥 "

        file = open(selected_gif_path, 'rb')
        user = update.effective_user

        msg_tgs =  await send_animation(
            update, 
            animation=file,
            parse_mode="HTML"
        )
        
        msg_text = await send_text(update, selected_message)
        
        msg_user = update.message
        asyncio.create_task(delete_dice_msg(update, context, msg_user, msg_tgs, msg_text))
    else:
        await send_text(update, 'Usage: /dice number amount symbol')
        return


async def delete_dice_msg(update: Update, context: ContextTypes.DEFAULT_TYPE, msg_user, msg_tgs, msg_text):
    delay = 60
    await asyncio.sleep(delay)
    
    if msg_user:
        await msg_user.delete()
    
    if msg_tgs:
        await msg_tgs.delete()
    
    if msg_text:
        await msg_text.delete()
    