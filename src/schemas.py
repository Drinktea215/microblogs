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
        from_attributes = True


class ListTweetsSchemas(BaseModel):
    id: int
    content: str = Field(..., alias='tweet_data')
    tweet_date_create: datetime
    attachments: list[LinksFilesSchemas] = Field(..., alias='media')
    author: UsersSchemas
    likes_users: list[UsersSchemas]

    class Config:
        from_attributes = True


class LinksFilesSchemas(BaseModel):
    link: str

    class Config:
        from_attributes = True


ListTweetsSchemas.model_rebuild()
