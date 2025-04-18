from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import current_timestamp

from src.store.db import Base


class Captcha(Base):
    """
    Model for storing captcha data.
    - `chat_id`: Unique identifier for the chat.
    - `user_id`: Unique identifier for the user.
    - `message_id`: Unique identifier for the message.
    - `button_id`: Unique identifier for the button.
    - `inserted_at`: Timestamp of when the captcha was sent.
    """

    __tablename__ = "captchas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, index=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    message_id: Mapped[int] = mapped_column(BigInteger, index=True)
    button_id: Mapped[str] = mapped_column(String(16), index=True)
    inserted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=current_timestamp())
