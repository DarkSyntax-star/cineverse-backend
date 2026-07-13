from sqlalchemy.orm import Session
from ..models.category import Category
from .base_repository import BaseRepository

class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db: Session):
        super().__init__(Category, db)
