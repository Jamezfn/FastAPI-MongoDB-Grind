from beanie import Document, Link
from pydantic import Field
from datetime import datetime, timezone
from pymongo import IndexModel, ASCENDING, DESCENDING

from .settings import BeanieSettingsProtocol
from .user import User
from .post import Post


class Comment(Document):
    post: Link[Post]
    user: Link[User]
    body: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings():
        name = "comments"
        indexes = [
            IndexModel([("post.$id", ASCENDING), ("created_at", DESCENDING)]),
            IndexModel([("user.$id", ASCENDING), ("created_at", DESCENDING)])
        ]