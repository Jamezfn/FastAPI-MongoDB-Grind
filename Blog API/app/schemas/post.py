from pydantic import BaseModel, field_validator, Field
from beanie import PydanticObjectId
from datetime import datetime
from typing import Optional, List

from app.models.category import Category
from app.schemas.user import UserResponse
from app.schemas.tag import TagResponse


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
    id: PydanticObjectId = Field(alias="_id")
    title: str
    body: str
    categories: Category
    created_at: datetime
    username: str
    tags: List[str] = []

    model_config = {"from_attributes": True}