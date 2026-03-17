from beanie import PydanticObjectId
from datetime import datetime
from typing import List, Dict, Any

from .base import BaseRepo
from app.models.comment import Comment

class CommentRepo(BaseRepo[Comment]):
    def __init__(self):
        super().__init__(model=Comment)
    
    async def create_comment(self, data: Dict[str, Any]) -> Comment:
        """create comment"""
        comment = await self.create(data=data)

        pipeline = [
            {"$match": {"_id": comment.id}},
            {
                "$lookup": {
                    "from": "posts",
                    "localField": "post.$id",
                    "foreignField": "_id",
                    "as": "post"
                }
            },
            {"$unwind": "$post"},
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
                    "_id": 1,
                    "post_id": "$post._id",
                    "username": "$user.username",
                    "body": 1,
                    "created_at": 1
                }
            }
        ]

        result = await self.aggregate(pipeline)
        return result[0]
    
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
                }
            },
            {"$unwind": "$user"},
            {
                "$lookup": {
                    "from": "posts",
                    "localField": "post.$id",
                    "foreignField": "_id",
                    "as": "post"
                }
            },
            {"$unwind": "$post"},
            {
                "$project": {
                    "_id": 1,
                    "username": "$user.username",
                    "user_id": "$user._id",
                    "post_id": "$post._id",
                    "body": 1,
                    "created_at": 1
                }
            }
        ]

        return await self.aggregate(pipeline=pipeline, cursor_value=cursor, limit=limit)
    
    async def get_by_user(self, user_id: PydanticObjectId, cursor: datetime, limit: int = 10) -> List[Comment]:
        """Query comments based on user"""
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
                "$lookup": {
                    "from": "posts",
                    "localField": "post.$id",
                    "foreignField": "_id",
                    "as": "post"
                }
            },
            {"$unwind": "$post"},
            {
                "$project": {
                    "_id": 1,
                    "post_id": "$post._id",
                    "user_id": "$user._id",
                    "username": "$user.username",
                    "body": 1,
                    "created_at": 1
                }
            }
        ]

        return await self.aggregate(pipeline=pipeline, cursor_value=cursor, limit=limit)
    
    async def delete_by_post(self, post_id: PydanticObjectId) -> int:
        """Delete all comments belonging to a post. Returns count deleted."""
        result = await self.model.find({"post.$id": post_id}).delete()
        return result.deleted_count