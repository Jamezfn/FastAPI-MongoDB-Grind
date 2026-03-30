from fastapi import Request, Response

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

import time
from redis.asyncio import Redis

from app.core.redis import get_redis
from app.core.security.token_manager import jwt_manager

RATE_LIMIT_RULES = {
    "/api/v1/auth/login": (5, 0.1),
    "/api/v1/auth/register": (3, 0.05),
    "/api/v1/posts/": (10, 0.5),
    "global": (100, 2)
}

def _get_rule(path:str, method: str) -> tuple[float, float]:
    """Match path to token bucket rule. Falls back to global."""
    for prefix, limits in RATE_LIMIT_RULES.items():
        if prefix == "global":
            continue
        if path.startswith(prefix):
            if prefix == "/api/v1/posts/" and method != "POST":
                continue
        
        return limits
    return RATE_LIMIT_RULES["global"]

def _get_identifier(request: Request) -> str:
    """Use user ID if authenticated, fall back to IP."""
    auth = request.headers.get("Authorisation", "")
    if auth.startswith("Bearer "):
        payload = jwt_manager.decode_token(auth.split(" ")[1])
        if payload and payload.get("sub"):
            return f"user:{payload['sub']}"
        
    forwarded = request.headers.get("X-Forwarded-For")
    ip = forwarded .split(",")[0] if forwarded else request.client.host
    return f"ip:{ip}"

async def _consume_token(redis: Redis, key: str, capacity: float, refill_rate: float) -> tuple[bool, float]:
    """Token bucket algorithm."""
    now = time.time()

    async with redis.pipeline() as pipe:
        pipe.hgetall(key)
        result = await pipe.execute()
    
    bucket = result[0]

    if bucket:
        tokens = float(
            bucket[b"tokens"] if b"tokens" in bucket else bucket["tokens"]
        )
        last_refill = float(
            bucket[b"last_refill"] if b"last_refill" in bucket else bucket["last_refill"]
        )

        elapsed = now - last_refill
        tokens = min(capacity, tokens + elapsed * refill_rate)
    else:
        tokens = capacity
        last_refill = now

    
    if tokens < 1:
        return True, 0.0
    
    tokens -= 1

    async with redis.pipeline() as pipe:
        await pipe.hset(key, mapping={"tokens": tokens, "last_refill": now})
        await pipe.expire(key, int(capacity / refill_rate) * 2)
        await pipe.execute()

    return False, tokens

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        redis: Redis = await get_redis()
        path = request.url.path
        method = request.method

        if not path.startswith("/api/"):
            return await call_next(request)
        
        capacity, refill_rate = _get_rule(path, method)
        identifier = _get_identifier(request)
        key = f"rate_limit:{identifier}:{path}"

        is_limited, remaining = await _consume_token(redis, key, capacity, refill_rate)

        if is_limited:
            retry_after = int(1 / refill_rate)
            return JSONResponse(
                status_code=429,
                content={
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": "Too many requests. Please try again later.",
                    "details": None
                },
                headers={"Retry-After": str(retry_after)}
            )
        
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(int(capacity))
        response.headers["X-RateLimit-Remaining"] = str(int(remaining))
        return response

