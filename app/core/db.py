import logging
from typing import Annotated, AsyncIterator


from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app.core.config import config

logger = logging.getLogger(__name__)

async_engine = create_async_engine(
    str(config.DB_URL),
    pool_pre_ping=True,
    echo=config.LOG_LEVEL == "DEBUG",
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    future=True,
)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            logger.exception(e)
            raise e     


session = Annotated[async_sessionmaker, Depends(get_session)]