from sqlalchemy.orm import Session
from ..models.notification import Notification
from .base_repository import BaseRepository

class NotificationRepository(BaseRepository[Notification]):
    def __init__(self, db: Session):
        super().__init__(Notification, db)