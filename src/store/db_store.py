from typing import Final

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.utils.config import CONFIG


class Base(DeclarativeBase):
    pass


DB_STORE: Final[AsyncEngine] = create_async_engine(CONFIG.DATABASE_URL)


async def setup_dp_store() -> None:
    async with DB_STORE.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async_session: Final = async_sessionmaker(DB_STORE, expire_on_commit=False)
