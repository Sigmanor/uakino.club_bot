import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("TOKEN")
admin_id = int(os.getenv("ADMIN"))
uakino_url = "uakino.me"
app_version = "1.4.0"
