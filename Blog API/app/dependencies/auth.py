from beanie import PydanticObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from app.services.token import TokenService
from app.core.security.token_manager import jwt_manager
from app.repository.user.user import UserRepo
from app.dependencies.repository import get_user_repo, get_token_service
from app.models.user import User

security = HTTPBearer(auto_error=False)

async def get_raw_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[str]:
    if not credentials:
        return None
    
    return credentials.credentials

async def _verify_access_token(token: Optional[str], token_service: TokenService) -> Optional[dict]:
    if not token:
        return None
    
    payload = jwt_manager.decode_token(token=token)
    if not payload or payload.get("type") != "access":
        return None
    
    if await token_service.is_blacklisted(jti=payload.get("jti")):
        return None
    
    return payload

async def get_current_user(
        token: Optional[str] = Depends(get_raw_token),
        user_repo: UserRepo = Depends(get_user_repo),
        token_service: TokenService = Depends(get_token_service)
):
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Authentication Credentials"
    )

    payload = await _verify_access_token(token=token, token_service=token_service)
    if not payload:
        raise auth_exception
    
    user = await user_repo.get(PydanticObjectId(payload["sub"]))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User no longer exists.")
    
    return user
    
async def get_optional_user(
        token: Optional[str] = Depends(get_raw_token),
        user_repo: UserRepo = Depends(get_user_repo),
        token_service: TokenService = Depends(get_token_service)
) -> Optional[User]:
    payload = await _verify_access_token(token, token_service)
    if not payload:
        return None
    return await user_repo.get(PydanticObjectId(payload["sub"]))