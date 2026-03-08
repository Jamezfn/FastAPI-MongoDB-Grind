from beanie import Document
from pydantic import Field
from pymongo import IndexModel, ASCENDING

from .settings import BeanieSettingsProtocol

class Category(Document):
    name: str = Field(..., unique=True)

    class Settings(BeanieSettingsProtocol):
        name = "categories"
        validate_on_save = True
        use_state_management = True
        keep_nulls = False
        indexes = [
            IndexModel([("name", ASCENDING)], unique=True)
        ]