from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ....core.database import get_db
from ....core.dependencies import get_current_user
from ....services.auth_service import AuthService
from ....schemas.user import UserCreate, UserResponse
from ....schemas.token import Token, TokenRefresh

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register(user_data)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(form_data.username, form_data.password)

@router.post("/refresh", response_model=Token)
def refresh(token_data: TokenRefresh, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.refresh(token_data.refresh_token)

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    service = AuthService(db)
    service.logout(current_user.id)
    return

@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user
