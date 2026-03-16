from fastapi import APIRouter, status, Depends, Query
from beanie import PydanticObjectId
from typing import Optional
from datetime import datetime
from pydantic import TypeAdapter

from app.models.user import User
from app.models.category import Category
from app.services.post import PostService
from app.services.comment import CommentService
from app.dependencies.auth import get_current_user, get_optional_user
from app.dependencies.services import get_post_service, get_comment_service
from app.schemas.post import PostDetailResponse, CreatePostRequest, PostSummaryResponse, UpdatePostRequest
from app.schemas.common import PaginatedResponse

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_post(body: CreatePostRequest, current_user: User=Depends(get_current_user), post_service: PostService=Depends(get_post_service)):
    """Create post endpoint"""
    post = await post_service.create(
        user=current_user,
        title=body.title,
        body=body.body,
        tag_names=body.tag_names,
        category=body.category
    )

    return PostDetailResponse.model_validate(post)

@router.get("/", response_model=PaginatedResponse, status_code=status.HTTP_200_OK)
async def list_post(
    user_id: Optional[PydanticObjectId]=Query(None), limit: int=Query(5, le=10),
    tag_id: Optional[PydanticObjectId]=Query(None),
    category: Optional[Category] = Query(None),
    cursor: Optional[datetime]=Query(None), post_service: PostService = Depends(get_post_service),
    current_user: Optional[User] = Depends(get_optional_user),
):
    """List post endpoint"""
    if user_id:
        posts = await post_service.get_by_user(user_id=user_id, cursor=cursor, limit=limit)
    elif tag_id and category:
        posts = await post_service.get_by_tag_or_category(tag_ids=[tag_id], categories=[category], cursor=cursor, limit=limit)
    elif tag_id:
        posts = await post_service.get_by_tag(tag_id=tag_id, cursor=cursor, limit=limit)
    elif category:
        posts = await post_service.get_by_category(category=category, cursor=cursor, limit=limit)
    else:
        posts = await post_service.get_by_user(user_id=current_user.id if current_user else None, cursor=cursor, limit=limit)

    items = TypeAdapter(list[PostSummaryResponse]).validate_python(posts)
    next_cursor = posts[-1]["created_at"] if len(posts) == limit else None

    return PaginatedResponse(items=items, next_cursor=next_cursor, limit=limit)

@router.get("/search", response_model=PaginatedResponse[PostSummaryResponse], status_code=status.HTTP_200_OK)
async def search_posts(q: str = Query(..., min_length=1), cursor: Optional[datetime] = Query(None), limit: int = Query(10, le=50), post_service: PostService = Depends(get_post_service)):
    """Search for a post"""
    posts = await post_service.search(query=q, cursor=cursor, limit=limit)

    items = TypeAdapter(list[PostSummaryResponse]).validate_python(posts)
    next_cursor = posts[-1]["created_at"] if len(posts) == limit else None

    return PaginatedResponse(items=items, next_cursor=next_cursor, limit=limit)

@router.get("/{post_id}", response_model=PostDetailResponse)
async def get_post(post_id: PydanticObjectId, post_service: PostService=Depends(get_post_service)):
    """Get post with post id endpoint"""
    post = await post_service.get_post(post_id=post_id)
    return PostDetailResponse.model_validate(post)

@router.patch("/{post_id}", response_model=PostDetailResponse)
async def update_post(
        post_id: PydanticObjectId, body: UpdatePostRequest,
        current_user: User = Depends(get_current_user), post_service: PostService = Depends(get_post_service)
):
    post = await post_service.update(
        post_id=post_id,
        user=current_user,
        data=body.model_dump(exclude_none=True)
    )
    post = await post_service.get_post(post_id=post_id)
    return PostDetailResponse.model_validate(post)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
        post_id: PydanticObjectId,
        current_user: User = Depends(get_current_user),
        post_service: PostService = Depends(get_post_service),
        comment_service: CommentService = Depends(get_comment_service)
):
    await comment_service.delete_by_post(post_id)
    await post_service.delete(post_id=post_id, user=current_user)