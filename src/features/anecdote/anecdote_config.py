from dataclasses import dataclass
from typing import Final

from src.per_chat_config.config_field import ConfigField


@dataclass(frozen=True)
class AnecdoteConfig:
    """Configuration for the Anecdote feature."""

    ACTIVITY_TIMEOUT_INTERVAL = 5

    INACTIVITY_TIMEOUT = ConfigField(
        key="inactivity_timeout",
        description="Time in seconds before sending an anecdote",
        default=5,
    )


ANECDOTE_CONFIG: Final = AnecdoteConfig()
