from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class WatchHistory(Base):
    __tablename__ = "watch_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    progress = Column(Float, default=0.0)
    watched_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="watch_history")
    movie = relationship("Movie", back_populates="watch_history")
