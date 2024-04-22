from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm.exc import FlushError
from typing import Union
from database.models import *
from schemas import *
from exc import *
from logger import logger
from aiofiles import open
from os.path import splitext
from os import renames, remove
from shutil import rmtree


class UserDAL:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_new_user(self, name, api_key):
        new_user = Users(name=name, api_key=api_key)
        self.db.add(new_user)
        await self.db.commit()
        logger.info(f"Add new user - {name}, id = {new_user.id}")
        return "Complete"

    async def follow(self, author_id, api_key, add=True):
        logger.info(f"follow() {author_id}, add={add}")
        user1 = await find_user(api_key, self.db)
        user2 = await self.db.execute(
            select(Users).where(Users.id == author_id)
        )
        user2 = user2.scalars().one_or_none()

        if user2 is None:
            raise UserDontFind

        if add is True:
            user1.followed.add(user2)
            logger.info(f"{user1.id} add followed {user2.id}")
        else:
            user1.followed.remove(user2)
            logger.info(f"{user1.id} remove followed {user2.id}")

        await self.db.commit()

    async def get_all_tweets_for_user(self):
        logger.info("get_all_tweets_for_user()")
        tweets = await self.db.execute(select(Tweets))
        tweets = tweets.scalars().all()

        tweets.sort(key=lambda x: x.tweet_date_create, reverse=True)
        logger.info("received all tweets from db")

        tweets_ok = []
        tweets_bad = []
        for tweet in tweets:
            try:
                tweet = ListTweetsSchemas.model_validate(tweet)
                tweet = ListTweetsSchemas.model_dump(tweet, by_alias=False)
                tweet["attachments"] = [
                    x["link"] for x in tweet["attachments"]
                ]
                tweet["likes"] = [
                    {"user_id": x["id"], "name": x["name"]}
                    for x in tweet["likes"]
                ]
                tweets_ok.append(tweet)

            except Exception:
                tweets_bad.append(tweet.id)
                logger.warn("Bad tweet")

        return tweets_ok, tweets_bad

    async def get_profile(self, param, alien=False):
        logger.info("get_profile()")
        if alien:
            user = await find_user(param, self.db, api_key=False)
        else:
            user = await find_user(param, self.db)
        logger.info(f"user_id = {user.id}")

        followers = await self.db.execute(user.followers.select())
        followers = followers.scalars().all()
        logger.info(f"get followers user_id = {user.id}")

        following = await self.db.execute(user.followed.select())
        following = following.scalars().all()
        logger.info(f"get following user_id = {user.id}")

        try:
            user = UsersSchemas.model_validate(user)
            user = UsersSchemas.model_dump(user)
        except Exception:
            logger.error(f"user_id = {user.id} don't validated")
            return {}

        try:
            followers = [UsersSchemas.model_validate(f) for f in followers]
            followers = [UsersSchemas.model_dump(f) for f in followers]
        except Exception:
            logger.error(f"followers user_id = {user.id} don't validated")
            followers = []

        try:
            following = [UsersSchemas.model_validate(f) for f in following]
            following = [UsersSchemas.model_dump(f) for f in following]
        except Exception:
            logger.error(f"following user_id = {user.id} don't validated")
            following = []

        user["followers"] = followers
        user["following"] = following

        return user


class TweetDAL:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_tweet(self, api_key, body: Tweetters):
        logger.info("create_tweet()")
        user = await find_user(api_key, self.db)
        new_tweet = (
            Tweets(
                tweet_data=body.tweet_data, tweet_has_media=False, author=user
            )
            if not body.tweet_media_ids
            else Tweets(
                tweet_data=body.tweet_data, tweet_has_media=True, author=user
            )
        )
        logger.info(
            f"New tweet user_id = {user.id}, tweet_data = {new_tweet.tweet_data}, tweet_has_media = {new_tweet.tweet_has_media}"
        )
        self.db.add(new_tweet)

        if body.tweet_media_ids:
            files = await self.db.execute(
                select(Files).where(Files.id.in_(body.tweet_media_ids))
            )
            files = files.scalars().all()
            for file in files:
                renames(
                    f"../upload_files/{file.id}{file.extension}",
                    f"../upload_files/{new_tweet.id}/{file.id}{file.extension}",
                )
                file.tweet = new_tweet
                file.link = (
                    f"../upload_files/{new_tweet.id}/{file.id}{file.extension}"
                )
        await self.db.commit()
        logger.info(f"Tweet {new_tweet.id} created")

        return new_tweet.id

    async def save_file(self, file, file_id, file_ext):
        logger.info("save_file()")
        try:
            async with open(f"../upload_files/{file_id}{file_ext}", "wb") as f:
                file_content = await file.read()
                await f.write(file_content)
                logger.info(f"File {file_id} saved")
        except Exception:
            await self.delete_files(file_id, tweet=False)
            await self.db.commit()
            logger.info(f"File {file_id} don't saved")
            raise FileDontSave

    async def add_file_to_db(self, file):
        logger.info("add_file_to_db()")
        file_ext = splitext(file.filename)[1]
        new_media = Files(
            name=file.filename, size=file.size, extension=file_ext
        )

        self.db.add(new_media)
        await self.db.commit()
        logger.info(f"File {new_media.id} was added to db")

        return new_media.id, file_ext

    async def delete_tweet(self, tweet_id: int, api_key: str):
        logger.info("delete_tweet()")
        user = await find_user(api_key, self.db)

        author_id = await find_tweet(tweet_id, self.db)
        author_id = author_id.author_id

        if user.id == author_id:
            logger.info("user_id = author_id")
            tweet = await self.db.execute(
                select(Tweets).where(Tweets.id == tweet_id)
            )
            tweet = tweet.scalars().one_or_none()

            if tweet.tweet_has_media is True:
                await self.delete_files(tweet_id)
            await self.db.delete(tweet)

            await self.db.commit()
            logger.info(f"Tweet {tweet_id} was deleted")
            return True

        else:
            raise FlushError

    async def delete_files(self, ids: int, tweet=True):
        logger.info("delete_files()")
        if tweet:
            rmtree(f"../upload_files/{ids}")
            logger.info(f"Directory with files for tweet {ids} was deleted")
        else:
            file = await self.db.execute(select(Files).where(Files.id == ids))
            file = file.scalars().one_or_none()
            if file is not None:
                remove(f"../upload_files/{file.id}{file.extension}")
            await self.db.execute(delete(Files).where(Files.id == ids))
            logger.info(f"File {ids} was deleted")

    async def like(self, tweet_id: int, api_key: str, add=True):
        logger.info("like()")
        user = await find_user(api_key, self.db)
        tweet = await find_tweet(tweet_id, self.db)
        like_is_exist = user in tweet.likes

        if add is True:
            logger.info("Like add")
            if like_is_exist is False:
                logger.info("Like don't exist")
                tweet.likes.append(user)
                logger.info("Like added")
            else:
                logger.info("Like exist")
                raise LikeIsExist

        else:
            logger.info("Like delete")
            if like_is_exist is True:
                logger.info("Like exist")
                tweet.likes.remove(user)
                logger.info("Like deleted")
            else:
                logger.info("Like don't exist")
                raise LikeDoesntExist

        await self.db.commit()


async def find_user(
    param: Union[int, str], db: AsyncSession, api_key=True
) -> Users:
    if api_key:
        logger.info("Find user on api-key")
        user = await db.execute(select(Users).where(Users.api_key == param))
    else:
        logger.info("Find user on user_id")
        user = await db.execute(select(Users).where(Users.id == param))

    user = user.scalars().one_or_none()

    if user is None and api_key is True:
        logger.info("Api-Key don't find")
        raise ApiKeyDontFind
    elif user is None:
        logger.info("User don't find")
        raise UserDontFind

    logger.info("User find")

    return user


async def find_tweet(tweet_id: int, db: AsyncSession) -> Tweets:
    logger.info("Find tweet on tweet_id")
    tweet = await db.execute(select(Tweets).where(Tweets.id == tweet_id))
    tweet = tweet.scalars().one_or_none()

    if tweet is None:
        logger.info("Tweet don't find")
        raise TweetDontFind

    logger.info("Tweet find")

    return tweet
