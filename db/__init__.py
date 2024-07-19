from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from config import config
from .models import Base, User

engine = create_async_engine(
    config.db_url,
)

sessionmaker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = sessionmaker()
    try:
        yield session
    finally:
        await session.close()
