from beanie import Document, PydanticObjectId, Link
from pydantic import Field
from typing import List
from datetime import datetime, timezone
from pymongo import IndexModel, ASCENDING, DESCENDING

from .tags import Tag
from .category import Category
from .settings import BeanieSettingsProtocol

class Post(Document):
    user_id: PydanticObjectId
    title: str
    body: str
    tags: List[Link[Tag]] = Field(default_factory=list)
    categories: List[Link[Category]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings(BeanieSettingsProtocol):
        name = 'posts'
        validate_on_save = True
        use_state_management = True
        keep_nulls = False
        indexes = [
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("created_at", DESCENDING)])
        ]