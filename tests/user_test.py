from conftest import async_session_maker, client
from sqlalchemy import insert, select
from database.models import *
from database.crud import *


async def test_add_users():
    response = await client.post("/api/tweets/", json={"tweet_data": "Hello!", "tweet_media_ids": []})
    assert response.status_code == 200