from fastapi import APIRouter, Header, Depends
from database.db import get_db
from database.crud import *
from redis_client import redis_cli
import json

router_users = APIRouter(prefix="/users", tags=["Users"])


@router_users.post("/{id}/follow")
async def add_follow(id: int, api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    udal = UserDAL(db_session)
    await udal.follow(id, api_key, add=True)
    return {"result": True}


@router_users.delete("/{id}/follow")
async def del_follow(id: int, api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    udal = UserDAL(db_session)
    await udal.follow(id, api_key, add=False)
    return {"result": True}


@router_users.get("/me")
async def my_profile(api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    response = await redis_cli.get(f"{api_key}_me")
    if response is None:
        udal = UserDAL(db_session)
        profile = await udal.get_profile(api_key)
        await redis_cli.set(f"{api_key}_me", json.dumps(profile), 10)
    else:
        profile = json.loads(response.decode("utf-8"))
    return {"result": True, "user": profile}


@router_users.get("/{id}")
async def alien_profile(id: int, api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    response = await redis_cli.get(f"profile_{id}")
    if response is None:
        udal = UserDAL(db_session)
        profile = await udal.get_profile(id, alien=True)
        await redis_cli.set(f"profile_{id}", json.dumps(profile), 10)
    else:
        profile = json.loads(response.decode("utf-8"))
    return {"result": True, "user": profile}
