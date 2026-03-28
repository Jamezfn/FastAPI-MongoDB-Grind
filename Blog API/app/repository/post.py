from typing import Optional, List, Dict, Any
from beanie import PydanticObjectId
from datetime import datetime

from .base import BaseRepo
from app.models.post import Post
from app.models.category import Category

class PostRepo(BaseRepo[Post]):
    def __init__(self):
        super().__init__(model=Post)

    async def create_post(self, data: Dict[str, Any]) -> Post:
        """Create post and serialize"""
        post = await self.create(data=data)

        pipeline = [
            {"$match": {"_id": post.id}},
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user.$id",
                    "foreignField": "_id",
                    "as": "user",
                }
            },
            {"$unwind": "$user"},
            {
                "$lookup": {
                    "from": "tags",
                    "localField": "tags.$id",
                    "foreignField": "_id",
                    "as": "tags",
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "title": 1,
                    "body": 1,
                    "categories": 1,
                    "created_at": 1,
                    "username": "$user.username",
                    "tags": {
                        "$map": {
                            "input": "$tags",
                            "as": "tag",
                            "in": "$$tag.name"
                        }
                    },
                }
            },
        ]

        collection = self.model.get_pymongo_collection()
        cursor = collection.aggregate(pipeline)
        result = await cursor.to_list(length=None)
        return result[0] if result else post.model_dump()
    
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
            self, category: Category, cursor: Optional[datetime] = None,
            limit: int = 10, fetch_links: bool = False
    ) -> List[Post]:
        """Get post based on category"""
        filters = {"category": category}

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
            or_conditions.append({"category": {"$in": category_ids}})

        filters = {"$or": or_conditions} if or_conditions else {}

        return await self.find_with_cursor(filters=filters, cursor_value=cursor, sort=[("created_at", -1)], limit=limit, fetch_links=fetch_links)

    async def search(
            self, query: str, cursor: Optional[datetime] = None,
            limit: int = 10, fetch_links: bool = False
    ) -> List[Post]:
        """Search posts using aggregation and return detailed response models."""
        pipeline = []

        match_stage = {"$text": {"$search": query}}
        if cursor:
            match_stage["created_at"] = {"$lt": cursor}
        
        pipeline.append({"$match": match_stage})
        pipeline.append({"$sort": {"created_at": -1}})
        pipeline.append(
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user.$id",
                    "foreignField": "_id",
                    "as": "user"
                }
            }
        )
        pipeline.append({"$unwind": "$user"})

        pipeline.append(
            {

                "$lookup": {
                    "from": "tags",
                    "localField": "tags.$id",
                    "foreignField": "_id",
                    "as": "tags"
                }
            }
        )

        pipeline.append(
            {
                "$project": {
                    "_id": 1,
                    "title": 1,
                    "body": 1,
                    "categories": 1,
                    "created_at": 1,
                    "username": "$user.username",
                    "tags": {
                        "$map": {
                            "input": "$tags",
                            "as": "tag",
                            "in": "$$tag.name"
                        }
                    }
                }
            }
        )

        return await self.aggregate(pipeline=pipeline)



    async def get_post_with_relations(self, post_id: PydanticObjectId) -> Optional[dict]:
        """
        Fetch a single post by ID, with user and tags populated,
        returning a dictionary ready for PostDetailResponse.
        """
        pipeline = [
            {"$match": {"_id": post_id}},
            {
                "$lookup": {
                    "from": "users",
                    "let": {"user_id": "$user.$id"},
                    "pipeline": [
                        {"$match": {"$expr": {"$eq": ["$_id", "$$user_id"]}}},
                        {"$project": {"username": 1}}
                    ],
                    "as": "user"
                }
            },
            {"$unwind": "$user"},
            {
                "$lookup": {
                    "from": "tags",
                    "let": {"tag_ids": "$tags.$id"},
                    "pipeline": [
                        {"$match": {"$expr": {"$in": ["$_id", "$$tag_ids"]}}},
                        {"$project": {"_id": 0, "name": 1}}
                    ],
                    "as": "tags"
                }
            },
            {
                "$project": {
                    "title": 1,
                    "body": 1,
                    "created_at": 1,
                    "username": "$user.username",
                    "tags": {
                        "$map": {
                            "input": "$tags",
                            "as": "tag",
                            "in": "$$tag.name"
                        }
                    },
                    "categories": 1,
                }
            }
        ]

        results = await self.aggregate(pipeline=pipeline)
        return results[0] if results else None
    
    async def get_posts_by_user_aggregated(
        self, user_id: PydanticObjectId, cursor: Optional[datetime] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Fetch posts by a specific user, returning only:
        - title, body, created_at, categories
        - username (from the linked user)
        - tags (array of tag names)
        Supports cursor pagination on created_at.
        """
        pipeline: List[Dict[str, Any]] = [
            {"$match": {"user.$id": user_id}},
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
                "$lookup": {
                    "from": "tags",
                    "let": {"tag_ids": "$tags.$id"},
                    "pipeline": [
                        {"$match": {"$expr": {"$in": ["$_id", "$$tag_ids"]}}},
                        {"$project": {"_id": 0, "name": 1}}
                    ],
                    "as": "tags"
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "title": 1,
                    "body": 1,
                    "created_at": 1,
                    "categories": "$categories",
                    "username": "$user.username",
                    "tags": "$tags.name"
                }
            },
            {"$sort": {"created_at": -1}}
        ]
        return await self.aggregate(
            pipeline=pipeline, cursor_field="created_at", cursor_value=cursor,
            cursor_operator="$lt", limit=limit
        )

    async def get_posts_by_tag_aggregated(
        self,
        tag_id: PydanticObjectId,
        cursor: Optional[datetime] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Fetch posts that contain a specific tag, returning only:
        - title, body, created_at, categories
        - username (from the linked user)
        - tags (array of all tag names for the post)
        Supports cursor pagination on created_at.
        """
        pipeline: List[Dict[str, Any]] = [
            {"$match": {"tags.$id": tag_id}},
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
                "$lookup": {
                    "from": "tags",
                    "let": {
                        "$map": {
                            "input": "$tags",
                            "as": "t",
                            "in": "$$t.$id"
                        }
                    },
                    "pipeline": [
                        {"$match": {"$expr": {"$in": ["$_id", "$$tag_ids"]}}},
                        {"$project": {"_id": 0, "name": 1}}
                    ],
                    "as": "tags"
                }
            },
            {
                "$project": {
                    "title": 1,
                    "body": 1,
                    "created_at": 1,
                    "categories": 1,
                    "username": "$user.username",
                    "tags": "$tags.name"
                }
            },
            {"$sort": {"created_at": -1}}
        ]
        return await self.aggregate(pipeline=pipeline, cursor_field="created_at", cursor_value=cursor,
            cursor_operator="$lt", limit=limit
        )

    async def get_posts_by_category_aggregated(
        self,
        category: Category,
        cursor: Optional[datetime] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Fetch posts belonging to a specific category, returning only:
        - title, body, created_at, categories (the enum)
        - username (from the linked user)
        - tags (array of tag names)
        Supports cursor pagination on created_at.
        """
        pipeline: List[Dict[str, Any]] = [
            {"$match": {"categories": category}},
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
                "$lookup": {
                    "from": "tags",
                    "let": {"tag_ids": "$tags.$id"},
                    "pipeline": [
                        {"$match": {"$expr": {"$in": ["$_id", "$$tag_ids"]}}},
                        {"$project": {"_id": 0, "name": 1}}
                    ],
                    "as": "tags"
                }
            },
            {
                "$project": {
                    "title": 1,
                    "body": 1,
                    "created_at": 1,
                    "categories": 1,
                    "username": "$user.username",
                    "tags": "$tags.name"
                }
            },
            {"$sort": {"created_at": -1}}
        ]

        return await self.aggregate(pipeline=pipeline, cursor_field="created_at", cursor_value=cursor, cursor_operator="$lt", limit=limit)

    async def get_posts_by_tag_or_category_aggregated(
        self, tag_ids: Optional[List[PydanticObjectId]] = None, categories: Optional[List[Category]] = None,
        cursor: Optional[datetime] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Fetch posts that match ANY of the provided tag IDs OR ANY of the provided categories.
        Returns only:
        - title, body, created_at, categories
        - username (from linked user)
        - tags (array of tag names)
        Supports cursor pagination on created_at.
        """
        match_conditions = []
        if tag_ids:
            match_conditions.append({"tags.$id": {"$in": tag_ids}})
        if categories:
            match_conditions.append({"categories": {"$in": categories}})
        if not match_conditions:
            return []

        pipeline: List[Dict[str, Any]] = [
            {"$match": {"$or": match_conditions}},
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
                "$lookup": {
                    "from": "tags",
                    "let": {"tag_ids": {"$map": {"input": "$tags", "as": "t", "in": "$$t.$id"}}},
                    "pipeline": [
                        {"$match": {"$expr": {"$in": ["$_id", "$$tag_ids"]}}},
                        {"$project": {"_id": 0, "name": 1}}
                    ],
                    "as": "tags"
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "title": 1,
                    "body": 1,
                    "created_at": 1,
                    "categories": 1,
                    "username": "$user.username",
                    "tags": "$tags.name"
                }
            },
            {"$sort": {"created_at": -1}}
        ]

        return await self.aggregate( pipeline=pipeline, cursor_field="created_at", cursor_value=cursor,
            cursor_operator="$lt", limit=limit)