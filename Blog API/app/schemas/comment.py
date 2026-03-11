from pydantic import BaseModel
from beanie import PydanticObjectId
from datetime import datetime

class CreateCommentRequest(BaseModel):
    body: str


class CommentResponse(BaseModel):
    id: PydanticObjectId
    body: str
    created_at: datetime
    username: str

    model_config = {"from_attributes": True}