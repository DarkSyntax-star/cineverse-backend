from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ....core.database import get_db
from ....core.dependencies import get_current_active_admin
from ....services.category_service import CategoryService
from ....schemas.category import CategoryCreate, CategoryResponse

router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = CategoryService(db)
    return service.get_all(skip=skip, limit=limit)

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
):
    service = CategoryService(db)
    return service.create(category_data)

@router.put("/{id}", response_model=CategoryResponse)
def update_category(
    id: int,
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
):
    service = CategoryService(db)
    category = service.update(id, category_data)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
):
    service = CategoryService(db)
    if not service.delete(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return