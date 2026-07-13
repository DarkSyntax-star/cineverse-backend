from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from ..repositories.movie_repository import MovieRepository
from ..schemas.movie import MovieCreate, MovieUpdate
from .tmdb_service import TmdbService

class MovieService:
    def __init__(self, db: Session):
        self.repo = MovieRepository(db)
        self.db = db
        self.tmdb = TmdbService()

    # Existing database methods for admin operations
    def create(self, data: MovieCreate):
        return self.repo.create(**data.dict(exclude_unset=True))

    def get_from_db(self, id: int):
        return self.repo.get_with_details(id)

    def get_all_from_db(self, skip: int = 0, limit: int = 20):
        return self.repo.get_all(skip=skip, limit=limit)

    def update(self, id: int, data: MovieUpdate):
        return self.repo.update(id, **data.dict(exclude_unset=True))

    def delete(self, id: int):
        return self.repo.delete(id)

    # New TMDB methods
    async def get_popular(self, page: int = 1) -> List[Dict[str, Any]]:
        """Get popular movies from TMDB"""
        return await self.tmdb.get_popular_movies(page)

    async def get_trending(self) -> List[Dict[str, Any]]:
        """Get trending movies from TMDB"""
        return await self.tmdb.get_trending_movies()

    async def get_top_rated(self, page: int = 1) -> List[Dict[str, Any]]:
        """Get top rated movies from TMDB"""
        return await self.tmdb.get_top_rated_movies(page)

    async def get_upcoming(self, page: int = 1) -> List[Dict[str, Any]]:
        """Get upcoming movies from TMDB"""
        return await self.tmdb.get_upcoming_movies(page)

    async def get_movie_details(self, movie_id: int) -> Dict[str, Any]:
        """Get movie details from TMDB"""
        return await self.tmdb.get_movie_details(movie_id)

    async def search(self, query: str, page: int = 1) -> List[Dict[str, Any]]:
        """Search movies on TMDB"""
        return await self.tmdb.search_movies(query, page)