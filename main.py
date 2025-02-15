"""
Main entry point for the UAKino Telegram Bot.
Initializes the bot, sets up logging, and registers command handlers.
"""
import logging
import sys
from telegram.ext import ApplicationBuilder, CommandHandler

from config.settings import bot_token
from handlers.base import start_command
from handlers.content import movie_command, cartoon_command, serial_command
from handlers.admin import broadcast_command, db_command
from services.database import Database

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("bot.log", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)


def register_handlers(application) -> None:
    """
    Register all command handlers with the application.

    Args:
        application: The telegram bot application instance
    """
    # Basic commands
    application.add_handler(CommandHandler("start", start_command))

    # Content commands
    application.add_handler(CommandHandler("movie", movie_command))
    application.add_handler(CommandHandler("cartoon", cartoon_command))
    application.add_handler(CommandHandler("serial", serial_command))

    # Admin commands
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    application.add_handler(CommandHandler("db", db_command))


async def main() -> None:
    """
    Initialize and start the bot application.
    """
    # Initialize database
    db = Database()
    logger.info("Database initialized")

    # Create application instance
    application = ApplicationBuilder().token(bot_token).build()

    # Register command handlers
    register_handlers(application)
    logger.info("Handlers registered")

    # Start the bot
    await application.run_polling()


if __name__ == "__main__":
    try:
        import asyncio
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Bot crashed: {e}", exc_info=True)
        sys.exit(1)
