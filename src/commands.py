import logging
import os
from datetime import datetime
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from .content_fetcher import get_random_content
from .config import uakino_url, app_version, admin_id
from .database import Database

logger = logging.getLogger(__name__)

db = Database()


def register_user(update: Update) -> None:
    user = update.effective_user
    db.add_user(user.id, user.username, user.first_name, user.last_name)


async def start_command(update: Update, context) -> None:
    logger.info(update)
    register_user(update)
    await update.message.reply_text(
        f"Привіт 🏴‍☠️\n\nЯ покажу тобі випадковий фільм/серіал/мультфільм з сайту <a href='https://{uakino_url}'>uakino</a>\n\n"
        "<b>Список команд:</b>\n/movie <i>фільм</i>\n/serial <i>серіал</i>\n/cartoon <i>мультфільм</i>\n\n"
        f"<b>Версія:</b> {app_version}\n\n"
        f"<blockquote>Бот був створений задля розваги і немає ніякого зв'язку з сайтом https://{uakino_url} як і <a href='https://t.me/sigmanor'>автор</a> бота\n\nВихідний код бота можна знайти на <a href='https://github.com/Sigmanor/uakino.club_bot'>GitHub</a></blockquote>",
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

    # Create link button row
    keyboard = [
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
    register_user(update)

    if update.effective_user.id != admin_id:
        await update.message.reply_text("You don't have permission to use this command")
        return

    if not context.args:
        await update.message.reply_text("Please provide a message to broadcast")
        return

    message = " ".join(context.args)
    users = db.get_all_users()
    sent = 0
    failed = 0

    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
            sent += 1
        except:
            failed += 1

    await update.message.reply_text(f"Message sent to {sent} users\nFailed: {failed}")


async def db_command(update: Update, context) -> None:
    register_user(update)

    if update.effective_user.id != admin_id:
        await update.message.reply_text("You don't have permission to use this command")
        return

    users = db.get_all_users_data()

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>UAKino Bot Users</title>
        <style>
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h2>UAKino Bot Users - {date}</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Username</th>
                <th>First Name</th>
                <th>Last Name</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """

    rows = ""
    for user in users:
        rows += f"""
            <tr>
                <td>{user[0]}</td>
                <td>{user[1] or '-'}</td>
                <td>{user[2] or '-'}</td>
                <td>{user[3] or '-'}</td>
            </tr>
        """

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_content = html_content.format(date=current_date, rows=rows)

    filename = f"users_{current_date.replace(' ', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    await update.message.reply_document(
        document=open(filename, "rb"), filename=filename, caption=f"Total users: {len(users)}"
    )

    os.remove(filename)
