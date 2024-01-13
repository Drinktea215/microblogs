from conftest import async_session_maker, client
from sqlalchemy import insert, select
from database.models import *
from database.crud import *


async def test_add_users():
    async with async_session_maker() as session:
        user = await session.execute(select(Users).where(Users.id == 1))
        user = user.scalars().one_or_none()
        # assert 1 == 1
        # udal = UserDAL(session)
        # result = await udal.add_new_user('Dog', 'user1')
        # assert result == "Complete", "No complete"
        # assert await udal.add_new_user('Cat', 'user2') == "Complete"
        # assert await udal.add_new_user('Mouth', 'user3') == "Complete"
        # assert await udal.add_new_user('Fish', 'user4') == "Complete"

