from fastapi import Depends

from app.services.auth import AuthService
from app.services.user import UserService
from app.repository.user.user import UserRepo
from app.repository.token import RefreshTokenRepo, BlacklistedTokenRepo
from app.dependencies.auth import get_user_repo, get_blacklisted_token_repo
from app.dependencies.repository import get_refresh_token_repo


def get_auth_service(
        user_repo: UserRepo = Depends(get_user_repo),
        refresh_token_repo: RefreshTokenRepo = Depends(get_refresh_token_repo),
        blacklisted_token_repo: BlacklistedTokenRepo = Depends(get_blacklisted_token_repo)
) -> AuthService:
    return AuthService(
        user_repo=user_repo,
        refresh_token_repo=refresh_token_repo,
        blacklisted_token_repo=blacklisted_token_repo
    )

def get_user_service(user_repo: UserRepo = Depends(get_user_repo)) -> UserService:
    return UserService(user_repo=user_repo)