from typing import Optional, List

from .base import BaseRepo
from app.models.tags import Tag

class TagRepo(BaseRepo[Tag]):
    def __init__(self):
        super().__init__(model=Tag)

    async def get_by_name(self, name: str) -> Optional[Tag]:
        return await self.find_one({"name": name})

    async def get_many_by_names(self, names: List[str]) -> List[Tag]:
        return await self.model.find({"name": {"$in": names}}).to_list()

    async def name_exists(self, name: str) -> bool:
        return await self.model.find({"name": name}).count() > 0