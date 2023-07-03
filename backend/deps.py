import redis
from backend.config import settings

import redis

__all__ = [
    "get_redis"
]


def create_redis():
    return redis.ConnectionPool.from_url(
        settings.BACKEND_URI
    )


pool = create_redis()


def get_redis():
    # Here, we re-use our connection pool
    # not creating a new one
    return redis.Redis(connection_pool=pool)
