from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..core.database import Base

class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    profile_url = Column(String, nullable=True)

    movies = relationship("Movie", secondary="movie_actors", back_populates="actors")
