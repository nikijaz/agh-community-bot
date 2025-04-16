from datetime import datetime, timezone

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.store.db_store import Base


class ConfigEntryModel(Base):
    __tablename__ = "config"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, index=True)
    key: Mapped[str] = mapped_column(String(256), index=True)
    value: Mapped[str] = mapped_column(String(256))
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
