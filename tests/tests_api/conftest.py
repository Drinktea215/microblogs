from src.database.config import (
    DB_HOST_TEST,
    DB_NAME_TEST,
    DB_PASS_TEST,
    DB_PORT_TEST,
    DB_USER_TEST,
    REDIS_CLIENT_TEST,
    REDIS_PORT_TEST,
)
import os

os.environ["ENV"] = "test"
DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
os.environ["DATABASE_URL_TEST"] = DATABASE_URL_TEST

import pytest
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
from database.redis_client import get_redis
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from src.database.crud import UserDAL
from src.database.models import Base
from src.database.db import get_db, get_database_url
from src.main import app
import shutil

engine = create_async_engine(get_database_url(), echo=True)
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)

Base.metadata.bind = engine


def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    with async_session_maker() as session:
        yield session


def override_get_redis():
    return Redis(host=REDIS_CLIENT_TEST, port=REDIS_PORT_TEST, db=0)


app.dependency_overrides[get_db] = override_get_async_session
app.dependency_overrides[get_redis] = override_get_redis


@pytest.fixture(autouse=True, scope="session")
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        udal = UserDAL(session)
        await udal.add_new_user("Dog", "user1")
        await udal.add_new_user("Cat", "user2")
        await udal.add_new_user("Mouth", "user3")
        await udal.add_new_user("Fish", "user4")
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    shutil.rmtree("../upload_files")
    os.mkdir("../upload_files")

    await override_get_redis().flushall(asynchronous=True)


@pytest.fixture(scope="session")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
