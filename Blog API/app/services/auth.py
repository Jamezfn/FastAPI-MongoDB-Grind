from fastapi import HTTPException, status
from datetime import datetime, timezone

from app.models.user import User
from app.repository.user.user import UserRepo
from app.services.token import TokenService
from app.core.security.hashing import Hash
from app.core.security.token_manager import jwt_manager

class AuthService:
    def __init__(self, user_repo: UserRepo, token_service: TokenService):
        self.user_repo = user_repo
        self.token_service = token_service

    async def register(self, username: str, email: str, password: str) -> User:
        """User registration service"""
        if await self.user_repo.email_exists(email=email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email already exists")
        if await self.user_repo.username_exists(username=username):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username already exists")
        
        return await self.user_repo.create({
            "username": username,
            "email": email,
            "password": Hash.hash_password(plain_password=password)
        })
    
    async def login(self, email: str, password: str) -> dict:
        """Login user and grand authorization"""
        user = await self.user_repo.get_for_auth(email=email)
        if not user or not Hash.verify_password(plain_password=password, hashed_password=user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")
        
        access_token, _, access_expires = jwt_manager.create_access_token(user_id=str(user.id))
        refresh_token, _, refresh_expires = jwt_manager.create_refresh_token(str(user.id))

        await self.token_service.store_refresh_token(
            user_id=user.id,
            token=refresh_token,
            expires_at=refresh_expires
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": access_expires
        }
    
    async def refresh(self, refresh_token: str) -> dict:
        """Get refresh token"""
        user_id = await self.token_service.get_refresh_token_user(token=refresh_token)
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token.")
        
        payload = jwt_manager.decode_token(token=refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token.")
        
        await self.token_service.revoke_refresh_token(token=refresh_token)

        access_token, _, access_expires = jwt_manager.create_access_token(payload["sub"])
        new_refresh_token, _, refresh_expires = jwt_manager.create_refresh_token(payload["sub"])


        await self.token_service.store_refresh_token(
            user_id=user_id,
            token=refresh_token,
            expires_at=refresh_expires
        )

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "expires_at": access_expires
        }
    
    async def logout(self, access_token: str, refresh_token: str) -> None:
        """Blacklist access token and revoke refresh token"""
        payload = jwt_manager.decode_token(token=access_token)
        if payload:
            await self.token_service.blacklist_access_token(
                jti=payload["jti"],
                expires_at=datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
            )

        await self.token_service.revoke_refresh_token(token=refresh_token)