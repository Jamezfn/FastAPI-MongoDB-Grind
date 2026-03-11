from app.repository.user.user import UserRepo
from app.repository.post import PostRepo
from app.repository.comment import CommentRepo
from app.repository.tag import TagRepo
from app.repository.token import RefreshTokenRepo, BlacklistedTokenRepo


def get_user_repo() -> UserRepo:
    return UserRepo()

def get_post_repo() -> PostRepo:
    return PostRepo()

def get_comment_repo() -> CommentRepo:
    return CommentRepo()

def get_tag_repo() -> TagRepo:
    return TagRepo()

def get_refresh_token_repo() -> RefreshTokenRepo:
    return RefreshTokenRepo()

def get_blacklisted_token_repo() -> BlacklistedTokenRepo:
    return BlacklistedTokenRepo()