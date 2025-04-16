from typing import Final

from src.config.config_entry import ConfigEntry


class AnecdoteConfig:
    REDIS_ACTIVE_TIME_KEY = "active_time"
    REDIS_ANECDOTE_TIME_KEY = "anecdote_time"

    INACTIVITY_TIMEOUT = ConfigEntry(
        key="inactivity_timeout",
        description="Time in seconds before sending an anecdote",
        default=60,
    )


ANECDOTE_CONFIG: Final = AnecdoteConfig()
