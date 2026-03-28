from redis.asyncio import Redis
from typing import Optional

from app.config import settings

redis_client: Optional[Redis] = None

async def init_redis() -> None:
    """Initialise redis"""
    global redis_client
    redis_client = Redis.from_url(settings.redis_url, decode_responses=True)

async def get_redis() -> Redis:
    """Get redis client"""
    return redis_client

async def close_redis() -> None:
    """Close connection"""
    if redis_client:
        await redis_client.aclose()