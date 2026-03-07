from redis.asyncio import Redis


def get_redis_client(redis: Redis) -> Redis:
    return redis
