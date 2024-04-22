import pytest
from src.database.crud import *
from tests.tests_db.conftest import async_session_maker
from src.database.models import *
from sqlalchemy import select
from src.schemas import Tweetters


async def add_users(udal: UserDAL, count: int = 4):
    users = [
        ("Dog", "user1"),
        ("Cat", "user2"),
        ("Mouth", "user3"),
        ("Fish", "user4"),
    ]
    for u in users[:count]:
        await udal.add_new_user(u[0], u[1])


async def add_tweets(tdal: TweetDAL, count: int = 4):
    tweets = [
        ("user1", {"tweet_data": "Hello world!", "tweet_media_ids": []}),
        ("user2", {"tweet_data": "Hello world!", "tweet_media_ids": []}),
        ("user3", {"tweet_data": "Hello world!", "tweet_media_ids": []}),
        ("user4", {"tweet_data": "Hello world!", "tweet_media_ids": []}),
    ]
    for t in tweets[:count]:
        tt = Tweetters.model_validate(t[1])
        await tdal.create_tweet(t[0], tt)


@pytest.mark.asyncio
async def test_add_users():
    async with async_session_maker() as session:
        udal = UserDAL(session)
        await add_users(udal)

        response = await session.execute(select(Users))
        response = response.scalars().all()
        assert len(response) == 4


@pytest.mark.asyncio
async def test_find_user_on_id():
    async with async_session_maker() as session:
        udal = UserDAL(session)
        await add_users(udal)

        response = await find_user(2, session, False)
        assert response.name == "Cat"


@pytest.mark.asyncio
async def test_find_user_on_api_key():
    async with async_session_maker() as session:
        udal = UserDAL(session)
        await add_users(udal)

        response = await find_user("user4", session)
        assert response.name == "Fish"


@pytest.mark.asyncio
async def test_create_tweet():
    async with async_session_maker() as session:
        udal = UserDAL(session)
        await add_users(udal)
        tdal = TweetDAL(session)
        await add_tweets(tdal)
        response = await session.execute(select(Tweets))
        response = response.scalars().all()
        assert len(response) == 4


@pytest.mark.asyncio
async def test_find_tweet():
    async with async_session_maker() as session:
        udal = UserDAL(session)
        await add_users(udal)
        tdal = TweetDAL(session)
        await add_tweets(tdal)

        response = await find_tweet(2, session)
        assert response.author_id == 2


@pytest.mark.asyncio
async def test_delete_tweet():
    async with async_session_maker() as session:
        udal = UserDAL(session)
        await add_users(udal, 2)
        tdal = TweetDAL(session)
        await add_tweets(tdal, 2)
        r = await tdal.delete_tweet(1, "user1")
        assert r is True
        response = await session.execute(select(Tweets))
        response = response.scalars().all()
        assert len(response) == 1
        assert response[0].id == 2


@pytest.mark.asyncio
async def test_add_like():
    async with async_session_maker() as session:
        udal = UserDAL(session)
        await add_users(udal, 2)
        tdal = TweetDAL(session)
        await add_tweets(tdal, 1)
        await tdal.like(1, "user2")
        response = await session.execute(select(Tweets).where(Tweets.id == 1))
        response = response.scalars().one_or_none()
        assert len(response.likes) == 1


@pytest.mark.asyncio
async def test_del_like():
    async with async_session_maker() as session:
        udal = UserDAL(session)
        await add_users(udal, 3)
        tdal = TweetDAL(session)
        await add_tweets(tdal, 1)
        await tdal.like(1, "user2")
        await tdal.like(1, "user3")
        await tdal.like(1, "user2", add=False)
        response = await session.execute(select(Tweets).where(Tweets.id == 1))
        response = response.scalars().one_or_none()
        assert len(response.likes) == 1


@pytest.mark.asyncio
async def test_add_follow():
    async with async_session_maker() as session:
        udal = UserDAL(session)
        await add_users(udal)
        await udal.follow(1, "user3")
        await udal.follow(1, "user4")
        response = await session.execute(select(Users).where(Users.id == 1))
        response = response.scalars().one_or_none()
        followers = await session.execute(response.followers.select())
        followers = followers.scalars().all()
        assert len(followers) == 2


@pytest.mark.asyncio
async def test_del_follow():
    async with async_session_maker() as session:
        udal = UserDAL(session)
        await add_users(udal)
        await udal.follow(1, "user3")
        await udal.follow(1, "user4")
        await udal.follow(1, "user3", False)
        response = await session.execute(select(Users).where(Users.id == 1))
        response = response.scalars().one_or_none()
        followers = await session.execute(response.followers.select())
        followers = followers.scalars().all()
        assert len(followers) == 1


@pytest.mark.asyncio
async def test_get_all_tweets_for_user():
    async with async_session_maker() as session:
        udal = UserDAL(session)
        await add_users(udal)
        tdal = TweetDAL(session)
        await add_tweets(tdal)
        result_ok, result_bad = await udal.get_all_tweets_for_user()
        assert len(result_ok) == 4 and len(result_bad) == 0


@pytest.mark.asyncio
async def test_get_profile():
    async with async_session_maker() as session:
        udal = UserDAL(session)
        await add_users(udal)
        await udal.follow(2, "user1")
        await udal.follow(1, "user3")
        await udal.follow(1, "user4")
        user = await udal.get_profile("user1")
        assert user == {
            "id": 1,
            "name": "Dog",
            "followers": [
                {"id": 3, "name": "Mouth"},
                {"id": 4, "name": "Fish"},
            ],
            "following": [{"id": 2, "name": "Cat"}],
        }
