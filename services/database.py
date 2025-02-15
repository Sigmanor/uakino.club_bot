"""
Database service for managing user data and interactions.
Provides a simple SQLite interface for storing user information.
"""
import sqlite3
import os
import logging
from datetime import datetime
from typing import List, Tuple

logger = logging.getLogger(__name__)


class Database:
    """Handles all database operations for the bot."""

    def __init__(self):
        """Initialize database connection and ensure tables exist."""
        # Move up one level from services to main project directory
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(project_dir, "data")
        os.makedirs(data_dir, exist_ok=True)

        db_path = os.path.join(data_dir, "bot.db")
        try:
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
            self.create_tables()
            logger.info("Database initialized successfully")
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    def create_tables(self) -> None:
        """Create necessary database tables if they don't exist."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    joined_at TIMESTAMP
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Failed to create tables: {e}")
            raise

    def add_user(self, user_id: int, username: str, first_name: str, last_name: str) -> None:
        """
        Add a new user to the database or update existing user.

        Args:
            user_id: Telegram user ID
            username: Telegram username
            first_name: User's first name
            last_name: User's last name
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO users (
                    user_id, username, first_name, last_name, joined_at
                ) VALUES (?, ?, ?, ?, ?)
            """, (user_id, username, first_name, last_name, datetime.now()))
            self.conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Failed to add user {user_id}: {e}")
            raise

    def get_all_users(self) -> List[int]:
        """
        Get all user IDs from the database.

        Returns:
            List of user IDs
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT user_id FROM users")
            return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Failed to get all users: {e}")
            raise

    def get_all_users_data(self) -> List[Tuple[int, str, str, str]]:
        """
        Get complete user data for all users.

        Returns:
            List of tuples containing (user_id, username, first_name, last_name)
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT user_id, username, first_name, last_name
                FROM users
            """)
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Failed to get all users data: {e}")
            raise

    def __del__(self):
        """Ensure database connection is closed on object destruction."""
        if hasattr(self, 'conn'):
            self.conn.close()
