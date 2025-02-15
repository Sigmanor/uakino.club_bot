"""
Application configuration and environment settings.

This module handles loading and validating all configuration values
from environment variables and defines constant values used throughout the application.
"""
import os
from typing import Final
from dotenv import load_dotenv

# Load environment variables from .env file
if not load_dotenv():
    raise RuntimeError("Failed to load .env file")

# Required environment variables
try:
    BOT_TOKEN: Final[str] = os.getenv("TOKEN")
    if not BOT_TOKEN:
        raise ValueError("TOKEN environment variable is not set")

    ADMIN_ID: Final[int] = int(os.getenv("ADMIN", "0"))
    if ADMIN_ID == 0:
        raise ValueError("ADMIN environment variable is not set or invalid")
except ValueError as e:
    raise RuntimeError(f"Configuration error: {e}")

# Application constants
APP_VERSION: Final[str] = "1.2.0"

# Service URLs and endpoints
UAKINO_URL: Final[str] = "uakino.me"

# Expose variables with original names for backward compatibility
# These will be used by existing code
bot_token = BOT_TOKEN
admin_id = ADMIN_ID
uakino_url = UAKINO_URL
app_version = APP_VERSION
