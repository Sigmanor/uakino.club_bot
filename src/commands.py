import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from src.content_fetcher import get_random_content
from src.config import uakino_url, app_version
logger = logging.getLogger(__name__)


def register_user(update: Update) -> None:
    # Database functionality removed
    pass


async def start_command(update: Update, context) -> None:
    logger.info(update)
    register_user(update)
    await update.message.reply_text(
        f"Привіт 🏴‍☠️\n\nЯ покажу тобі випадковий фільм/серіал/мультфільм з сайту <a href='https://{uakino_url}'>uakino</a>\n\n"
        "<b>Список команд:</b>\n/movie <i>фільм</i>\n/serial <i>серіал</i>\n/cartoon <i>мультфільм</i>\n\n"
        f"<b>Версія:</b> {app_version}\n\n"
        f"<blockquote>Бот був створений задля розваги і немає ніякого зв'язку з сайтом https://{uakino_url} як і <a href='https://sigmanor.chkl.ink/'>автор</a> бота\n\nВихідний код бота можна знайти на <a href='https://github.com/Sigmanor/uakino.club_bot'>GitHub</a></blockquote>",
        disable_web_page_preview=True,
        parse_mode=ParseMode.HTML,
    )


async def build_tg_message(update: Update, context, content_type: str, button_text: str) -> None:
    logger = logging.getLogger(__name__)
    register_user(update)
    waitMessage = await update.message.reply_text(f"Шукаю {button_text} 🧐")
    random_content = get_random_content(content_type)

    caption_text = (
        f"<b>{random_content[0]} ({random_content[1]})</b>\n\n"
        f"<b>IMDb:</b> {random_content[5]}\n<b>Жанр:</b> {random_content[2]}\n<b>Актори:</b> {random_content[7]}\n\n"
        f"{random_content[4] if len(random_content[4].strip()) > 5 else ''}"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                text=f"Посилання на {button_text.lower()}",
                url=random_content[3],
                callback_data=f"link:{content_type}:{button_text}",
            )
        ]
    ]

    content_row = []
    button_order = [
        ("filmy", "Фільм"),
        ("seriesss", "Серіал"),
        ("cartoon", "Мульт")
    ]

    for type_code, type_name in button_order:
        if type_code == content_type:
            content_row.append(
                InlineKeyboardButton(
                    text=type_name,
                    callback_data=f"another:{type_code}:{type_name}",
                )
            )
        else:
            content_row.append(
                InlineKeyboardButton(
                    text=type_name,
                    callback_data=f"another:{type_code}:{type_name}"
                )
            )
    
    keyboard.append(content_row)

    logger.info(
        f"User {update.effective_user.id} received link to {button_text}: {random_content[3]}"
    )

    await update.message.reply_photo(
        photo=random_content[6],
        caption=caption_text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

    await context.bot.delete_message(
        chat_id=update.message.chat.id, message_id=waitMessage.message_id
    )


async def movie_command(update: Update, context) -> None:
    logger.info(update)
    await build_tg_message(update, context, "filmy", "Фільм")


async def cartoon_command(update: Update, context) -> None:
    logger.info(update)
    await build_tg_message(update, context, "cartoon", "Мульт")


async def serial_command(update: Update, context) -> None:
    logger.info(update)
    await build_tg_message(update, context, "seriesss", "Серіал")


async def broadcast_command(update: Update, context) -> None:
    # Command removed as per request
    await update.message.reply_text("This command has been removed.")


async def db_command(update: Update, context) -> None:
    # Command removed as per request
    await update.message.reply_text("This command has been removed.")
