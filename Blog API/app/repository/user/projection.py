from pydantic import BaseModel, Field
from beanie import PydanticObjectId

class UserAuthProjection(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    username: str
    password: str