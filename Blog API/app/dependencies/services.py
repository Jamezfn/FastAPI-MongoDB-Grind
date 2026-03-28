from fastapi import Depends

from app.services.token import TokenService
from app.services.auth import AuthService
from app.services.user import UserService
from app.services.comment import CommentService
from app.services.post import PostService
from app.repository.user.user import UserRepo
from app.repository.comment import CommentRepo
from app.repository.post import PostRepo
from app.repository.tag import TagRepo
from app.dependencies.auth import get_user_repo, get_token_service
from app.dependencies.repository import get_comment_repo, get_post_repo, get_tag_repo


def get_auth_service(
        user_repo: UserRepo = Depends(get_user_repo),
        token_service: TokenService = Depends(get_token_service)
) -> AuthService:
    return AuthService(
        user_repo=user_repo,
        token_service=token_service
    )

def get_user_service(user_repo: UserRepo = Depends(get_user_repo)) -> UserService:
    return UserService(user_repo=user_repo)

def get_post_service(
        post_repo: PostRepo = Depends(get_post_repo),
        tag_repo: TagRepo = Depends(get_tag_repo)
) -> PostService:
    return PostService(post_repo=post_repo, tag_repo=tag_repo)

def get_comment_service(
        comment_repo: CommentRepo = Depends(get_comment_repo),
        post_repo: PostRepo = Depends(get_post_repo)
) -> CommentService:
    return CommentService(comment_repo=comment_repo, post_repo=post_repo)