from typing import List
from sqlalchemy.orm import Session
from ..repositories.favorite_repository import FavoriteRepository
from ..repositories.movie_repository import MovieRepository

class FavoriteService:
    def __init__(self, db: Session):
        self.repo = FavoriteRepository(db)
        self.movie_repo = MovieRepository(db)

    def add_favorite(self, user_id: int, movie_id: int):
        # Check if already exists
        existing = self.repo.get_by_user_and_movie(user_id, movie_id)
        if existing:
            return {"message": "Already in favorites"}
        return self.repo.create(user_id=user_id, movie_id=movie_id)

    def remove_favorite(self, user_id: int, movie_id: int) -> bool:
        favorite = self.repo.get_by_user_and_movie(user_id, movie_id)
        if not favorite:
            return False
        return self.repo.delete(favorite.id)

    def get_user_favorites(self, user_id: int, skip: int = 0, limit: int = 100):
        # Get favorite movies
        favorites = self.repo.get_all(user_id=user_id, skip=skip, limit=limit)
        movie_ids = [f.movie_id for f in favorites]
        return self.movie_repo.get_all(id_in=movie_ids) if movie_ids else []