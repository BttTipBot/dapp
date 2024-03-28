
import random

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes



# Define the start function
async def good_morning(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"gm {user.mention_html()}!"
    )

# Define the start function
async def good_night(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    good_night_messages = [
        "Sweet dreams!",
        "Sleep tight!",
        "Good night!"
    ]
    
    # List of good night GIF URLs (replace with your own URLs)
    gif_urls = [
        "assets/gif/gm.gif",
        # "assets/gif/gm2.gif",
        # "assets/gif/gm3.gif",
    ]
    
    # Randomly select a good night message
    selected_message = random.choice(good_night_messages)

    # Randomly select a GIF URL
    selected_gif_path = random.choice(gif_urls)

    file = open(selected_gif_path, 'rb')

    user = update.effective_user
    # await update.message.reply_photo(
    #     photo=file,
    #     caption="gn!",
    #     reply_markup=ForceReply(selective=True),
    # )

    await update.message.reply_animation(
        animation=file,
        caption=f"{selected_message} @{user.username}",
        # reply_markup=ForceReply(selective=True),
    
    )