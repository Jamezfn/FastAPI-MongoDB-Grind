from fastapi import HTTPException, status
from datetime import datetime, timezone

from app.models.user import User
from app.repository.user.user import UserRepo
from app.repository.token import RefreshTokenRepo, BlacklistedTokenRepo
from app.core.security.hashing import Hash
from app.core.security.token_manager import jwt_manager

class AuthService:
    def __init__(self, user_repo: UserRepo, refresh_token_repo: RefreshTokenRepo, blacklisted_token_repo: BlacklistedTokenRepo):
        self.user_repo = user_repo
        self.refresh_token_repo = refresh_token_repo
        self.blacklisted_token_repo = blacklisted_token_repo

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
        if not user or not Hash.verify_password(plain_password=password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")
        
        access_token, _, access_expires = jwt_manager.create_access_token(user_id=str(user.id))
        refresh_token, _, refresh_expires = jwt_manager.create_refresh_token(str(user.id))

        await self.refresh_token_repo.create({
            "user": user.id,
            "token": refresh_token,
            "expires_at": refresh_expires
        })

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": access_expires
        }
    
    async def refresh(self, refresh_token: str) -> dict:
        """Get refresh token"""
        stored = await self.refresh_token_repo.get_by_token(token=refresh_token)
        if not stored:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token.")
        
        if stored.expires_at < datetime.now(timezone.utc):
            await stored.delete()
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired.")
        
        payload = jwt_manager.decode_token(token=refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token.")
        
        await stored.delete()
        access_token, _, access_expires = jwt_manager.create_access_token(payload["sub"])
        new_refresh_token, _, refresh_expires = jwt_manager.create_refresh_token(payload["sub"])

        await self.refresh_token_repo.create({
            "user": payload["sub"],
            "token": new_refresh_token,
            "expires_at": refresh_expires
        })

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "expires_at": access_expires
        }
    
    async def logout(self, access_token: str, refresh_token: str) -> None:
        """Blacklist access token and revoke refresh token"""
        payload = jwt_manager.decode_token(token=access_token)
        if payload:
            await self.blacklisted_token_repo.blacklist(
                jti=payload["jti"],
                expires_at=datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
            )

        await self.refresh_token_repo.revoke(refresh_token)