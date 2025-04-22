import asyncio

from src.features.anecdote import anecdote_feature
from src.features.captcha import captcha_feature
from src.features.config import config_feature
from src.store.db import setup_db
from src.utils.bot import BOT


def setup_features() -> None:
    captcha_feature.setup()
    anecdote_feature.setup()
    config_feature.setup()


async def main() -> None:
    setup_features()
    await setup_db()
    await BOT.run_until_disconnected()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
