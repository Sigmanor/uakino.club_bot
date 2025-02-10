import sqlite3
from datetime import datetime
import os


class Database:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        db_path = os.path.join(data_dir, "bot.db")
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                joined_at TIMESTAMP
            )
        """
        )
        self.conn.commit()

    def add_user(self, user_id, username, first_name, last_name):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, joined_at)
            VALUES (?, ?, ?, ?, ?)
        """,
            (user_id, username, first_name, last_name, datetime.now()),
        )
        self.conn.commit()

    def get_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT user_id FROM users")
        return [row[0] for row in cursor.fetchall()]

    def get_all_users_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT user_id, username, first_name, last_name FROM users")
        return cursor.fetchall()
