from fastapi import HTTPException, status
from beanie import PydanticObjectId

from app.repository.user.user import UserRepo
from app.models.user import User
from app.core.security.hashing import Hash

class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def get_profile(self, user_id: PydanticObjectId) -> User:
        """Retrieve user profile"""
        user = await self.user_repo.get(id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return user
    
    async def update_profile(self, user_id: PydanticObjectId, data: dict) -> User:
        """Update profile"""
        if "username" in data:
            if await self.user_repo.username_exists(data["username"]):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username exists")
        
        user = await self.user_repo.update(id=user_id, update_data=data)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        
        return user
    
    async def change_password(
            self, user_id: PydanticObjectId,
            current_password: str, new_password: str
    ) -> None:
        """Change user password"""
        user = await self.user_repo.get(id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        
        if not Hash.verify_password(plain_password=current_password, hashed_password=user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Current password is incorrect.")
        
        await self.user_repo.update_password(id=user_id, password=new_password)