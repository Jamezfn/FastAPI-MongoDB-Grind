from beanie import Document, PydanticObjectId
from pydantic import Field
from datetime import datetime, timezone
from pymongo import IndexModel, ASCENDING, DESCENDING

from .settings import BeanieSettingsProtocol


class Comment(Document):
    post_id: PydanticObjectId
    user_id: PydanticObjectId
    body: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings(BeanieSettingsProtocol):
        name = "comments"
        indexes = [
            IndexModel([("post_id", ASCENDING), ("created_at", DESCENDING)]),
            IndexModel([("user_id", ASCENDING), ("created_at", DESCENDING)])
        ]