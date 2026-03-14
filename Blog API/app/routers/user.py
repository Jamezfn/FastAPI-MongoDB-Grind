from fastapi import APIRouter, status, Depends
from beanie import PydanticObjectId

from app.schemas.user import UserResponse, UpdateProfileRequest, ChangePasswordRequest
from app.models.user import User
from app.services.user import UserService
from app.dependencies.auth import get_current_user
from app.dependencies.services import get_user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get profile endpoint"""
    return UserResponse.model_validate(current_user)

@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: PydanticObjectId, user_service: UserService = Depends(get_user_service)):
    """Get user endpoint"""
    user = await user_service.get_profile(user_id=user_id)
    return UserResponse.model_validate(user)

@router.patch("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_profile(body: UpdateProfileRequest, current_user: User=Depends(get_current_user), user_service: UserService=Depends(get_user_service)):
    """Update user profile"""
    updated = await user_service.update_profile(user_id=current_user.id, data=body.model_dump(exclude_none=True))

    return UserResponse.model_validate(updated)

@router.post("/me/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(body: ChangePasswordRequest, current_user: User=Depends(get_current_user), user_service: UserService=Depends(get_user_service)):
    """Change password endpoint"""
    await user_service.change_password(user_id=current_user.id, current_password=body.current_password, new_password=body.new_password)