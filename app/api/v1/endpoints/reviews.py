from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ....core.database import get_db
from ....core.dependencies import get_current_user
from ....services.review_service import ReviewService
from ....schemas.review import ReviewCreate, ReviewResponse

router = APIRouter()

@router.get("/movie/{movie_id}", response_model=List[ReviewResponse])
def get_movie_reviews(
    movie_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = ReviewService(db)
    return service.get_movie_reviews(movie_id, skip=skip, limit=limit)

@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = ReviewService(db)
    return service.create_review(current_user.id, review_data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = ReviewService(db)
    if not service.delete_review(id, current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return