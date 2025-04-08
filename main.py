from typing import Final

from telethon import TelegramClient

from src.features.anecdote.anecdote_feature import AnecdoteFeature
from src.features.captcha.captcha_feature import CaptchaFeature
from src.utils.config import CONFIG

bot: Final = TelegramClient(
    session="bot",
    api_id=CONFIG.TELEGRAM_API_ID,
    api_hash=CONFIG.TELEGRAM_API_HASH,
).start(bot_token=CONFIG.TELEGRAM_BOT_TOKEN)


def setup_features() -> None:
    CaptchaFeature(bot).setup()
    AnecdoteFeature(bot).setup()


def main() -> None:
    setup_features()
    bot.run_until_disconnected()


if __name__ == "__main__":
    main()
