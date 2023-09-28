from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/postgres"

engine = create_async_engine(DATABASE_URL)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_db():
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
