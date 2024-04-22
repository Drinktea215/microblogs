from fastapi import APIRouter, Header, Depends
from starlette.responses import JSONResponse
from database.db import get_db
from database.crud import *
from exc import ApiKeyDontFind, UserDontFind
from database.redis_client import get_redis
from redis.asyncio import Redis
from logger import logger
import json

router_users = APIRouter(prefix="/users", tags=["Users"])


@router_users.post("/{id}/follow", response_class=JSONResponse)
async def add_follow(
    id: int,
    api_key: str = Header(),
    db_session: AsyncSession = Depends(get_db),
):
    try:
        udal = UserDAL(db_session)
        await udal.follow(id, api_key, add=True)
        return JSONResponse(content={"result": True})

    except ApiKeyDontFind as e:
        error_text = e.text
        error_type = e.type
        logger.warning(error_type)

    except UserDontFind as e:
        error_text = e.text
        error_type = e.type
        logger.warning(error_type)

    except Exception:
        error_text = "Something wrong!"
        error_type = "Exception"
        logger.error(error_type)

    return JSONResponse(
        content={
            "result": False,
            "error_type": error_type,
            "error_message": error_text,
        }
    )


@router_users.delete("/{id}/follow", response_class=JSONResponse)
async def del_follow(
    id: int,
    api_key: str = Header(),
    db_session: AsyncSession = Depends(get_db),
):
    try:
        udal = UserDAL(db_session)
        await udal.follow(id, api_key, add=False)
        return JSONResponse(content={"result": True})

    except ApiKeyDontFind as e:
        error_text = e.text
        error_type = e.type
        logger.warning(error_type)

    except UserDontFind as e:
        error_text = e.text
        error_type = e.type
        logger.warning(error_type)

    except Exception:
        error_text = "Something wrong!"
        error_type = "Exception"
        logger.error(error_type)

    return JSONResponse(
        content={
            "result": False,
            "error_type": error_type,
            "error_message": error_text,
        }
    )


@router_users.get("/me", response_class=JSONResponse)
async def my_profile(
    api_key: str = Header(),
    db_session: AsyncSession = Depends(get_db),
    redis_cli: Redis = Depends(get_redis),
):
    try:
        response = await redis_cli.get(f"{api_key}_me")
        if response is None:
            udal = UserDAL(db_session)
            profile = await udal.get_profile(api_key)
            await redis_cli.set(
                f"{api_key}_me", json.dumps(profile, default=str), 10
            )
        else:
            profile = json.loads(response.decode("utf-8"))
        return JSONResponse(content={"result": True, "user": profile})

    except ApiKeyDontFind as e:
        error_text = e.text
        error_type = e.type
        logger.warning(error_type)

    except Exception:
        error_text = "Something wrong!"
        error_type = "Exception"
        logger.error(error_type)

    return JSONResponse(
        content={
            "result": False,
            "error_type": error_type,
            "error_message": error_text,
        }
    )


@router_users.get("/{id}", response_class=JSONResponse)
async def alien_profile(
    id: int,
    api_key: str = Header(),
    db_session: AsyncSession = Depends(get_db),
    redis_cli: Redis = Depends(get_redis),
):
    try:
        response = await redis_cli.get(f"profile_{id}")
        if response is None:
            udal = UserDAL(db_session)
            profile = await udal.get_profile(id, alien=True)
            await redis_cli.set(
                f"profile_{id}", json.dumps(profile, default=str), 10
            )
        else:
            profile = json.loads(response.decode("utf-8"))
        return JSONResponse(content={"result": True, "user": profile})

    except ApiKeyDontFind as e:
        error_text = e.text
        error_type = e.type
        logger.warning(error_type)

    except UserDontFind as e:
        error_text = e.text
        error_type = e.type
        logger.warning(error_type)

    except Exception:
        error_text = "Something wrong!"
        error_type = "Exception"
        logger.error(error_type)

    return JSONResponse(
        content={
            "result": False,
            "error_type": error_type,
            "error_message": error_text,
        }
    )
