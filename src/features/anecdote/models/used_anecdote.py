from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import current_timestamp

from src.store.db import Base


class UsedAnecdote(Base):
    """
    Model for storing used anecdotes data.
    - `chat_id`: Unique identifier for the chat.
    - `hash`: Unique hash for the anecdote.
    - `inserted_at`: Timestamp of when the anecdote was used.
    """

    __tablename__ = "used_anecdotes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, index=True)
    hash: Mapped[str] = mapped_column(String(16))
    inserted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=current_timestamp())
