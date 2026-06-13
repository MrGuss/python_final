import redis.asyncio as redis

from app.core.config import settings


def get_redis() -> redis.Redis:
    client = redis.from_url(settings.redis_url)
    return client
