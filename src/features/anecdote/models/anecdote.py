from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import current_timestamp

from src.store.db import Base


class Anecdote(Base):
    """
    Model for storing anecdotes.
    - `chat_id`: Unique identifier for the chat.
    - `text`: The text of the anecdote.
    - `used`: A boolean indicating whether the anecdote has been used.
    - `inserted_at`: Timestamp of when the anecdote was sent.
    """

    __tablename__ = "anecdotes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, index=True)
    text: Mapped[str] = mapped_column(String)
    used: Mapped[bool] = mapped_column(index=True, default=False)
    inserted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=current_timestamp())
