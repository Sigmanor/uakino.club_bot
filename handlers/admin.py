"""
Admin-only command handlers for broadcast and database operations.
"""
import logging
import os
from datetime import datetime
from telegram import Update
from config.settings import admin_id
from services.database import Database
from handlers.base import _register_user

logger = logging.getLogger(__name__)

db = Database()


async def broadcast_command(update: Update, context) -> None:
    """
    Broadcast a message to all registered users. Admin only command.

    Args:
        update: Telegram update object
        context: CallbackContext object containing the message to broadcast
    """
    logger.info(update)
    _register_user(update)

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
        except Exception as e:
            logger.error(f"Failed to send broadcast to user {user_id}: {e}")
            failed += 1

    await update.message.reply_text(f"Message sent to {sent} users\nFailed: {failed}")


async def db_command(update: Update, context) -> None:
    """
    Generate and send an HTML report of all registered users. Admin only command.

    Args:
        update: Telegram update object
        context: CallbackContext object
    """
    logger.info(update)
    _register_user(update)

    if update.effective_user.id != admin_id:
        await update.message.reply_text("You don't have permission to use this command")
        return

    users = db.get_all_users_data()
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows = "\n".join(
        f"""
            <tr>
                <td>{user[0]}</td>
                <td>{user[1] or '-'}</td>
                <td>{user[2] or '-'}</td>
                <td>{user[3] or '-'}</td>
            </tr>
        """
        for user in users
    )

    html_content = f"""<!DOCTYPE html>
    <html><head><title>UAKino Bot Users</title><style>
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
    </style></head><body>
        <h2>UAKino Bot Users - {current_date}</h2>
        <table>
            <tr><th>ID</th><th>Username</th><th>First Name</th><th>Last Name</th></tr>
            {rows}
        </table>
    </body></html>"""

    filename = f"users_{current_date.replace(' ', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    await update.message.reply_document(
        document=open(filename, "rb"),
        filename=filename,
        caption=f"Total users: {len(users)}"
    )

    os.remove(filename)
