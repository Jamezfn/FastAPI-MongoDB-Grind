from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from beanie import PydanticObjectId
from datetime import datetime

from app.repository.post import PostRepo
from app.repository.tag import TagRepo
from app.models.user import User
from app.models.category import Category
from app.models.post import Post

class PostService:
    def __init__(self, post_repo: PostRepo, tag_repo: TagRepo):
        self.post_repo = post_repo
        self.tag_repo = tag_repo

    async def create(
            self, user: User, title: str, body: str, tag_names: List[str], category: Category
    ) -> Post:
        """Create post"""
        normalized = list({name.strip().lower() for name in tag_names})
        existing_tags = await self.tag_repo.get_many_by_names(normalized)

        found_names = {t.name for t in existing_tags}
        missing = [n for n in normalized if n not in found_names]
        
        new_tags = []
        for name in missing:
            tag = await self.tag_repo.create({"name": name})
            new_tags.append(tag)

        tags = existing_tags + new_tags

        return await self.post_repo.create_post({
            "user": user.id,
            "title": title,
            "body": body,
            "tags": [t.id for t in tags],
            "categories": category
        })
    
    async def get_post(self, post_id: PydanticObjectId):
        """get post by id"""
        return await self.post_repo.get_post_with_relations(post_id=post_id)
    
    async def update(self, post_id: PydanticObjectId, user: User, data: dict) -> Post:
        """Update post"""
        post = await self.post_repo.get(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
        if post.user.ref.id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        
        if "tag_names" in data:
            tags = await self.tag_repo.get_many_by_names(data.pop("tag_names"))
            data["tags"] = [t.id for t in tags]

        updated = await self.post_repo.update(post_id, data)
        return updated
    
    async def delete(self, post_id: PydanticObjectId, user: User) -> None:
        """Delete post"""
        post = await self.post_repo.get(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if post.user.ref.id != user.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="forbidden")
        
        await self.post_repo.delete({"_id": post_id})

    async def get_by_user(self, user_id: PydanticObjectId, cursor: Optional[datetime] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        return await self.post_repo.get_posts_by_user_aggregated(user_id=user_id, cursor=cursor, limit=limit)
    
    async def get_by_tag(self, tag_id: PydanticObjectId, cursor: Optional[datetime] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        return await self.post_repo.get_posts_by_tag_aggregated(tag_id=tag_id, cursor=cursor, limit=limit)
    
    async def get_by_category(self, category: Category, cursor: Optional[datetime] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Return posts in a given category with only the fields we need."""
        return await self.post_repo.get_posts_by_category_aggregated(category=category, cursor=cursor, limit=limit)
    
    async def get_by_tag_or_category(
            self, tag_ids: Optional[List[PydanticObjectId]] = None, categories: Optional[List[Category]] = None,
            cursor: Optional[datetime] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Fetch posts by tags OR categories, returning only needed fields."""
        return await self.post_repo.get_posts_by_tag_or_category_aggregated(
            tag_ids=tag_ids, categories=categories, cursor=cursor, limit=limit)
    
    async def search(
        self, query: str,
        cursor: Optional[datetime] = None, limit: int = 10
    ) -> List[Post]:
        return await self.post_repo.search(query=query, cursor=cursor, limit=limit)