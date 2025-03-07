import redis.asyncio as redis
from core.config import settings


redis_client = redis.Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    decode_responses=True,
)

async def get_redis_client() -> redis.Redis:
    return redis_client
