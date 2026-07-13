from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ....core.database import get_db
from ....services.movie_service import MovieService
from ....schemas.movie import MovieResponse

router = APIRouter()

@router.get("/", response_model=List[MovieResponse])
async def search_movies(
    q: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    service = MovieService(db)
    return await service.search(q, page)