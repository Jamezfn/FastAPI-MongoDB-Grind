from beanie import Document, Link
from pydantic import Field
from datetime import datetime, timezone
from pymongo import IndexModel, ASCENDING

from .user import User


class RefreshToken(Document):
    user: Link[User]
    token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "refresh_tokens"
        indexes = [
            IndexModel([("token", ASCENDING)], unique=True),
            IndexModel([("user.$id", ASCENDING)]),
            IndexModel([("expires_at", ASCENDING)], expireAfterSeconds=0)
        ]


class BlacklistedToken(Document):
    jti: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "blacklisted_tokens"
        indexes = [
            IndexModel([("jti", ASCENDING)], unique=True),
            IndexModel([("expires_at", ASCENDING)], expireAfterSeconds=0)
        ]