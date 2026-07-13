from typing import List, Optional
from sqlalchemy.orm import Session
from ..repositories.genre_repository import GenreRepository
from ..schemas.genre import GenreCreate

class GenreService:
    def __init__(self, db: Session):
        self.repo = GenreRepository(db)

    def create(self, data: GenreCreate):
        return self.repo.create(**data.dict())

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip=skip, limit=limit)

    def update(self, id: int, data: GenreCreate):
        return self.repo.update(id, **data.dict())

    def delete(self, id: int):
        return self.repo.delete(id)