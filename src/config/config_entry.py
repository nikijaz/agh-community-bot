import json
from typing import Callable, cast

from sqlalchemy import select, update

from src.config.models.config_entry_model import ConfigEntryModel
from src.store.db_store import async_session


class ConfigEntry[T: int | float | bool | str]:
    def __init__(
        self,
        key: str,
        description: str,
        default: T,
        check: Callable[[T], bool] | None = None,
    ):
        self.type = type(default)

        self.key = key
        self.description = description
        self.default = default
        self.check = check

    def __cast_value(self, value: str) -> T:
        return cast(T, json.loads(value))

    async def __get_from_db(self, chat_id: int) -> T | None:
        async with async_session() as session:
            result = await session.execute(
                select(ConfigEntryModel).filter_by(chat_id=chat_id, key=self.key)
            )
            config_entry_model = result.scalars().first()

            if config_entry_model is not None:
                return self.__cast_value(config_entry_model.value)
            return None

    async def get(self, chat_id: int) -> T:
        value = await self.__get_from_db(chat_id)
        if value is not None:
            return value
        return self.default

    async def set(self, chat_id: int, value: T) -> None:
        async with async_session() as session:
            if await self.__get_from_db(chat_id) is None:
                config_entry_model = ConfigEntryModel(
                    chat_id=chat_id,
                    key=self.key,
                    value=json.dumps(value),
                )
                session.add(config_entry_model)
                await session.commit()
            else:
                await session.execute(
                    update(ConfigEntryModel)
                    .filter_by(chat_id=chat_id, key=self.key)
                    .values(value=json.dumps(value))
                )
