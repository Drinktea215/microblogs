from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase
from .config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
import os


def get_database_url():
    if os.environ.get("ENV") == "test":
        return os.getenv("DATABASE_URL_TEST")
    else:
        return os.getenv("DATABASE_URL")


DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
os.environ["DATABASE_URL"] = DATABASE_URL

engine = create_async_engine(get_database_url(), echo=True)

async_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        yield session
