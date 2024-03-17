from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_
from sqlalchemy.orm.exc import FlushError
from database.models import *
from schemas import *
from exc import *
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
        return "Complete"

    async def follow(self, author_id, api_key, add=True):
        user1 = await find_user(api_key, self.db)
        user2 = await self.db.execute(select(Users).where(Users.id == author_id))
        user2 = user2.scalars().one_or_none()

        if add is True:
            user1.followed.append(user2)
        else:
            user1.followed.remove(user2)

        await self.db.commit()

    async def get_all_tweets_for_user(self, api_key):
        tweets = await self.db.execute(select(Tweets))
        tweets = tweets.scalars().all()

        tweets.sort(key=lambda x: x.tweet_date_create, reverse=True)

        tweets_ok = []
        tweets_bad = []
        for tweet in tweets:
            try:
                tweet = ListTweetsSchemas.from_orm(tweet)
                tweet = ListTweetsSchemas.dict(tweet, by_alias=False)
                tweet["attachments"] = [x["link"] for x in tweet["attachments"]]
                tweet["likes"] = [{"user_id": x["id"], "name": x["name"]} for x in tweet["likes"]]
                tweets_ok.append(tweet)

            except Exception:
                tweets_bad.append(tweet.id)

        return tweets_ok, tweets_bad

    async def get_profile(self, param, alien=False):
        if alien:
            user = await find_user(param, self.db, api_key=False)
        else:
            user = await find_user(param, self.db)

        followers = await self.db.execute(user.followers)
        followers = followers.scalars().all()

        following = await self.db.execute(user.followed)
        following = following.scalars().all()

        try:
            user = UsersSchemas.model_validate(user)
            user = UsersSchemas.model_dump(user)
        except Exception:
            return {}

        try:
            followers = [UsersSchemas.model_validate(f) for f in followers]
            followers = [UsersSchemas.model_dump(f) for f in followers]
        except Exception:
            followers = []

        try:
            following = [UsersSchemas.model_validate(f) for f in following]
            following = [UsersSchemas.model_dump(f) for f in following]
        except Exception:
            following = []

        user["followers"] = followers
        user["following"] = following

        return user


class TweetDAL:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_tweet(self, api_key, body: Tweetters):
        user = await find_user(api_key, self.db)
        new_tweet = Tweets(tweet_data=body.tweet_data, tweet_has_media=False, author=user) \
            if not body.tweet_media_ids else Tweets(tweet_data=body.tweet_data, tweet_has_media=True, author=user)
        self.db.add(new_tweet)

        if body.tweet_media_ids:
            files = await self.db.execute(select(Files).where(Files.id.in_(body.tweet_media_ids)))
            files = files.scalars().all()
            for file in files:
                renames(f"../upload_files/{file.id}{file.extension}",
                        f"../upload_files/{new_tweet.id}/{file.id}{file.extension}")
                file.tweet = new_tweet
                file.link = f"../upload_files/{new_tweet.id}/{file.id}{file.extension}"
        await self.db.commit()

        return new_tweet.id

    async def save_file(self, file, file_id, file_ext):
        try:
            async with open(f"../upload_files/{file_id}{file_ext}", "wb") as f:
                file_content = await file.read()
                await f.write(file_content)
        except Exception:
            await self.delete_files(file_id, tweet=False)
            await self.db.commit()
            raise FileDontSave

    async def add_file_to_db(self, file):
        file_ext = splitext(file.filename)[1]
        new_media = Files(name=file.filename, size=file.size, extension=file_ext)

        self.db.add(new_media)
        await self.db.commit()

        return new_media.id, file_ext

    async def delete_tweet(self, tweet_id: int, api_key: str):
        user = await find_user(api_key, self.db)

        author_id = await find_tweet(tweet_id, self.db)
        author_id = author_id.author_id

        if user.id == author_id:
            tweet = await self.db.execute(select(Tweets).where(Tweets.id == tweet_id))
            tweet = tweet.scalars().one_or_none()

            if tweet.tweet_has_media is True:
                await self.delete_files(tweet_id)
            await self.db.delete(tweet)

            await self.db.commit()
            return True

        else:
            raise FlushError

    async def delete_files(self, ids: int, tweet=True):
        if tweet:
            rmtree(f"../upload_files/{ids}")
        else:
            file = await self.db.execute(select(Files).where(Files.id == ids))
            file = file.scalars().one_or_none()
            if file is not None:
                remove(f"../upload_files/{file.id}{file.extension}")
            await self.db.execute(delete(Files).where(Files.id == ids))

    async def like(self, tweet_id: int, api_key: str, add=True):
        user = await find_user(api_key, self.db)
        tweet = await find_tweet(tweet_id, self.db)
        like_is_exist = user in tweet.likes

        if add is True:
            if like_is_exist is False:
                tweet.likes.append(user)
            else:
                raise LikeIsExist

        else:
            if like_is_exist is True:
                tweet.likes.remove(user)
            else:
                raise LikeDoesntExist

        await self.db.commit()


async def find_user(param, db: AsyncSession, api_key=True) -> int:
    if api_key:
        user = await db.execute(select(Users).where(Users.api_key == param))
    else:
        user = await db.execute(select(Users).where(Users.id == param))

    user = user.scalars().one_or_none()

    if user is None and api_key is True:
        raise ApiKeyDontFind()
    elif user is None:
        raise UserDontFind()

    return user


async def find_tweet(tweet_id: int, db: AsyncSession):
    tweet = await db.execute(select(Tweets).where(Tweets.id == tweet_id))
    tweet = tweet.scalars().one_or_none()

    if tweet is None:
        raise TweetDontFind()

    return tweet
