import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from content_fetcher import get_random_content
from config import uakino_url, app_version

logger = logging.getLogger(__name__)


async def start_command(update: Update, context) -> None:
    logger.info(update)
    await update.message.reply_text(
        f"Привіт 🏴‍☠️\n\nЯ покажу тобі випадковий фільм/серіал/мультфільм з сайту <a href='https://{
            uakino_url}'>uakino</a>\n\n"
        "<b>Список команд:</b>\n/movie <i>фільм</i>\n/serial <i>серіал</i>\n/cartoon <i>мультфільм</i>\n\n"
        f"<b>Версія бота:</b> {app_version}\n\n"
        f"<blockquote>Бот був створений задля розваги і немає ніякого зв'язку з сайтом https://{
            uakino_url} як і <a href='https://t.me/sigmanor'>автор</a> бота</blockquote>",
        disable_web_page_preview=True,
        parse_mode=ParseMode.HTML,
    )


async def build_tg_message(update: Update, context, content_type: str, button_text: str) -> None:
    waitMessage = await update.message.reply_text(f"Шукаю {button_text} 🧐")
    random_content = get_random_content(content_type)

    caption_text = (
        f"<b>{random_content[0]} ({random_content[1]})</b>\n\n"
        f"<b>IMDb:</b> {random_content[5]}\n<b>Жанр:</b> {
            random_content[2]}\n<b>Актори:</b> {random_content[7]}\n\n"
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
        chat_id=update.message.chat.id, message_id=waitMessage.message_id
    )


async def movie_command(update: Update, context) -> None:
    logger.info(update)
    await build_tg_message(update, context, "filmy", "фільм")


async def cartoon_command(update: Update, context) -> None:
    logger.info(update)
    await build_tg_message(update, context, "cartoon", "мультфільм")


async def serial_command(update: Update, context) -> None:
    logger.info(update)
    await build_tg_message(update, context, "seriesss", "серіал")
