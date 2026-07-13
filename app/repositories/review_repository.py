from sqlalchemy.orm import Session
from ..models.review import Review
from .base_repository import BaseRepository

class ReviewRepository(BaseRepository[Review]):
    def __init__(self, db: Session):
        super().__init__(Review, db)