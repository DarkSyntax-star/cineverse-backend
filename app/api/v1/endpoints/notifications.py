from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ....core.database import get_db
from ....core.dependencies import get_current_user
from ....services.notification_service import NotificationService
from ....schemas.notification import NotificationResponse

router = APIRouter()

@router.get("/", response_model=List[NotificationResponse])
def get_notifications(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = NotificationService(db)
    return service.get_user_notifications(current_user.id, skip=skip, limit=limit)

@router.put("/{id}/read")
def mark_as_read(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = NotificationService(db)
    return service.mark_as_read(id, current_user.id)