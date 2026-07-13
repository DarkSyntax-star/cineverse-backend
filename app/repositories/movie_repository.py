from typing import Optional, List, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from ..models.movie import Movie
from .base_repository import BaseRepository

class MovieRepository(BaseRepository[Movie]):
    def __init__(self, db: Session):
        super().__init__(Movie, db)

    def get_with_details(self, id: int) -> Optional[Movie]:
        return self.db.query(Movie).options(
            joinedload(Movie.director),
            joinedload(Movie.genres),
            joinedload(Movie.actors),
            joinedload(Movie.categories),
        ).filter(Movie.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100, **filters) -> List[Movie]:
        query = self.db.query(Movie)
        for key, value in filters.items():
            if value is not None:
                if key == "id_in" and isinstance(value, list):
                    query = query.filter(Movie.id.in_(value))
                else:
                    query = query.filter(getattr(Movie, key) == value)
        return query.offset(skip).limit(limit).all()

    def get_featured(self, limit: int = 5) -> List[Movie]:
        return self.db.query(Movie).filter(Movie.is_featured == True).limit(limit).all()

    def get_trending(self, limit: int = 10) -> List[Movie]:
        return self.db.query(Movie).filter(Movie.is_trending == True).limit(limit).all()

    def get_top_rated(self, limit: int = 10) -> List[Movie]:
        return self.db.query(Movie).order_by(Movie.rating.desc()).limit(limit).all()

    def get_upcoming(self, limit: int = 10) -> List[Movie]:
        return self.db.query(Movie).filter(Movie.is_upcoming == True).limit(limit).all()

    def search(self, query: str, skip: int = 0, limit: int = 20) -> List[Movie]:
        return self.db.query(Movie).filter(
            or_(
                Movie.title.ilike(f"%{query}%"),
                Movie.description.ilike(f"%{query}%")
            )
        ).offset(skip).limit(limit).all()