from fastapi import APIRouter, Depends, Query
from beanie import PydanticObjectId
from datetime import datetime
from typing import Optional
from pydantic import TypeAdapter

from app.schemas.comment import CreateCommentRequest, CommentResponse
from app.schemas.common import PaginatedResponse
from app.models.user import User
from app.services.comment import CommentService
from app.dependencies.services import get_comment_service
from app.dependencies.auth import get_current_user

router = APIRouter(tags=["Comments"])


@router.post("/posts/{post_id}/comments", response_model=CommentResponse, status_code=201)
async def create_comment(
        post_id: PydanticObjectId,
        body: CreateCommentRequest,
        current_user: User = Depends(get_current_user),
        comment_service: CommentService = Depends(get_comment_service)
):
    comment = await comment_service.create(
        user=current_user,
        post_id=post_id,
        body=body.body
    )

    return CommentResponse.model_validate(comment)

@router.get("/posts/{post_id}/comments")
async def get_post_comments(post_id: PydanticObjectId, cursor: Optional[datetime] = Query(None), limit: int = Query(10, le=50),
    comment_service: CommentService = Depends(get_comment_service)
):
    """Get comments for a post"""
    comments = await comment_service.get_by_post(post_id=post_id, cursor=cursor, limit=limit)
    items = TypeAdapter(list[CommentResponse]).validate_python(comments)

    next_cursor = comments[-1]["created_at"] if len(comments) == limit else None

    return PaginatedResponse(items=items, next_cursor=next_cursor, limit=limit)

@router.get("/users/{user_id}/comments", response_model=PaginatedResponse[CommentResponse])
async def get_users_comments(user_id: PydanticObjectId, cursor: Optional[datetime] = Query(None), limit: int = Query(10, le=50),
    comment_service: CommentService = Depends(get_comment_service)
):
    """Get comments for a post"""
    comments = await comment_service.get_by_user(user_id=user_id, cursor=cursor, limit=limit)
    items = TypeAdapter(list[CommentResponse]).validate_python(comments)

    next_cursor = comments[-1]["created_at"] if len(comments) == limit else None

    return PaginatedResponse(items=items, next_cursor=next_cursor, limit=limit)

@router.delete("/comments/{comment_id}", status_code=204)
async def delete_comment(
        comment_id: PydanticObjectId,
        current_user: User = Depends(get_current_user),
        comment_service: CommentService = Depends(get_comment_service)
):
    await comment_service.delete(comment_id=comment_id, user=current_user)