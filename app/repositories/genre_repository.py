from sqlalchemy.orm import Session
from ..models.genre import Genre
from .base_repository import BaseRepository

class GenreRepository(BaseRepository[Genre]):
    def __init__(self, db: Session):
        super().__init__(Genre, db)
