from redis.asyncio import Redis
from beanie import PydanticObjectId
from datetime import datetime, timezone

class TokenService:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def store_refresh_token(self, user_id: PydanticObjectId, token: str, expires_at: datetime) -> None:
        """Store Refresh token"""
        user_id = str(user_id)
        ttl = int((expires_at - datetime.now(timezone.utc)).total_seconds())
        async with self.redis.pipeline() as pipe:
            await pipe.setex(f"refresh:{token}", ttl, user_id)
            await pipe.sadd(f"user_refresh_tokens:{user_id}", token)
            await pipe.expire(f"user_refresh_tokens:{user_id}", ttl)
            await pipe.execute()
    
    async def revoke_refresh_token(self, token: str) -> None:
        """Revoke token from a single device"""
        user_id = await self.redis.get(f"refresh:{token}")
        if user_id:
            async with self.redis.pipeline() as pipe:
                await pipe.delete(f"refresh:{token}")
                await pipe.srem(f"user_refresh_tokens:{user_id}", token)
                await pipe.execute()

    async def get_refresh_token_user(self, token: str) -> str | None:
        """Returns user_id if token exists, None otherwise."""
        return await self.redis.get(f"refresh:{token}")

    async def revoke_all_refresh_tokens(self, user_id: PydanticObjectId) -> None:
        """Revoke token from all devices"""
        user_id = str(user_id)
        tokens = await self.redis.smembers(f"user_refresh_tokens:{(user_id)}")
        if tokens:
            async with self.redis.pipeline() as pipe:
                for token in tokens:
                    await pipe.delete((f"refresh:{token}"))
                await pipe.delete(f"user_refresh_tokens:{user_id}")
                await pipe.execute()

    async def blacklist_access_token(self, jti: str, expires_at: datetime) -> None:
        """Blacklist an access token"""
        ttl = int((expires_at - datetime.now(timezone.utc)).total_seconds())
        if ttl > 0:
            await self.redis.setex(f"blacklist:{jti}", ttl, "1")

    async def is_blacklisted(self, jti: str) -> True:
        """Check if access token is blacklisted"""
        return await self.redis.exists(f"blacklist:{jti}") > 0