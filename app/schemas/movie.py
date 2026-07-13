from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List
from .genre import GenreResponse
from .actor import ActorResponse
from .category import CategoryResponse
from .director import DirectorResponse

class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    poster_url: Optional[str] = None
    backdrop_url: Optional[str] = None
    trailer_url: Optional[str] = None
    release_date: Optional[date] = None
    runtime: Optional[int] = None
    rating: float = 0.0
    vote_count: int = 0
    is_featured: bool = False
    is_trending: bool = False
    is_top_rated: bool = False
    is_upcoming: bool = False
    language: Optional[str] = None
    country: Optional[str] = None

class MovieCreate(MovieBase):
    director_id: Optional[int] = None
    genre_ids: List[int] = []
    actor_ids: List[int] = []
    category_ids: List[int] = []

class MovieUpdate(MovieBase):
    director_id: Optional[int] = None
    genre_ids: Optional[List[int]] = None
    actor_ids: Optional[List[int]] = None
    category_ids: Optional[List[int]] = None

class MovieResponse(MovieBase):
    id: int
    director: Optional[DirectorResponse] = None
    genres: List[GenreResponse] = []
    actors: List[ActorResponse] = []
    categories: List[CategoryResponse] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
