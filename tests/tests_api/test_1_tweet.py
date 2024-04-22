import pytest
import os.path


class TestTweets:
    @pytest.mark.asyncio(scope="session")
    @pytest.mark.parametrize(
        "api_key, text, idx",
        [
            ("user1", "Hello, world!", 1),
            ("user2", "Hello, Who are you?", 2),
            ("user3", "And you?", 3),
            ("user4", "What?", 4),
            ("user1", "I'm friend!", 5),
            ("user2", "Oh! Really?!", 6),
            ("user3", "And you?", 7),
            ("user4", "What?", 8),
        ],
    )
    async def test_add_tweet(
        self, async_client, api_key: str, text: str, idx: int
    ):
        response = await async_client.post(
            "/api/tweets/",
            headers={"api-key": api_key},
            json={"tweet_data": text, "tweet_media_ids": []},
        )
        assert response.status_code == 200
        assert response.json() == {"result": True, "tweet_id": idx}

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.parametrize(
        "api_key, image, idx",
        [
            ("user1", "../tests/cats.jpg", 1),
            ("user1", "../tests/cats.jpg", 2),
            ("user3", "../tests/cats.jpg", 3),
        ],
    )
    async def test_add_media(
        self, async_client, api_key: str, image: str, idx: int
    ):
        response = await async_client.post(
            "/api/medias/",
            headers={"api-key": api_key},
            files={"file": open(image, "rb")},
        )
        assert response.status_code == 200
        assert response.json() == {"media_id": idx, "result": True}

    @pytest.mark.asyncio(scope="session")
    async def test_add_tweet_with_images_1(self, async_client):
        response = await async_client.post(
            "/api/tweets/",
            headers={"api-key": "user1"},
            json={"tweet_data": "This is my cat's", "tweet_media_ids": [1, 2]},
        )
        assert response.status_code == 200
        assert response.json() == {"result": True, "tweet_id": 9}
        assert os.path.isdir("../upload_files/9") is True
        assert os.path.isfile("../upload_files/9/1.jpg") is True
        assert os.path.isfile("../upload_files/9/2.jpg") is True

    @pytest.mark.asyncio(scope="session")
    async def test_add_tweet_with_images_2(self, async_client):
        response = await async_client.post(
            "/api/tweets/",
            headers={"api-key": "user3"},
            json={"tweet_data": "And this my", "tweet_media_ids": [3]},
        )
        assert response.status_code == 200
        assert response.json() == {"result": True, "tweet_id": 10}
        assert os.path.isdir("../upload_files/10") is True
        assert os.path.isfile("../upload_files/10/3.jpg") is True

    @pytest.mark.asyncio(scope="session")
    async def test_del_tweet(self, async_client):
        response = await async_client.delete(
            "/api/tweets/10", headers={"api-key": "user3"}
        )
        assert response.status_code == 200
        assert os.path.isdir("../upload_files/10") is False

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.parametrize(
        "api_key, idx",
        [
            ("user1", 2),
            ("user1", 4),
            ("user2", 1),
            ("user2", 3),
            ("user3", 2),
            ("user3", 4),
            ("user4", 1),
            ("user4", 2),
        ],
    )
    async def test_add_like(self, async_client, api_key: str, idx: int):
        response = await async_client.post(
            f"/api/tweets/{idx}/likes", headers={"api-key": api_key}
        )
        assert response.status_code == 200
        assert response.json() == {"result": True}

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.parametrize("api_key, idx", [("user2", 1), ("user3", 4)])
    async def test_del_like(self, async_client, api_key: str, idx: int):
        response = await async_client.delete(
            f"/api/tweets/{idx}/likes", headers={"api-key": api_key}
        )
        assert response.status_code == 200
        assert response.json() == {"result": True}

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.parametrize("api_key", ["user3"])
    async def test_get_tweets(self, async_client, api_key):
        response = await async_client.get(
            "/api/tweets/", headers={"api-key": api_key}
        )

        assert response.status_code == 200
        response = response.json()
        assert response["result"] is True
        assert len(response["tweets"]) == 9
        assert len(response["tweets"][0]["attachments"]) == 2
        assert len(response["tweets"][-1]["likes"]) == 1
