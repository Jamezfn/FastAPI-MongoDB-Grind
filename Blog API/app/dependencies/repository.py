from redis.asyncio import Redis
from fastapi import Depends

from app.core.redis import get_redis
from app.services.token import TokenService
from app.repository.user.user import UserRepo
from app.repository.post import PostRepo
from app.repository.comment import CommentRepo
from app.repository.tag import TagRepo


def get_user_repo() -> UserRepo:
    return UserRepo()

def get_post_repo() -> PostRepo:
    return PostRepo()

def get_comment_repo() -> CommentRepo:
    return CommentRepo()

def get_tag_repo() -> TagRepo:
    return TagRepo()

async def get_token_service(redis: Redis = Depends(get_redis)) -> TokenService:
    return TokenService(redis=redis)