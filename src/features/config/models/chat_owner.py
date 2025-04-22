from sqlalchemy import BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.store.db import Base


class ChatOwner(Base):
    """
    Model for storing chat owners.
    - `chat_id`: Unique identifier for the chat.
    - `owner_id`: The user ID of the chat owner.
    """

    __tablename__ = "chat_owners"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    owner_id: Mapped[int] = mapped_column(BigInteger, index=True)
