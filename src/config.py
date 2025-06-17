import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("TOKEN")
admin_id = int(os.getenv("ADMIN"))
uakino_url = "uakino.best"
app_version = "1.9.1"
