from fastapi import APIRouter, Header, Depends
from database.db import get_db
from database.crud import *

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
    udal = UserDAL(db_session)
    profile = await udal.get_profile(api_key)
    return {"result": True, "user": profile}


@router_users.get("/{id}")
async def alien_profile(id: int, api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    udal = UserDAL(db_session)
    profile = await udal.get_profile(id, alien=True)
    return {"result": True, "user": profile}
