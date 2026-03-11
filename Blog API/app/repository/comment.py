from beanie import PydanticObjectId
from datetime import datetime
from typing import List, Optional, Dict, Any

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


    async def get_comments_by_post_aggregated(
        self,
        post_id: PydanticObjectId,
        cursor: Optional[datetime] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Fetch comments for a specific post, returning only:
        - comment body, created_at, and (optionally) _id
        - username of the commenter
        Supports cursor pagination on created_at.
        """
        pipeline: List[Dict[str, Any]] = [
            {"$match": {"post.$id": post_id}},
            {
                "$lookup": {
                    "from": "users",
                    "let": {"uid": "$user.$id"},
                    "pipeline": [
                        {"$match": {"$expr": {"$eq": ["$_id", "$$uid"]}}},
                        {"$project": {"username": 1}}
                    ],
                    "as": "user"
                }
            },
            {"$unwind": "$user"},
            {
                "$project": {
                    "_id": 1,
                    "body": 1,
                    "created_at": 1,
                    "username": "$user.username"
                }
            },
            {"$sort": {"created_at": -1}}
        ]

        return await self.aggregate(pipeline=pipeline, cursor_field="created_at", cursor_value=cursor, cursor_operator="$lt", limit=limit)

    async def get_comments_by_user_aggregated(
        self, user_id: PydanticObjectId, cursor: Optional[datetime] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Fetch comments written by a specific user, returning:
        - comment body, created_at, and _id
        - username of the commenter (the same user)
        - title of the post the comment belongs to
        Supports cursor pagination on created_at.
        """
        pipeline: List[Dict[str, Any]] = [
            {"$match": {"user.$id": user_id}},
            {
                "$lookup": {
                    "from": "posts",
                    "let": {"pid": "$post.$id"},
                    "pipeline": [
                        {"$match": {"$expr": {"$eq": ["$_id", "$$pid"]}}},
                        {"$project": {"title": 1}}
                    ],
                    "as": "post"
                }
            },
            {"$unwind": "$post"},
            {
                "$lookup": {
                    "from": "users",
                    "let": {"uid": "$user.$id"},
                    "pipeline": [
                        {"$match": {"$expr": {"$eq": ["$_id", "$$uid"]}}},
                        {"$project": {"username": 1}}
                    ],
                    "as": "user"
                }
            },
            {"$unwind": "$user"},
            {
                "$project": {
                    "_id": 1,
                    "body": 1,
                    "created_at": 1,
                    "username": "$user.username",
                    "post_title": "$post.title"
                }
            },
            {"$sort": {"created_at": -1}}
        ]

        return await self.aggregate(pipeline=pipeline, cursor_field="created_at", cursor_value=cursor,
            cursor_operator="$lt", limit=limit)