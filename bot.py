import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram.error import NetworkError
from config import bot_token
from commands import (
    start_command,
    movie_command,
    cartoon_command,
    serial_command,
    broadcast_command,
    db_command,
)
from content_fetcher import get_random_content  # використовується в новому handler

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
    logger.info(f"User {update.effective_user.id} clicked 'Ще один' button. Callback data: {update.callback_query.data}")
    
    # Обробка callback з даними у форматі "another:<content_type>:<button_text>"
    data = update.callback_query.data  # наприклад: "another:filmy:фільм"
    try:
        _, content_type, button_text = data.split(":", 2)
    except ValueError:
        return

    # Відповідаємо, щоб зник спіннер на кнопці
    await update.callback_query.answer()

    message = update.callback_query.message

    # Оновлюємо inline-клавіатуру: змінюємо текст кнопки "Ще один..."
    keyboard = message.reply_markup.inline_keyboard if message.reply_markup else []
    new_keyboard = []
    for row in keyboard:
        new_row = []
        for btn in row:
            if btn.callback_data == data:
                new_text = btn.text + " ⌛"
                new_row.append(InlineKeyboardButton(text=new_text, callback_data="disabled"))
            else:
                new_row.append(btn)
        new_keyboard.append(new_row)
    await message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(new_keyboard))

    # Генеруємо новий контент
    random_content = get_random_content(content_type)
    caption_text = (
        f"<b>{random_content[0]} ({random_content[1]})</b>\n\n"
        f"<b>IMDb:</b> {random_content[5]}\n<b>Жанр:</b> {random_content[2]}\n<b>Актори:</b> {random_content[7]}\n\n"
        f"{random_content[4].strip() if len(random_content[4].strip()) > 5 else ''}"
    )

    new_keyboard = [
        [InlineKeyboardButton(
            text=f"Посилання на {button_text}", 
            url=random_content[3],
            callback_data=f"link:{content_type}:{button_text}"  # This won't trigger for URL buttons
        )],
        [InlineKeyboardButton(text=f"Ще один {button_text}", callback_data=f"another:{content_type}:{button_text}")]
    ]
    
    logger.info(f"User {update.effective_user.id} received link to {button_text}: {random_content[3]}")

    await message.reply_photo(
        photo=random_content[6],
        caption=caption_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(new_keyboard),
    )
def main() -> None:
    application = (
        Application.builder()
        .token(bot_token)
        .post_init(post_init)
        .read_timeout(15)
        .get_updates_read_timeout(42)
        .build()
    )

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("movie", movie_command))
    application.add_handler(CommandHandler("serial", serial_command))
    application.add_handler(CommandHandler("cartoon", cartoon_command))
    application.add_handler(CommandHandler("add", broadcast_command))
    application.add_handler(CommandHandler("db", db_command))

    # Додаємо callback handler для "Ще один ..." кнопки
    application.add_handler(CallbackQueryHandler(another_handler, pattern=r"^another:"))
    application.add_error_handler(error_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
