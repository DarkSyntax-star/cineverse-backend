from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from ....core.database import get_db
from ....core.dependencies import get_current_user, get_current_active_admin
from ....services.movie_service import MovieService
from ....schemas.movie import MovieCreate, MovieUpdate, MovieResponse

router = APIRouter()

# Existing endpoints for admin (database)
@router.get("/db", response_model=List[MovieResponse])
def get_movies_db(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = MovieService(db)
    return service.get_all_from_db(skip=skip, limit=limit)

@router.get("/db/{id}", response_model=MovieResponse)
def get_movie_db(id: int, db: Session = Depends(get_db)):
    service = MovieService(db)
    movie = service.get_from_db(id)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return movie

@router.post("/", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(
    movie_data: MovieCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
):
    service = MovieService(db)
    return service.create(movie_data)

@router.put("/{id}", response_model=MovieResponse)
def update_movie(
    id: int,
    movie_data: MovieUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
):
    service = MovieService(db)
    movie = service.update(id, movie_data)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return movie

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
):
    service = MovieService(db)
    if not service.delete(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return

# New TMDB endpoints for public consumption
@router.get("/", response_model=List[MovieResponse])
async def get_movies(
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    service = MovieService(db)
    movies = await service.get_popular(page)
    return movies

@router.get("/featured", response_model=List[MovieResponse])
async def get_featured(
    db: Session = Depends(get_db)
):
    service = MovieService(db)
    movies = await service.get_popular(page=1)
    return movies[:5]  # Return first 5 as featured

@router.get("/trending", response_model=List[MovieResponse])
async def get_trending(
    db: Session = Depends(get_db)
):
    service = MovieService(db)
    return await service.get_trending()

@router.get("/top-rated", response_model=List[MovieResponse])
async def get_top_rated(
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    service = MovieService(db)
    return await service.get_top_rated(page)

@router.get("/upcoming", response_model=List[MovieResponse])
async def get_upcoming(
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    service = MovieService(db)
    return await service.get_upcoming(page)

@router.get("/{id}", response_model=MovieResponse)
async def get_movie(
    id: int,
    db: Session = Depends(get_db)
):
    service = MovieService(db)
    try:
        movie = await service.get_movie_details(id)
        return movie
    except HTTPException:
        # Fallback to database if not found in TMDB
        movie_db = service.get_from_db(id)
        if not movie_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
        return movie_db