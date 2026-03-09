from typing import Optional
from beanie import PydanticObjectId

from ..base import BaseRepo
from .projection import UserAuthProjection
from app.models.user import User

class UserRepo(BaseRepo[User]):
    def __init__(self):
        super().__init__(model=User)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.find_one({"email": email})
    
    async def get_by_username(self, username: str) -> Optional[User]:
        return await self.find_one({"username": username})
    
    async def get_for_auth(self, email: str) -> Optional[UserAuthProjection]:
        return await self.model.find_one({"email": email}, projection_model=UserAuthProjection)
    
    async def email_exists(self, email: str) -> bool:
        return await self.find_one({"email": email}) is not None
    
    async def username_exists(self, username: str) -> bool:
        return await self.find_one({"username": username}) is not None
    
    async def update_password(self, id: PydanticObjectId, password: str) -> Optional[User]:
        return await self.update(id=id, update_data={"password": password})