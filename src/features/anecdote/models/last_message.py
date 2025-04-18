from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import current_timestamp

from src.store.db import Base


class LastMessage(Base):
    """
    Model for storing the last message sent in a chat.
    - `chat_id`: Unique identifier for the chat.
    - `updated_at`: Timestamp of when the last message was sent.
    """

    __tablename__ = "last_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=current_timestamp())
