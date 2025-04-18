import json
from typing import Callable, cast

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from src.per_chat_config.models.config_entry import ConfigEntry
from src.store.db import Session


class ConfigField[T: int | float | bool | str]:
    """
    A class representing a configuration field for a chat.
    - `key`: The key for the configuration field.
    - `description`: A description of the configuration field.
    - `default`: The default value for the configuration field.
    - `check`: An optional function to validate the value before setting it.
    """

    def __init__(self, key: str, description: str, default: T, check: Callable[[T], bool] | None = None) -> None:
        self.key = key
        self.description = description
        self.default = default
        self._check = check

    @staticmethod
    def _serialize(value: T) -> str:
        """Serialize the value to a JSON string."""
        return json.dumps(value)

    @staticmethod
    def _deserialize(value: str) -> T:
        """Deserialize the JSON string back to the original type."""
        return cast(T, json.loads(value))

    async def get(self, chat_id: int) -> T:
        """Get the value from the database. If not found, return the default value."""
        async with Session() as session:
            result = await session.scalar(
                select(ConfigEntry).where(
                    ConfigEntry.chat_id == chat_id,
                    ConfigEntry.key == self.key,
                ),
            )
            if result is None:
                return self.default
            return self._deserialize(result.value)

    async def set(self, chat_id: int, value: T) -> bool:
        """Set the value in the database. If the value is invalid, return `False` without updating the database."""
        if self._check is not None and not self._check(value):
            return False
        async with Session() as session:
            await session.execute(
                insert(ConfigEntry)
                .values(chat_id=chat_id, key=self.key, value=self._serialize(value))
                .on_conflict_do_update(index_elements=["chat_id", "key"], set_={"value": self._serialize(value)})
            )
            await session.commit()
        return True
