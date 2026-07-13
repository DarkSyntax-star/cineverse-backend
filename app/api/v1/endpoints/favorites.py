from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ....core.database import get_db
from ....core.dependencies import get_current_user
from ....services.favorite_service import FavoriteService
from ....schemas.movie import MovieResponse

router = APIRouter()

@router.get("/", response_model=List[MovieResponse])
def get_favorites(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = FavoriteService(db)
    return service.get_user_favorites(current_user.id, skip=skip, limit=limit)

@router.post("/{movie_id}", status_code=status.HTTP_201_CREATED)
def add_favorite(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = FavoriteService(db)
    return service.add_favorite(current_user.id, movie_id)

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = FavoriteService(db)
    if not service.remove_favorite(current_user.id, movie_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found")
    return