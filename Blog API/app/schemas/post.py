from pydantic import BaseModel
from beanie import PydanticObjectId
from datetime import datetime
from typing import Optional, List

from app.models.category import Category


class CreatePostRequest(BaseModel):
    title: str
    body: str
    tag_names: List[str] = []
    category: Category


class UpdatePostRequest(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    tag_names: Optional[List[str]] = None
    category: Optional[Category] = None

    model_config = {"extra": "forbid"}


class PostSummaryResponse(BaseModel):
    """For listing posts — no body."""
    id: PydanticObjectId
    title: str
    category: Category
    created_at: datetime
    username: str
    tags: List[str]

    model_config = {"from_attributes": True}


class PostDetailResponse(BaseModel):
    """For single post view — includes body."""
    id: PydanticObjectId
    title: str
    body: str
    category: Category
    created_at: datetime
    username: str
    tags: List[str] = []

    model_config = {"from_attributes": True}