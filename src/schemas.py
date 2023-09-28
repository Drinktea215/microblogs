from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class Tweetters(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[list[int]]


class UsersSchemas(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ListTweetsSchemas(BaseModel):
    id: int
    content: str = Field(..., alias='tweet_data')
    tweet_date_create: datetime
    attachments: list[LinksFilesSchemas] = Field(..., alias='media')
    author: UsersSchemas
    likes_users: list[UsersSchemas]

    class Config:
        orm_mode = True


class LinksFilesSchemas(BaseModel):
    link: str

    class Config:
        orm_mode = True


ListTweetsSchemas.update_forward_refs()
