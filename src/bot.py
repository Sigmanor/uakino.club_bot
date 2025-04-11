import logging
import asyncio
import time
from typing import List, Tuple, Any

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
)
from telegram.error import NetworkError, TimedOut, BadRequest
from .config import bot_token
from .commands import (
    start_command,
    movie_command,
    cartoon_command,
    serial_command,
    broadcast_command,
    db_command,
)
from .content_fetcher import get_random_content

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


async def post_init(application: Application) -> None:
    bot = application.bot
    await bot.set_my_commands(
        [
            ("start", "Інформація про бота"),
            ("movie", "Отримати випадковий фільм"),
            ("serial", "Отримати випадковий серіал"),
            ("cartoon", "Отримати випадковий мультфільм"),
        ]
    )


async def error_handler(update: Update, context: CallbackContext) -> None:
    logger = logging.getLogger(__name__)
    error = context.error
    if isinstance(error, (NetworkError, TimedOut)):
        logger.warning(f"Network error occurred: {error}")
        await asyncio.sleep(15)
        try:
            if context.application.running:
                await context.application.stop()
            await context.application.start()
            logger.info("Bot successfully restarted after network error")
        except Exception as e:
            logger.error(f"Failed to restart bot: {e}")
            import sys
            sys.exit(1)
    elif isinstance(error, BadRequest):
        logger.error(f"Bad Request: {error}")
    else:
        logger.error("Exception while handling an update:", exc_info=error)


async def another_handler(update: Update, context: CallbackContext) -> None:
    logger = logging.getLogger(__name__)
    logger.info(
        f"User {update.effective_user.id} clicked button. Callback data: {update.callback_query.data}"
    )
    data = update.callback_query.data
    try:
        _, content_type, button_text = data.split(":", 2)
    except ValueError:
        return

    await update.callback_query.answer(text=f"Шукаю {button_text.lower()}...", show_alert=False)
    message = update.callback_query.message

    random_content: List[Any] = get_random_content(content_type)
    caption_text: str = (
        f"<b>{random_content[0]} ({random_content[1]})</b>\n\n"
        f"<b>IMDb:</b> {random_content[5]}\n<b>Жанр:</b> {random_content[2]}\n<b>Актори:</b> {random_content[7]}\n\n"
        f"{random_content[4].strip() if len(random_content[4].strip()) > 5 else ''}"
    )

    new_keyboard: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text=f"Посилання на {button_text.lower()}",
                url=random_content[3],
                callback_data=f"link:{content_type}:{button_text}",
            )
        ]
    ]

    content_row: List[InlineKeyboardButton] = []
    button_order: List[Tuple[str, str]] = [
        ("filmy", "Фільм"),
        ("seriesss", "Серіал"),
        ("cartoon", "Мульт"),
    ]

    for type_code, type_name in button_order:
        content_row.append(
            InlineKeyboardButton(
                text=type_name,
                callback_data=f"another:{type_code}:{type_name}",
            )
        )
    new_keyboard.append(content_row)

    logger.info(
        f"User {update.effective_user.id} received link to {button_text}: {random_content[3]}"
    )

    await message.reply_photo(
        photo=random_content[6],
        caption=caption_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(new_keyboard),
    )
    await asyncio.sleep(0.5)


async def health_check() -> None:
    logger = logging.getLogger(__name__)
    while True:
        try:
            await asyncio.sleep(300)
            logger.info("Bot health check: OK")
        except Exception as e:
            logger.error(f"Health check failed: {e}")


def main() -> None:
    application = (
        Application.builder()
        .token(bot_token)
        .post_init(post_init)
        .read_timeout(60)
        .write_timeout(60)
        .connect_timeout(60)
        .pool_timeout(60)
        .get_updates_read_timeout(120)
        .build()
    )

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("movie", movie_command))
    application.add_handler(CommandHandler("serial", serial_command))
    application.add_handler(CommandHandler("cartoon", cartoon_command))
    application.add_handler(CommandHandler("add", broadcast_command))
    application.add_handler(CommandHandler("db", db_command))
    application.add_handler(CallbackQueryHandler(another_handler, pattern=r"^another:"))
    application.add_error_handler(error_handler)

    async def run_bot():
        while True:
            try:
                await application.start()
                await application.run_until_stopped()
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.error(f"Bot crashed: {e}")
                await asyncio.sleep(15)

    asyncio.run(run_bot())

if __name__ == "__main__":
    main()