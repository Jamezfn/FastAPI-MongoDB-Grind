from fastapi import APIRouter, status, Depends, Response, Cookie

from app.dependencies.services import get_auth_service
from app.services.auth import AuthService
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.schemas.user import UserResponse
from app.schemas.user import UserResponse
from app.dependencies.services import get_auth_service
from app.dependencies.auth import get_current_user
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

@router.put("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
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