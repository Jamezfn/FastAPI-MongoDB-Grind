from fastapi import APIRouter, status, Depends, Response, Cookie, HTTPException
from typing import Optional

from app.dependencies.services import get_auth_service
from app.services.auth import AuthService
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.schemas.user import UserResponse
from app.schemas.user import UserResponse
from app.dependencies.services import get_auth_service
from app.dependencies.auth import get_current_user, get_raw_token
from app.models.user import User
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)):
    """Register/signup endpoint"""
    user = await auth_service.register(
        username=body.username,
        email=body.email,
        password=body.password
    )

    return UserResponse.model_validate(user)

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(body: LoginRequest, response: Response, auth_service: AuthService = Depends(get_auth_service)):
    """Login/sign in endpoint"""
    tokens = await auth_service.login(email=body.email, password=body.password)
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    return TokenResponse(access_token=tokens["access_token"], expires_at=tokens["expires_at"])

@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh(response: Response, refresh_token: Optional[str] = Cookie(None), auth_service: AuthService = Depends(get_auth_service)):
    """Refresh access token"""
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised")
    
    tokens = await auth_service.refresh(refresh_token=refresh_token)
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    return TokenResponse(access_token=tokens["access_token"], expires_at=tokens["expires_at"])

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response, refresh_token: Optional[str] = Cookie(None), access_token: Optional[str] = Depends(get_raw_token), current_user: User = Depends(get_current_user), auth_service: AuthService = Depends(get_auth_service)):
    """Logout user endpoint"""
    await auth_service.logout(access_token=access_token, refresh_token=refresh_token or "")
    response.delete_cookie("refresh_token")