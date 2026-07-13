from sqlalchemy import Column, Integer, String, Float, Date, Text, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

# Association tables
movie_genre = Table(
    "movie_genres",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id")),
    Column("genre_id", Integer, ForeignKey("genres.id")),
)

movie_actor = Table(
    "movie_actors",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id")),
    Column("actor_id", Integer, ForeignKey("actors.id")),
)

movie_category = Table(
    "movie_categories",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id")),
    Column("category_id", Integer, ForeignKey("categories.id")),
)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    poster_url = Column(String, nullable=True)
    backdrop_url = Column(String, nullable=True)
    trailer_url = Column(String, nullable=True)
    release_date = Column(Date, nullable=True)
    runtime = Column(Integer, nullable=True)
    rating = Column(Float, default=0.0)
    vote_count = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    is_trending = Column(Boolean, default=False)
    is_top_rated = Column(Boolean, default=False)
    is_upcoming = Column(Boolean, default=False)
    language = Column(String, nullable=True)
    country = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    director_id = Column(Integer, ForeignKey("directors.id"), nullable=True)

    director = relationship("Director", back_populates="movies")
    genres = relationship("Genre", secondary=movie_genre, back_populates="movies")
    actors = relationship("Actor", secondary=movie_actor, back_populates="movies")
    categories = relationship("Category", secondary=movie_category, back_populates="movies")
    reviews = relationship("Review", back_populates="movie", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="movie", cascade="all, delete-orphan")
    watch_history = relationship("WatchHistory", back_populates="movie", cascade="all, delete-orphan")
