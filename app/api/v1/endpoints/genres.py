from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ....core.database import get_db
from ....core.dependencies import get_current_active_admin
from ....services.genre_service import GenreService
from ....schemas.genre import GenreCreate, GenreResponse

router = APIRouter()

@router.get("/", response_model=List[GenreResponse])
def get_genres(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = GenreService(db)
    return service.get_all(skip=skip, limit=limit)

@router.post("/", response_model=GenreResponse, status_code=status.HTTP_201_CREATED)
def create_genre(
    genre_data: GenreCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
):
    service = GenreService(db)
    return service.create(genre_data)

@router.put("/{id}", response_model=GenreResponse)
def update_genre(
    id: int,
    genre_data: GenreCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
):
    service = GenreService(db)
    genre = service.update(id, genre_data)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
    return genre

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_genre(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
):
    service = GenreService(db)
    if not service.delete(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
    return