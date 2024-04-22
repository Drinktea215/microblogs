from redis.asyncio import Redis
from .config import REDIS_CLIENT, REDIS_PORT


def get_redis():
    return Redis(host=REDIS_CLIENT, port=REDIS_PORT, db=0)
