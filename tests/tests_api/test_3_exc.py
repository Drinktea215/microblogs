import pytest


@pytest.mark.asyncio(scope="session")
async def test_api_key_dont_find(async_client):
    response = await async_client.post(
        "/api/tweets/",
        headers={"api-key": "user5"},
        json={"tweet_data": "text", "tweet_media_ids": []},
    )
    assert response.status_code == 200
    assert response.json() == {
        "result": False,
        "error_type": "ApiKeyDontFind",
        "error_message": "You are not registered",
    }


@pytest.mark.asyncio(scope="session")
async def test_tweet_dont_find(async_client):
    response = await async_client.delete(
        f"/api/tweets/10", headers={"api-key": "user1"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "result": False,
        "error_type": "TweetDontFind",
        "error_message": "Message don't find",
    }


@pytest.mark.asyncio(scope="session")
async def test_like_is_exist(async_client):
    response = await async_client.post(
        "/api/tweets/",
        headers={"api-key": "user1"},
        json={"tweet_data": "text", "tweet_media_ids": []},
    )
    assert response.status_code == 200

    response = await async_client.post(
        f"/api/tweets/1/likes", headers={"api-key": "user2"}
    )
    assert response.status_code == 200

    response = await async_client.post(
        f"/api/tweets/1/likes", headers={"api-key": "user2"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "result": False,
        "error_type": "LikeIsExist",
        "error_message": "Like is exist",
    }


@pytest.mark.asyncio(scope="session")
async def test_like_doesnt_exist(async_client):
    response = await async_client.delete(
        f"/api/tweets/1/likes", headers={"api-key": "user3"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "result": False,
        "error_type": "LikeDoesntExist",
        "error_message": "Like doesn't exist",
    }


@pytest.mark.asyncio(scope="session")
async def test_max_size_file(async_client):
    response = await async_client.post(
        "/api/medias/",
        headers={"api-key": "user1"},
        files={"file": open("../tests/dog.png", "rb")},
    )
    assert response.status_code == 200
    assert response.json() == {
        "result": False,
        "error_type": "MaxSizeFile",
        "error_message": "Very big file. The file must not exceed 5 Mb.",
    }


@pytest.mark.asyncio(scope="session")
async def test_user_dont_find(async_client):
    response = await async_client.post(
        f"/api/users/10/follow", headers={"api-key": "user4"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "result": False,
        "error_type": "UserDontFind",
        "error_message": "User don't find on id",
    }
