"""
Base command handlers and user registration functionality.
"""
import logging
from telegram import Update
from telegram.constants import ParseMode
from services.database import Database
from config.settings import uakino_url, app_version

logger = logging.getLogger(__name__)

db = Database()


def _register_user(update: Update) -> None:
    """
    Register a new user in the database if they don't already exist.

    Args:
        update: Telegram update object containing user information
    """
    user = update.effective_user
    db.add_user(user.id, user.username, user.first_name, user.last_name)


async def start_command(update: Update, context) -> None:
    """
    Handle the /start command. Sends a welcome message with bot information.

    Args:
        update: Telegram update object
        context: CallbackContext object
    """
    logger.info(update)
    _register_user(update)

    await update.message.reply_text(
        f"Привіт 🏴‍☠️\n\n"
        f"Я покажу тобі випадковий фільм/серіал/мультфільм з сайту <a href='https://{uakino_url}'>uakino</a>\n\n"
        "<b>Список команд:</b>\n/movie <i>фільм</i>\n/serial <i>серіал</i>\n/cartoon <i>мультфільм</i>\n\n"
        f"<b>Версія:</b> {app_version}\n\n"
        f"<blockquote>Бот був створений задля розваги і немає ніякого зв'язку з сайтом https://{uakino_url} як і "
        f"<a href='https://t.me/sigmanor'>автор</a> бота\n\n"
        f"Вихідний код бота можна знайти на <a href='https://github.com/Sigmanor/uakino.club_bot'>GitHub</a></blockquote>",
        disable_web_page_preview=True,
        parse_mode=ParseMode.HTML,
    )
