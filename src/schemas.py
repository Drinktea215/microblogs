from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class Tweetters(BaseModel):
    tweet_data: str = Field(..., max_length=100)
    tweet_media_ids: Optional[list[int]]


class UsersSchemas(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class ListTweetsSchemas(BaseModel):
    id: int
    content: str = Field(..., alias="tweet_data")
    tweet_date_create: datetime
    attachments: list[LinksFilesSchemas] = Field(..., alias="media")
    author: UsersSchemas
    likes: list[UsersSchemas]

    model_config = ConfigDict(from_attributes=True)


class LinksFilesSchemas(BaseModel):
    link: str

    model_config = ConfigDict(from_attributes=True)
