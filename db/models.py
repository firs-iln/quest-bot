from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)


class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    username: Mapped[Optional[str]]
    quest_passed: Mapped[bool] = mapped_column(default=False)
    quest_passed_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    wallet_address: Mapped[Optional[str]]
