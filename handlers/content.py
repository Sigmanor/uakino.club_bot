"""
Handlers for fetching and displaying content (movies, cartoons, serials).
"""
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from services.database import Database
from services.content_fetcher import get_random_content
from handlers.base import _register_user

logger = logging.getLogger(__name__)

db = Database()


async def _build_tg_message(update: Update, context, content_type: str, button_text: str) -> None:
    """
    Build and send a message with random content information.

    Args:
        update: Telegram update object
        context: CallbackContext object
        content_type: Type of content to fetch (filmy, cartoon, seriesss)
        button_text: Text to display on the link button
    """
    _register_user(update)
    wait_message = await update.message.reply_text(f"Шукаю {button_text} 🧐")

    random_content = get_random_content(content_type)

    caption_text = (
        f"<b>{random_content[0]} ({random_content[1]})</b>\n\n"
        f"<b>IMDb:</b> {random_content[5]}\n"
        f"<b>Жанр:</b> {random_content[2]}\n"
        f"<b>Актори:</b> {random_content[7]}\n\n"
        f"{random_content[4] if len(random_content[4].strip()) > 5 else ''}"
    )

    await update.message.reply_photo(
        photo=random_content[6],
        caption=caption_text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=f"Посилання на {button_text}", url=random_content[3])]]
        ),
    )

    await context.bot.delete_message(
        chat_id=update.message.chat.id,
        message_id=wait_message.message_id
    )


async def movie_command(update: Update, context) -> None:
    """
    Handle the /movie command. Sends information about a random movie.

    Args:
        update: Telegram update object
        context: CallbackContext object
    """
    logger.info(update)
    await _build_tg_message(update, context, "filmy", "фільм")


async def cartoon_command(update: Update, context) -> None:
    """
    Handle the /cartoon command. Sends information about a random cartoon.

    Args:
        update: Telegram update object
        context: CallbackContext object
    """
    logger.info(update)
    await _build_tg_message(update, context, "cartoon", "мультфільм")


async def serial_command(update: Update, context) -> None:
    """
    Handle the /serial command. Sends information about a random TV series.

    Args:
        update: Telegram update object
        context: CallbackContext object
    """
    logger.info(update)
    await _build_tg_message(update, context, "seriesss", "серіал")
