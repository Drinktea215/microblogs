import pytest
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from database.crud import UserDAL
from src.database.db import get_db
from src.database.models import *
from src.database.config import DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST, DB_USER_TEST
from src.main import app

DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False, autoflush=False)

Base.metadata.bind = engine_test


@pytest.fixture(scope='session')
async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(autouse=True, scope='session')
async def create_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        udal = UserDAL(conn)
        await udal.add_new_user('Dog', 'user1')
        await udal.add_new_user('Cat', 'user2')
        await udal.add_new_user('Mouth', 'user3')
        await udal.add_new_user('Fish', 'user4')
    yield
    # async with engine_test.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


app.dependency_overrides[get_db] = override_get_async_session
transport = ASGITransport(app=app)
async_client = AsyncClient(transport=transport, base_url="http://test")
