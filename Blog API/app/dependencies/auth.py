from beanie import PydanticObjectId
from fastapi import Header, Depends, HTTPException, status
from typing import Optional

from app.repository.token import BlacklistedTokenRepo
from app.core.security.token_manager import jwt_manager
from app.repository.user.user import UserRepo
from app.dependencies.repository import get_user_repo, get_blacklisted_token_repo
from app.models.user import User

async def _get_token_from_header(authorization: Optional[str] = Header(None)) -> Optional[str]:
    if not authorization and not authorization.startswith('Bearer'):
        return None
    
    return authorization.split(" ")[1]

async def _verify_access_token(token: Optional[str], black_listed_repo: BlacklistedTokenRepo) -> Optional[dict]:
    if not token:
        return None
    
    payload = jwt_manager.decode_token(token=token)
    if not payload or payload.get("type") != "access":
        return None
    
    if await black_listed_repo.is_blacklisted(jti=payload.get("jti")):
        return None
    
    return payload

async def get_current_user(
        token: Optional[str] = Depends(_get_token_from_header),
        user_repo: UserRepo = Depends(get_user_repo),
        blacklisted_repo: BlacklistedTokenRepo = Depends(get_blacklisted_token_repo)
):
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Authentication Credentials"
    )

    payload = await _verify_access_token(token=token, black_listed_repo=blacklisted_repo)
    if not payload:
        raise auth_exception
    
    user = await user_repo.get(PydanticObjectId(payload["sub"]))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User no longer exists.")
    
    return user
    
async def get_optional_user(
        token: Optional[str] = Depends(_get_token_from_header),
        user_repo: UserRepo = Depends(get_user_repo),
        blacklisted_repo: BlacklistedTokenRepo = Depends(get_blacklisted_token_repo)
) -> Optional[User]:
    payload = await _verify_access_token(token, blacklisted_repo)
    if not payload:
        return None
    return await user_repo.get(PydanticObjectId(payload["sub"]))

async def get_raw_token(authorization: Optional[str] = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing access token.")
    return authorization.split(" ")[1]