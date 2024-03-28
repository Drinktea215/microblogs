from httpx import AsyncClient

from conftest import async_session_maker, async_client
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.crud import UserDAL


# from src.database.models import *
# from src.database.crud import *


# udal = UserDAL(get_db())
# udal.add_new_user('Dog', 'user1')
# udal.add_new_user('Cat', 'user2')
# udal.add_new_user('Mouth', 'user3')
# udal.add_new_user('Fish', 'user4')
# udal.add_new_user('test', 'test')
async def test_add_users():
    # assert True
    response = await async_client.post(
        "/api/tweets/",
        headers={"api-key": "user1"},
        json={"tweet_data": "Hello!", "tweet_media_ids": []}
    )
    assert response.status_code == 200