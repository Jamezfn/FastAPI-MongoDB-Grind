from beanie import Document
from pydantic import Field, EmailStr
from datetime import datetime, timezone
from pymongo import IndexModel, ASCENDING

from .settings import BeanieSettingsProtocol

class User(Document):
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: bytes = Field(...)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"
        validate_on_save = True
        use_state_management = True
        keep_nulls = False
        indexes = [
            IndexModel([("username", ASCENDING)], unique=True),
            IndexModel([("email", ASCENDING)], unique=True),
        ]