from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from datetime import datetime
from typing import Optional

class CreateCommentRequest(BaseModel):
    body: str


class CommentResponse(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    post_id: Optional[PydanticObjectId] = None
    user_id: Optional[PydanticObjectId] = None
    body: str
    created_at: datetime
    username: str

    model_config = {"from_attributes": True, "populate_by_name": True}