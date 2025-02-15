"""
Message formatting utilities for content and admin reports.
"""
from typing import List, Tuple
from datetime import datetime


def build_content_message(content_data: List[str]) -> Tuple[str, str]:
    """
    Build formatted message for content display.

    Args:
        content_data: List containing content information in order:
            [name, year, genre, link, description, imdb, image_url, actors]

    Returns:
        Tuple containing (caption_text, image_url)
    """
    name, year, genre, _, description, imdb, image_url, actors = content_data

    # Only include description if it's meaningful (more than 5 chars)
    description_text = description if len(description.strip()) > 5 else ''

    caption_text = (
        f"<b>{name} ({year})</b>\n\n"
        f"<b>IMDb:</b> {imdb}\n"
        f"<b>Жанр:</b> {genre}\n"
        f"<b>Актори:</b> {actors}\n\n"
        f"{description_text}"
    )

    return caption_text, image_url


def build_admin_report(users_data: List[Tuple]) -> Tuple[str, str]:
    """
    Generate HTML report of registered users.

    Args:
        users_data: List of tuples containing user information:
            [(user_id, username, first_name, last_name), ...]

    Returns:
        Tuple containing (html_content, filename)
    """
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"users_{current_date.replace(' ', '_')}.html"

    rows = "\n".join(
        f"""
            <tr>
                <td>{user[0]}</td>
                <td>{user[1] or '-'}</td>
                <td>{user[2] or '-'}</td>
                <td>{user[3] or '-'}</td>
            </tr>
        """
        for user in users_data
    )

    html_content = f"""
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
        <h2>UAKino Bot Users - {current_date}</h2>
        <table>
            <tr>
                <th>ID</th><th>Username</th><th>First Name</th><th>Last Name</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>"""

    return html_content, filename
