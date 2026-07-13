from typing import List
from sqlalchemy.orm import Session
from ..repositories.notification_repository import NotificationRepository

class NotificationService:
    def __init__(self, db: Session):
        self.repo = NotificationRepository(db)

    def get_user_notifications(self, user_id: int, skip: int = 0, limit: int = 50):
        return self.repo.get_all(user_id=user_id, skip=skip, limit=limit)

    def mark_as_read(self, notification_id: int, user_id: int):
        notification = self.repo.get(notification_id)
        if notification and notification.user_id == user_id:
            return self.repo.update(notification_id, is_read=True)
        return None