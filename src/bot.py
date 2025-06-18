import logging
import asyncio
from typing import List, Tuple, Any

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
)
from telegram.error import NetworkError, TimedOut, BadRequest
from src.config import bot_token
from src.commands import (
    start_command,
    movie_command,
    cartoon_command,
    serial_command,
)
from src.content_fetcher import get_random_content

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


async def error_handler(_: Update, context: CallbackContext) -> None:
    logger = logging.getLogger(__name__)
    error = context.error
    if isinstance(error, (NetworkError, TimedOut)):
        logger.warning(f"Network error occurred: {error}")
        # Just log the error - the main loop will handle restarting if needed
        logger.info("Network error will be handled by main loop")
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

    # Get the current message with the buttons
    message = update.callback_query.message

    # Create a new keyboard with disabled buttons
    disabled_keyboard: List[List[InlineKeyboardButton]] = []

    # Copy the first row (link button) if it exists
    if (
        message.reply_markup
        and message.reply_markup.inline_keyboard
        and len(message.reply_markup.inline_keyboard) > 0
    ):
        first_row = message.reply_markup.inline_keyboard[0]
        disabled_keyboard.append(first_row)

    # Create disabled content buttons row
    disabled_content_row: List[InlineKeyboardButton] = []
    button_order: List[Tuple[str, str]] = [
        ("filmy", "Фільм"),
        ("seriesss", "Серіал"),
        ("cartoon", "Мульт"),
    ]

    for type_code, type_name in button_order:
        # Add "⏳" only to the button that was clicked
        if type_code == content_type:
            button_text_disabled = f"{type_name} ⏳"  # Add loading indicator to clicked button
        else:
            button_text_disabled = type_name  # Keep other buttons normal

        disabled_content_row.append(
            InlineKeyboardButton(
                text=button_text_disabled,
                callback_data="disabled",  # Disabled callback
            )
        )
    disabled_keyboard.append(disabled_content_row)

    # Update the message with disabled buttons
    await message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(disabled_keyboard))

    # Send a message that will be deleted later
    waitMessage = await message.reply_text(f"Шукаю {button_text.lower()} 🧐")

    # Fetch content
    random_content: List[Any] = get_random_content(content_type)
    caption_text: str = (
        f"<b>{random_content[0]} ({random_content[1]})</b>\n\n"
        f"<b>IMDb:</b> {random_content[5]}\n<b>Жанр:</b> {random_content[2]}\n<b>Актори:</b> {random_content[7]}\n\n"
        f"{random_content[4].strip() if len(random_content[4].strip()) > 5 else ''}"
    )

    # Create new keyboard with active buttons for the new message
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

    # Send new message with content and active buttons
    await message.reply_photo(
        photo=random_content[6],
        caption=caption_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(new_keyboard),
    )

    # Delete the wait message
    await context.bot.delete_message(chat_id=message.chat.id, message_id=waitMessage.message_id)

    await asyncio.sleep(0.5)


async def disabled_button_handler(update: Update, _: CallbackContext) -> None:
    # This handler is called when a user clicks on a disabled button
    # Just answer the callback query without any message
    await update.callback_query.answer()


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
    # Removed broadcast and db commands as per request
    application.add_handler(CallbackQueryHandler(another_handler, pattern=r"^another:"))
    application.add_handler(CallbackQueryHandler(disabled_button_handler, pattern=r"^disabled"))
    application.add_error_handler(error_handler)

    async def run_bot():
        logger = logging.getLogger(__name__)
        while True:
            try:
                # Only initialize if not already initialized
                if not application.running:
                    await application.initialize()
                    await application.start()
                    await application.updater.start_polling()
                    logger.info("Bot started successfully")

                # Add health check task
                asyncio.create_task(health_check())

                # Keep the bot running
                while application.running:
                    await asyncio.sleep(1)

            except Exception as e:
                logger.error(f"Bot crashed: {e}")
                # Try to properly shut down the application if it's running
                if application.running:
                    try:
                        await application.stop()
                        logger.info("Application stopped after error")
                    except Exception as shutdown_error:
                        logger.error(f"Error during shutdown: {shutdown_error}")

                # Wait before attempting to restart
                await asyncio.sleep(15)

    asyncio.run(run_bot())


if __name__ == "__main__":
    main()
