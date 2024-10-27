from telegram import Update, Animation, ReplyKeyboardMarkup, PhotoSize
from telegram.ext import ContextTypes

from telegram.error import RetryAfter, TimedOut


async def send_animation(update: Update, animation: Animation, caption: str = "", parse_mode: str = "HTML", reply_markup: ReplyKeyboardMarkup = None):
    try:
        return await update.message.reply_animation(
            animation=animation,
            caption=caption,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )
    except Exception as e:
        if isinstance(e, RetryAfter):
            send_text(update, caption, parse_mode, reply_markup)
        elif isinstance(e, TimedOut):
            print("send_animation", e)
        else:
            print("send_animation", e)
            return await update.message.reply_text(f"An error occurred: {e} for msg={caption}")

    
async def send_photo(update: Update, photo: PhotoSize, caption: str = "", parse_mode: str = "HTML", reply_markup: ReplyKeyboardMarkup = None):
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


async def send_text(update: Update, text: str = "", parse_mode: str = "HTML", reply_markup: ReplyKeyboardMarkup = None):
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
    


async def send_animation_noreply(context: ContextTypes.DEFAULT_TYPE, update: Update, animation: Animation, caption: str = "", parse_mode: str = "HTML", reply_markup: ReplyKeyboardMarkup = None):
    try:
        return await context.bot.send_animation(
            chat_id=update.effective_chat.id,
            animation=animation,
            caption=caption,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            message_thread_id=update.message.message_thread_id if update.effective_chat.is_forum else None
        )
    except Exception as e:
        if isinstance(e, RetryAfter):
            send_text_noreply(context, update, caption, parse_mode, reply_markup)
        elif isinstance(e, TimedOut):
            print("send_animation", e)
        else:
            print("send_animation", e)
            return await context.bot.send_message(update.effective_chat.id, f"An error occurred: {e} for msg={caption}")

    
async def send_photo_noreply(context: ContextTypes.DEFAULT_TYPE, update: Update, photo: PhotoSize, caption: str = "", parse_mode: str = "HTML", reply_markup: ReplyKeyboardMarkup = None):
    try:
        return await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            message_thread_id=update.message.message_thread_id if update.effective_chat.is_forum else None
        )
    except Exception as e:
        if isinstance(e, RetryAfter):
            return await  context.bot.send_message(update.effective_chat.id, f"I'm being rate limited. Please try again later. 😢 \n\n {e}")
        elif isinstance(e, TimedOut):
            return await  context.bot.send_message(update.effective_chat.id, f"We process your request but got timed out when sending the response. 😢 \n\n {e}")
        else:
            print("send_photo", e)
            return await  context.bot.send_message(update.effective_chat.id, f"An error occurred: {e}")


async def send_text_noreply(context: ContextTypes.DEFAULT_TYPE, update: Update, text: str = "", parse_mode: str = "HTML", reply_markup: ReplyKeyboardMarkup = None):
    return await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=parse_mode,
        reply_markup=reply_markup,
        message_thread_id=update.message.message_thread_id if update.effective_chat.is_forum else None
    )

async def send_html_noreply(context: ContextTypes.DEFAULT_TYPE, update: Update, text: str = "", reply_markup: ReplyKeyboardMarkup = None):
    return await send_text_noreply(
        context,
        update,
        text=text,
        parse_mode="HTML",
        reply_markup=reply_markup,
        message_thread_id=update.message.message_thread_id if update.effective_chat.is_forum else None
    )