from httpx import AsyncClient

from conftest import async_session_maker, async_client
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.crud import UserDAL


# from src.database.models import *
# from src.database.crud import *


async def test_add_users():
    # assert True
    response = await async_client.post(
        "/api/tweets/",
        headers={"api-key": "user1"},
        json={"tweet_data": "Hello!", "tweet_media_ids": []}
    )
    assert response.status_code == 200