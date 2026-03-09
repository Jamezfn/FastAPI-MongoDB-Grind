from typing import Optional, List
from beanie import PydanticObjectId
from datetime import datetime

from .base import BaseRepo
from app.models.post import Post

class PostRepo(BaseRepo[Post]):
    def __init__(self):
        super().__init__(model=Post)

    async def get_posts_by_user(
            self, user_id: PydanticObjectId, cursor: Optional[datetime] = None,
            limit: int = 10, fetch_links: bool = False
    ) -> List[Post]:
        """Get post based on user"""
        filters = {"user.$id": user_id}
        
        return await self.find_with_cursor(filters=filters, cursor_value=cursor, sort=[("created_at", -1)], limit=limit, fetch_links=fetch_links)
    
    async def get_by_tag(
            self, tag_id: PydanticObjectId, cursor: Optional[datetime] = None,
            limit: int = 10, fetch_links: bool = False
     ) -> List[Post]:
        """Get post based on tag"""
        filters = {"tags.$id": tag_id}

        return await self.find_with_cursor(filters=filters, cursor_value=cursor, sort=[("created_at", -1)], limit=limit, fetch_links=fetch_links)
        
    async def get_by_category(
            self, category_id: PydanticObjectId, cursor: Optional[datetime] = None,
            limit: int = 10, fetch_links: bool = False
    ) -> List[Post]:
        """Get post based on category"""
        filters = {"categories.$id": category_id}

        return await self.find_with_cursor(filters=filters, cursor_value=cursor, sort=[("created_at", -1)], limit=limit, fetch_links=fetch_links)
    
    async def get_by_tag_or_category(
            self, tag_ids: Optional[List[PydanticObjectId]] = None,
            category_ids: Optional[List[PydanticObjectId]] = None,
            cursor: Optional[datetime] = None,
            limit: int = 10, fetch_links: bool = False
    ) -> List[Post]:
        """Get post based on tag and category"""
        or_conditions = []
        if tag_ids:
            or_conditions.append({"tags.$id": {"$in": tag_ids}})
        if category_ids:
            or_conditions.append({"categories.$id": {"$in": category_ids}})

        filters = {"$or": or_conditions} if or_conditions else {}

        return await self.find_with_cursor(filters=filters, cursor_value=cursor, sort=[("created_at", -1)], limit=limit, fetch_links=fetch_links)

    async def search(
            self, query: str, cursor: Optional[datetime] = None,
            limit: int = 10, fetch_links: bool = False
    ) -> List[Post]:
        """Search"""
        filters = {"$text": {"$search": query}}

        return await self.find_with_cursor(filters=filters, cursor_value=cursor, sort=[("created_at", -1)], limit=limit, fetch_links=fetch_links)