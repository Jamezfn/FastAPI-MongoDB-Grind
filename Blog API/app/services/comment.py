from fastapi import HTTPException, status
from typing import Optional, List, Dict, Any
from datetime import datetime
from beanie import PydanticObjectId

from app.repository.comment import CommentRepo
from app.repository.post import PostRepo
from app.models.comment import Comment
from app.models.user import User


class CommentService:
    def __init__(self, comment_repo: CommentRepo, post_repo: PostRepo):
        self.comment_repo = comment_repo
        self.post_repo = post_repo

    async def create(self, user: User, post_id: PydanticObjectId, body: str) -> Comment:
        post = await self.post_repo.get(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not available")

        return await self.comment_repo.create({
            "post": post_id,
            "user": user.id,
            "body": body
        })

    async def delete(self, comment_id: PydanticObjectId, user: User) -> None:
        comment = await self.comment_repo.get(comment_id)
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not available")
        if comment.user.ref.id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="forbidden")
        await self.comment_repo.delete(comment_id)

    async def delete_by_post(self, post_id: PydanticObjectId) -> int:
        """Cascade delete — call this when deleting a post."""
        return await self.comment_repo.delete_by_post(post_id)

    async def get_by_post(
            self, post_id: PydanticObjectId,
            cursor: Optional[datetime] = None, limit: int = 10
    ) -> List[Comment]:
        post = await self.post_repo.get(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not available")
        return await self.comment_repo.get_by_post(
            post_id=post_id, cursor=cursor, limit=limit
        )

    async def get_by_user(
            self, user_id: PydanticObjectId,
            cursor: Optional[datetime] = None, limit: int = 10
    ) -> List[Comment]:
        return await self.comment_repo.get_by_user(
            user_id=user_id, cursor=cursor, limit=limit
        )
    
    async def get_by_post(self, post_id: PydanticObjectId, cursor: Optional[datetime] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        post = await self.post_repo.get(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not available")

        return await self.comment_repo.get_comments_by_post_aggregated(post_id=post_id, cursor=cursor, limit=limit)
    
    async def get_by_user(
        self,
        user_id: PydanticObjectId,
        cursor: Optional[datetime] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        return await self.comment_repo.get_comments_by_user_aggregated(user_id=user_id, cursor=cursor, limit=limit)