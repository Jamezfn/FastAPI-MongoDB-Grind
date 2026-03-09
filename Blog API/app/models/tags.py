from beanie import Document
from pydantic import Field
from pymongo import IndexModel, ASCENDING

from .settings import BeanieSettingsProtocol

class Tag(Document):
    name: str = Field(...)

    class Settings:
        name ="tags"
        validate_on_save = True
        use_state_management = True
        keep_nulls = False
        indexes = [IndexModel([("name", ASCENDING)], unique=True)]