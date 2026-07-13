from typing import List, Optional
from sqlalchemy.orm import Session
from ..repositories.review_repository import ReviewRepository
from ..schemas.review import ReviewCreate

class ReviewService:
    def __init__(self, db: Session):
        self.repo = ReviewRepository(db)

    def create_review(self, user_id: int, data: ReviewCreate):
        return self.repo.create(
            user_id=user_id,
            movie_id=data.movie_id,
            rating=data.rating,
            comment=data.comment
        )

    def get_movie_reviews(self, movie_id: int, skip: int = 0, limit: int = 100):
        return self.repo.get_all(movie_id=movie_id, skip=skip, limit=limit)

    def delete_review(self, review_id: int, user_id: int) -> bool:
        review = self.repo.get(review_id)
        if not review or review.user_id != user_id:
            return False
        return self.repo.delete(review_id)