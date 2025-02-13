import logging
from telegram.ext import Application, CommandHandler
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


async def error_handler(update, context) -> None:
    logger = logging.getLogger(__name__)
    logger.error("Exception while handling an update:", exc_info=context.error)

    if isinstance(context.error, NetworkError):
        logger.info("Network error occurred. Continuing operation...")
        return


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

    application.add_error_handler(error_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
