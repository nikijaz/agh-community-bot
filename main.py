import asyncio
from typing import Final

from telethon import TelegramClient

from src.features.anecdote.anecdote_feature import AnecdoteFeature
from src.features.captcha.captcha_feature import CaptchaFeature
from src.store.db_store import setup_dp_store
from src.utils.config import CONFIG

bot: Final = TelegramClient(
    session="bot",
    api_id=CONFIG.TELEGRAM_API_ID,
    api_hash=CONFIG.TELEGRAM_API_HASH,
).start(bot_token=CONFIG.TELEGRAM_BOT_TOKEN)


def setup_features() -> None:
    CaptchaFeature(bot).setup()
    AnecdoteFeature(bot).setup()


async def main() -> None:
    setup_features()
    await setup_dp_store()
    await bot.run_until_disconnected()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
