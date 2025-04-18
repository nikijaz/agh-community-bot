from typing import Final

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.utils.app_config import APP_CONFIG


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    pass


DB: Final[AsyncEngine] = create_async_engine(APP_CONFIG.DATABASE_URL)
Session: Final = async_sessionmaker(DB, expire_on_commit=False)


async def setup_db() -> None:
    """Setup the database store."""
    async with DB.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
