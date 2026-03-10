from beanie import PydanticObjectId
from datetime import datetime
from typing import List, Optional

from .base import BaseRepo
from app.models.comment import Comment

class CommentRepo(BaseRepo[Comment]):
    def __init__(self):
        super().__init__(model=Comment)

    async def get_by_post(self, post_id: PydanticObjectId, cursor: datetime, limit: int = 10) -> List[Comment]:
        """Query comments based on posts"""
        pipeline = [
            {"$match": {"post.$id": post_id}},
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user.$id",
                    "foreignField": "_id",
                    "as": "user"
                },
            },
            {"$unwind": "$user"},
            {
                "$project": {
                    "body": 1,
                    "created_at": 1,
                    "username": "user.username"
                }
            },
            {"$sort": {"created_at": -1}}
        ]

        return await self.aggregate(pipeline=pipeline, cursor_value=cursor, limit=limit)
    
    async def get_by_user(
            self, user_id: PydanticObjectId, cursor: Optional[datetime] = None, limit: int = 10,
    ) -> List[Comment]:
        """Query by user"""
        pipeline = [
            {"$match": {"user.$id": user_id}},
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user.$id",
                    "foreignField": "_id",
                    "as": "user"
                }
            },
            {"$unwind": "$user"},
            {
                "$project": {
                    "body": 1,
                    "created_at": 1,
                    "username": "$user.username"
                }
            },
            {"$sort": {"created_at": -1}}
        ]

        return await self.aggregate(pipeline=pipeline, cursor_value=cursor, limit=limit)
    
    async def delete_by_post(self, post_id: PydanticObjectId) -> int:
        """Delete all comments belonging to a post. Returns count deleted."""
        result = await self.model.find({"post.$id": post_id}).delete()
        return result.deleted_count