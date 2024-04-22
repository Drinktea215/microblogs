import pytest


class TestUser:
    @pytest.mark.asyncio(scope="session")
    @pytest.mark.parametrize(
        "api_key, idx",
        [
            ("user1", 3),
            ("user1", 4),
            ("user2", 1),
            ("user2", 3),
            ("user2", 4),
            ("user3", 1),
            ("user3", 2),
            ("user3", 4),
            ("user4", 2),
            ("user4", 3),
        ],
    )
    async def test_add_follow(self, async_client, api_key: str, idx: int):
        response = await async_client.post(
            f"/api/users/{idx}/follow", headers={"api-key": api_key}
        )
        assert response.status_code == 200
        assert response.json() == {"result": True}

    @pytest.mark.asyncio(scope="session")
    async def test_my_profile_before_del(self, async_client):
        response = await async_client.get(
            f"/api/users/me", headers={"api-key": "user3"}
        )
        assert response.status_code == 200
        response = response.json()
        assert response["result"] is True
        assert response["user"]["followers"] == [
            {"id": 1, "name": "Dog"},
            {"id": 2, "name": "Cat"},
            {"id": 4, "name": "Fish"},
        ]
        assert response["user"]["following"] == [
            {"id": 1, "name": "Dog"},
            {"id": 2, "name": "Cat"},
            {"id": 4, "name": "Fish"},
        ]

    @pytest.mark.asyncio(scope="session")
    async def test_alien_profile_before_del(self, async_client):
        response = await async_client.get(
            f"/api/users/4", headers={"api-key": "user3"}
        )
        assert response.status_code == 200
        response = response.json()
        assert response["result"] is True
        assert response["user"]["followers"] == [
            {"id": 1, "name": "Dog"},
            {"id": 2, "name": "Cat"},
            {"id": 3, "name": "Mouth"},
        ]
        assert response["user"]["following"] == [
            {"id": 2, "name": "Cat"},
            {"id": 3, "name": "Mouth"},
        ]

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.parametrize(
        "api_key, idx",
        [
            ("user1", 4),
            ("user2", 1),
            ("user2", 3),
            ("user3", 2),
            ("user3", 4),
            ("user4", 2),
        ],
    )
    async def test_del_follow(self, async_client, api_key: str, idx: int):
        response = await async_client.delete(
            f"/api/users/{idx}/follow", headers={"api-key": api_key}
        )
        assert response.status_code == 200
        assert response.json() == {"result": True}

    @pytest.mark.asyncio(scope="session")
    async def test_my_profile_after_del_from_redis(self, async_client):
        response = await async_client.get(
            f"/api/users/me", headers={"api-key": "user3"}
        )
        assert response.status_code == 200
        response = response.json()
        assert response["result"] is True
        assert response["user"]["followers"] == [
            {"id": 1, "name": "Dog"},
            {"id": 2, "name": "Cat"},
            {"id": 4, "name": "Fish"},
        ]
        assert response["user"]["following"] == [
            {"id": 1, "name": "Dog"},
            {"id": 2, "name": "Cat"},
            {"id": 4, "name": "Fish"},
        ]

    @pytest.mark.asyncio(scope="session")
    async def test_alien_profile_after_del(self, async_client):
        response = await async_client.get(
            f"/api/users/3", headers={"api-key": "user4"}
        )
        assert response.status_code == 200
        response = response.json()
        assert response["result"] is True
        assert response["user"]["followers"] == [
            {"id": 1, "name": "Dog"},
            {"id": 4, "name": "Fish"},
        ]
        assert response["user"]["following"] == [{"id": 1, "name": "Dog"}]
