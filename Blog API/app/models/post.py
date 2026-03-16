from beanie import Document, Link
from pydantic import Field
from typing import List
from datetime import datetime, timezone
from pymongo import IndexModel, ASCENDING, DESCENDING, TEXT

from .tags import Tag
from .user import User
from .category import Category
from .settings import BeanieSettingsProtocol

class Post(Document):
    user: Link[User] 
    title: str
    body: str
    tags: List[Link[Tag]] = Field(default_factory=list)
    categories: Category
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = 'posts'
        validate_on_save = True
        use_state_management = True
        keep_nulls = False
        indexes = [
            IndexModel([("user.$id", ASCENDING)]),
            IndexModel([("created_at", DESCENDING)]),
            IndexModel([("title", TEXT), ("body", TEXT)])
        ]