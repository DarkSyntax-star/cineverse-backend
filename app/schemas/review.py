from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .user import UserResponse

class ReviewBase(BaseModel):
    rating: float
    comment: str

class ReviewCreate(ReviewBase):
    movie_id: int

class ReviewUpdate(BaseModel):
    rating: Optional[float] = None
    comment: Optional[str] = None

class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    movie_id: int
    created_at: datetime
    user: UserResponse

    class Config:
        from_attributes = True
