from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import current_timestamp

from src.store.db import Base


class ConfigEntry(Base):
    """
    Model for storing configuration entries for each chat.
    - `chat_id`: Unique identifier for the chat.
    - `key`: Configuration key.
    - `value`: Configuration value.
    - `inserted_at`: Timestamp of when the entry was created.
    """

    __tablename__ = "config_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, index=True)
    key: Mapped[str] = mapped_column(String(256), index=True)
    value: Mapped[str] = mapped_column(String(256))
    inserted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=current_timestamp())
