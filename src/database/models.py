from __future__ import annotations
from typing import List
from .db import Base
from sqlalchemy import Column, Integer, DateTime, Boolean, String, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column, backref
from sqlalchemy.sql import func
from sqlalchemy.schema import Table, ForeignKey

assoc_table_for_likes = Table(
    "assoc_table_for_likes",
    Base.metadata,
    Column(
        "tweet_id",
        ForeignKey("tweets.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    ),
)

followers = Table(
    "followers",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id")),
    Column("followed_id", Integer, ForeignKey("users.id")),
)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, unique=True)
    name = Column(String, nullable=False)
    tweets_author: Mapped[List["Tweets"]] = relationship(
        back_populates="author"
    )

    likes_tweets: Mapped[List[Tweets]] = relationship(
        secondary=assoc_table_for_likes, back_populates="likes"
    )

    followed = relationship(
        "Users",
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=backref("followers", lazy="write_only"),
        lazy="write_only",
    )


class Tweets(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    tweet_data = Column(String, nullable=False)
    tweet_date_create = Column(
        DateTime, nullable=False, server_default=func.now()
    )
    tweet_has_media = Column(Boolean, default=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["Users"] = relationship(
        back_populates="tweets_author", lazy="selectin"
    )

    likes: Mapped[List[Users]] = relationship(
        secondary=assoc_table_for_likes,
        back_populates="likes_tweets",
        lazy="selectin",
    )
    media: Mapped[List["Files"]] = relationship(
        back_populates="tweet", cascade="all, delete", lazy="selectin"
    )


class Files(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    size = Column(Float, nullable=False)
    extension = Column(String, nullable=False)
    tweet_ids: Mapped[int] = mapped_column(
        ForeignKey("tweets.id"), nullable=True
    )
    tweet: Mapped["Tweets"] = relationship(back_populates="media")
    link = Column(String)
