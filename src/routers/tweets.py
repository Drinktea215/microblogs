from fastapi import APIRouter, Header, Depends
from starlette.responses import JSONResponse
from database.db import get_db
from database.crud import *

router_tweets = APIRouter(prefix="/tweets", tags=["Tweets"])


@router_tweets.post("/", response_class=JSONResponse)
async def add_tweet(body: Tweetters, api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    tdal = TweetDAL(db_session)
    tweet_id = await tdal.create_tweet(api_key, body)
    return JSONResponse(content={"result": True, "tweet_id": tweet_id})


@router_tweets.delete("/{id}", response_class=JSONResponse)
async def del_tweet(id: int, api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    tdal = TweetDAL(db_session)
    result = await tdal.delete_tweet(id, api_key)
    return JSONResponse(content={"result": result})


@router_tweets.post("/{id}/likes")
async def add_like_tweet(id: int, api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    tdal = TweetDAL(db_session)
    await tdal.like(id, api_key, add=True)
    return {"result": True}


@router_tweets.delete("/{id}/likes")
async def del_like_tweet(id: int, api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    tdal = TweetDAL(db_session)
    await tdal.like(id, api_key, add=False)
    return {"result": True}


@router_tweets.get("/")
async def get_tweets(api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    udal = UserDAL(db_session)
    result_ok, result_bad = await udal.get_all_tweets_for_user(api_key)
    return {"result": True, "tweets": result_ok}
