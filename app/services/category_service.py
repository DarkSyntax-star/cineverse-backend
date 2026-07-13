from typing import List, Optional
from sqlalchemy.orm import Session
from ..repositories.category_repository import CategoryRepository
from ..schemas.category import CategoryCreate

class CategoryService:
    def __init__(self, db: Session):
        self.repo = CategoryRepository(db)

    def create(self, data: CategoryCreate):
        return self.repo.create(**data.dict())

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip=skip, limit=limit)

    def update(self, id: int, data: CategoryCreate):
        return self.repo.update(id, **data.dict())

    def delete(self, id: int):
        return self.repo.delete(id)