from telegram import Update, Animation, ReplyKeyboardMarkup, PhotoSize

from telegram.error import RetryAfter, TimedOut


async def send_animation(update: Update, animation: Animation, caption: str = "", parse_mode: str = "Markdown", reply_markup: ReplyKeyboardMarkup = None):
    try:
        return await update.message.reply_animation(
            animation=animation,
            caption=caption,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )
    except Exception as e:
        if isinstance(e, RetryAfter):
            return await update.message.reply_text(f"I'm being rate limited. Please try again later. 😢 \n\n {e}")
        elif isinstance(e, TimedOut):
            return await update.message.reply_text(f"We process your request but got timed out when sending the response. 😢 \n\n {e}")
        else:
            print("send_animation", e)
            return await update.message.reply_text(f"An error occurred: {e}")

    
async def send_photo(update: Update, photo: PhotoSize, caption: str = "", parse_mode: str = "Markdown", reply_markup: ReplyKeyboardMarkup = None):
    try:
        return await update.message.reply_photo(
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )
    except Exception as e:
        if isinstance(e, RetryAfter):
            return await update.message.reply_text(f"I'm being rate limited. Please try again later. 😢 \n\n {e}")
        elif isinstance(e, TimedOut):
            return await update.message.reply_text(f"We process your request but got timed out when sending the response. 😢 \n\n {e}")
        else:
            print("send_photo", e)
            return await update.message.reply_text(f"An error occurred: {e}")


async def send_text(update: Update, text: str = "", parse_mode: str = "Markdown", reply_markup: ReplyKeyboardMarkup = None):
    return await update.message.reply_text(
        text=text,
        parse_mode=parse_mode,
        reply_markup=reply_markup
    )

async def send_html(update: Update, text: str = "", reply_markup: ReplyKeyboardMarkup = None):
    return await send_text(
        update,
        text=text,
        parse_mode="HTML",
        reply_markup=reply_markup
    )