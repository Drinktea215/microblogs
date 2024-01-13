from fastapi import APIRouter, Header, Depends
from starlette.responses import JSONResponse
from database.db import get_db
from database.crud import *
from redis_client import redis_cli
import json
from exc import *

router_tweets = APIRouter(prefix="/tweets", tags=["Tweets"])


@router_tweets.post("/", response_class=JSONResponse)
async def add_tweet(body: Tweetters, api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    try:
        tdal = TweetDAL(db_session)
        tweet_id = await tdal.create_tweet(api_key, body)
        return JSONResponse(content={"result": True, "tweet_id": tweet_id})

    except ApiKeyDontFind as e:
        error = e.text

    except Exception:
        error = "Something wrong!"

    return JSONResponse(content={"result": False, "error": error})


@router_tweets.delete("/{id}", response_class=JSONResponse)
async def del_tweet(id: int, api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    try:
        print("LOOK")
        tdal = TweetDAL(db_session)
        result = await tdal.delete_tweet(id, api_key)
        return JSONResponse(content={"result": result})

    except TweetDontFind as e:
        error = e.text

    except ApiKeyDontFind as e:
        error = e.text

    except Exception:
        error = "Something wrong!"

    return JSONResponse(content={"result": False, "error": error})


@router_tweets.post("/{id}/likes", response_class=JSONResponse)
async def add_like_tweet(id: int, api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    try:
        tdal = TweetDAL(db_session)
        await tdal.like(id, api_key, add=True)
        return JSONResponse(content={"result": True})
    except TweetDontFind as e:
        error = e.text

    except ApiKeyDontFind as e:
        error = e.text

    except Exception:
        error = "Something wrong!"

    return JSONResponse(content={"result": False, "error": error})


@router_tweets.delete("/{id}/likes", response_class=JSONResponse)
async def del_like_tweet(id: int, api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    try:
        tdal = TweetDAL(db_session)
        await tdal.like(id, api_key, add=False)
        return JSONResponse(content={"result": True})

    except TweetDontFind as e:
        error = e.text

    except ApiKeyDontFind as e:
        error = e.text

    except Exception:
        error = "Something wrong!"

    return JSONResponse(content={"result": False, "error": error})


@router_tweets.get("/", response_class=JSONResponse)
async def get_tweets(api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    try:
        response = await redis_cli.get(f"{api_key}_get_tweets")
        if response is None:
            udal = UserDAL(db_session)
            result_ok, result_bad = await udal.get_all_tweets_for_user(api_key)
            await redis_cli.set(f"{api_key}_get_tweets", json.dumps(result_ok), 10)
        else:
            result_ok = json.loads(response.decode("utf-8"))
        return JSONResponse(content={"result": True, "tweets": result_ok})

    except ApiKeyDontFind as e:
        error = e.text

    except Exception:
        error = "Something wrong!"

    return JSONResponse(content={"result": False, "error": error})
