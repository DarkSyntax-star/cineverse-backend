from typing import Optional
from sqlalchemy.orm import Session
from ..models.favorite import Favorite
from .base_repository import BaseRepository

class FavoriteRepository(BaseRepository[Favorite]):
    def __init__(self, db: Session):
        super().__init__(Favorite, db)

    def get_by_user_and_movie(self, user_id: int, movie_id: int) -> Optional[Favorite]:
        return self.db.query(Favorite).filter(
            Favorite.user_id == user_id,
            Favorite.movie_id == movie_id
        ).first()
