from fastapi import APIRouter, Header, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from database.db import get_db
from database.crud import *
from database.redis_client import get_redis
from redis.asyncio import Redis
from logger import logger
from exc import *
import json

router_tweets = APIRouter(prefix="/tweets", tags=["Tweets"])


@router_tweets.post("/", response_class=JSONResponse)
async def add_tweet(
    body: Tweetters,
    api_key: str = Header(),
    db_session: AsyncSession = Depends(get_db),
):
    logger.info(f"add_tweet: {body}")
    try:
        tdal = TweetDAL(db_session)
        tweet_id = await tdal.create_tweet(api_key, body)
        return JSONResponse(content={"result": True, "tweet_id": tweet_id})

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


@router_tweets.delete("/{id}", response_class=JSONResponse)
async def del_tweet(
    id: int,
    api_key: str = Header(),
    db_session: AsyncSession = Depends(get_db),
):
    try:
        tdal = TweetDAL(db_session)
        result = await tdal.delete_tweet(id, api_key)
        return JSONResponse(content={"result": result})

    except TweetDontFind as e:
        error_text = e.text
        error_type = e.type
        logger.warning(error_type)

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


@router_tweets.post("/{id}/likes", response_class=JSONResponse)
async def add_like_tweet(
    id: int,
    api_key: str = Header(),
    db_session: AsyncSession = Depends(get_db),
):
    try:
        tdal = TweetDAL(db_session)
        await tdal.like(id, api_key, add=True)
        return JSONResponse(content={"result": True})

    except TweetDontFind as e:
        error_text = e.text
        error_type = e.type
        logger.warning(error_type)

    except LikeIsExist as e:
        error_text = e.text
        error_type = e.type
        logger.warning(error_type)

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


@router_tweets.delete("/{id}/likes", response_class=JSONResponse)
async def del_like_tweet(
    id: int,
    api_key: str = Header(),
    db_session: AsyncSession = Depends(get_db),
):
    try:
        tdal = TweetDAL(db_session)
        await tdal.like(id, api_key, add=False)
        return JSONResponse(content={"result": True})

    except TweetDontFind as e:
        error_text = e.text
        error_type = e.type
        logger.warning(error_type)

    except LikeDoesntExist as e:
        error_text = e.text
        error_type = e.type
        logger.warning(error_type)

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


@router_tweets.get("/", response_class=JSONResponse)
async def get_tweets(
    api_key: str = Header(),
    db_session: AsyncSession = Depends(get_db),
    redis_cli: Redis = Depends(get_redis),
):
    try:
        response = await redis_cli.get(f"{api_key}_get_tweets")
        if response is None:
            udal = UserDAL(db_session)
            result_ok, result_bad = await udal.get_all_tweets_for_user()
            await redis_cli.set(
                f"{api_key}_get_tweets", json.dumps(result_ok, default=str), 10
            )
        else:
            result_ok = json.loads(response.decode("utf-8"))
        return JSONResponse(
            content={"result": True, "tweets": jsonable_encoder(result_ok)}
        )

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
