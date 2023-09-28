import os
import pathlib
from typing import Annotated
import aiofiles as aiofiles
from fastapi import FastAPI, APIRouter, Response, UploadFile, File, Header, Depends
from starlette.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from database import get_db
from crud import *
from models import *

app = FastAPI(title="Clone tweetter")


@app.post("/api/tweets/", response_class=JSONResponse)
async def add_tweet(body: Tweetters, api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    tdal = TweetDAL(db_session)
    tweet_id = await tdal.create_tweet(api_key, body)
    return JSONResponse(content={"result": True, "tweet_id": tweet_id})


@app.post("/api/medias/", response_class=JSONResponse)
async def load_file(file: UploadFile = File(...), db_session: AsyncSession = Depends(get_db)):
    tdal = TweetDAL(db_session)
    file_id, file_ext = await tdal.add_file_to_db(file)
    await tdal.save_file(file, file_id, file_ext)
    return JSONResponse(content={"result": True, "media_id": file_id})


@app.delete("/api/tweets/{id}", response_class=JSONResponse)
async def del_tweet(id: int, api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    tdal = TweetDAL(db_session)
    result = await tdal.delete_tweet(id, api_key)
    return JSONResponse(content={"result": result})


@app.post("/api/tweets/{id}/likes")
async def add_like_tweet(id: int, api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    tdal = TweetDAL(db_session)
    await tdal.like(id, api_key, add=True)
    return {"result": True}


@app.delete("/api/tweets/{id}/likes")
async def del_like_tweet(id: int, api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    tdal = TweetDAL(db_session)
    await tdal.like(id, api_key, add=False)
    return {"result": True}


@app.post("/api/users/{id}/follow")
async def add_follow(id: int, api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    udal = UserDAL(db_session)
    await udal.follow(id, api_key, add=True)
    return {"result": True}


@app.delete("/api/users/{id}/follow")
async def del_follow(id: int, api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    udal = UserDAL(db_session)
    await udal.follow(id, api_key, add=False)
    return {"result": True}


@app.get("/api/tweets/")
async def get_tweets(api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    udal = UserDAL(db_session)
    result_ok, result_bad = await udal.get_all_tweets_for_user(api_key)
    return {"result": True, "tweets": result_ok}


@app.get("/api/users/me")
async def my_profile(api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    udal = UserDAL(db_session)
    profile = await udal.get_profile(api_key)
    return {"result": True, "user": profile}


@app.get("/api/users/{id}")
async def alien_profile(id: int, api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    udal = UserDAL(db_session)
    profile = await udal.get_profile(id, alien=True)
    return {"result": True, "user": profile}


@app.get("/")
async def root(api_key: str = Header(), db_session: AsyncSession = Depends(get_db)):
    # udal = UserDAL(db_session)
    # result = await udal.add_new_user(api_key)
    return {"api-key": api_key, "result": api_key}
