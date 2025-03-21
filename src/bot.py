import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram.error import NetworkError, Forbidden, TimedOut
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


async def error_handler(update: Update, context) -> None:
    logger = logging.getLogger(__name__)
    logger.error("Exception while handling an update:", exc_info=context.error)

    if isinstance(context.error, NetworkError):
        logger.info("Network error occurred. Continuing operation...")
        return


async def another_handler(update: Update, context) -> None:
    logger = logging.getLogger(__name__)
    logger.info(
        f"User {update.effective_user.id} clicked button. Callback data: {update.callback_query.data}"
    )
    data = update.callback_query.data
    try:
        _, content_type, button_text = data.split(":", 2)
    except ValueError:
        return

    # Show loading state
    await update.callback_query.answer(text=f"Шукаю {button_text.lower()}...", show_alert=False)
    message = update.callback_query.message

    random_content = get_random_content(content_type)
    caption_text = (
        f"<b>{random_content[0]} ({random_content[1]})</b>\n\n"
        f"<b>IMDb:</b> {random_content[5]}\n<b>Жанр:</b> {random_content[2]}\n<b>Актори:</b> {random_content[7]}\n\n"
        f"{random_content[4].strip() if len(random_content[4].strip()) > 5 else ''}"
    )
    
    # Create base keyboard with link button
    new_keyboard = [
        [
            InlineKeyboardButton(
                text=f"Посилання на {button_text.lower()}",
                url=random_content[3],
                callback_data=f"link:{content_type}:{button_text}",
            )
        ]
    ]

    # Create fixed-order content type buttons
    content_row = []
    button_order = [
        ("filmy", "Фільм"),
        ("seriesss", "Серіал"),
        ("cartoon", "Мульт")
    ]

    for type_code, type_name in button_order:
        if type_code == content_type:
            # Current content type button
            content_row.append(
                InlineKeyboardButton(
                    text=type_name,
                    callback_data=f"another:{type_code}:{type_name}",
                )
            )
        else:
            # Other content type buttons
            content_row.append(
                InlineKeyboardButton(
                    text=type_name,
                    callback_data=f"another:{type_code}:{type_name}"
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
        .read_timeout(15)
        .write_timeout(15)
        .connect_timeout(15)
        .get_updates_read_timeout(42)
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

    application.run_polling()


if __name__ == "__main__":
    main()
