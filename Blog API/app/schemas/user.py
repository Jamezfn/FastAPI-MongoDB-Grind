from pydantic import BaseModel, EmailStr
from beanie import PydanticObjectId
from datetime import datetime
from typing import Optional


class UserResponse(BaseModel):
    id: PydanticObjectId
    username: str
    email: EmailStr
    created_at: datetime

    model_config = {"from_attributes": True}


class UpdateProfileRequest(BaseModel):
    username: Optional[str] = None

    model_config = {"extra": "forbid"} 


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str