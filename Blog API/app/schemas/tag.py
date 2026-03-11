from pydantic import BaseModel
from beanie import PydanticObjectId


class CreateTagRequest(BaseModel):
    name: str


class TagResponse(BaseModel):
    id: PydanticObjectId
    name: str

    model_config = {"from_attributes": True}