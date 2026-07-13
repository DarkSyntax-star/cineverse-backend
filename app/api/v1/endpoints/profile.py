from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ....core.database import get_db
from ....core.dependencies import get_current_user
from ....services.profile_service import ProfileService
from ....schemas.user import UserResponse, UserUpdate

router = APIRouter()

@router.get("/", response_model=UserResponse)
def get_profile(
    current_user = Depends(get_current_user)
):
    return current_user

@router.put("/", response_model=UserResponse)
def update_profile(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = ProfileService(db)
    user = service.update_profile(current_user.id, user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user