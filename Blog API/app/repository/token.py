from typing import Optional
from datetime import datetime, timezone
from beanie import PydanticObjectId

from .base import BaseRepo
from app.models.token import RefreshToken, BlacklistedToken

class RefreshTokenRepo(BaseRepo[RefreshToken]):
    def __init__(self):
        super().__init__(model=RefreshToken)

    async def get_by_token(self, token: str) -> Optional[RefreshToken]:
        return await self.find({"token": token})
    
    async def revoke(self, token: str) -> bool:
        return await self.delete({"token": token})
    
    async def revoke_all_for_user(self, user_id: PydanticObjectId) -> int:
        return await self.delete_get_count({"user.$id": user_id})
    
class BlacklistedTokenRepo(BaseRepo[BlacklistedToken]):
    def __init__(self):
        super().__init__(model=BlacklistedToken)

    async def blacklist(self, jti: str, expires_at: datetime) -> None:
        await self.create({"jti": jti, "expires_at": expires_at})

    async def is_blacklisted(self, jti: str) -> bool:
        return await self.model.find({"jti": jti}).count() > 0