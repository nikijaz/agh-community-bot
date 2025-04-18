from typing import Final

from telethon import TelegramClient

from src.utils.app_config import APP_CONFIG

BOT: Final = TelegramClient(
    session="bot",
    api_id=APP_CONFIG.TELEGRAM_API_ID,
    api_hash=APP_CONFIG.TELEGRAM_API_HASH,
).start(bot_token=APP_CONFIG.TELEGRAM_BOT_TOKEN)
