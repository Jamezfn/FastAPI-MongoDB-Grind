from fastapi import APIRouter, status, Depends

from app.models.user import User
from app.models.post import Post
from app.services.post import PostService
from app.dependencies.auth import get_current_user
from app.dependencies.services import get_post_service
from app.schemas.post import PostDetailResponse, CreatePostRequest, CreatePostDetailResponse

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