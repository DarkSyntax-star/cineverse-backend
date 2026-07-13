from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from ..repositories.user_repository import UserRepository
from ..repositories.refresh_token_repository import RefreshTokenRepository
from ..schemas.user import UserCreate
from ..schemas.token import Token

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.token_repo = RefreshTokenRepository(db)
        self.db = db

    def register(self, user_data: UserCreate) -> Token:
        if self.user_repo.get_by_email(user_data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        if self.user_repo.get_by_username(user_data.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

        hashed = get_password_hash(user_data.password)
        user = self.user_repo.create(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed,
        )
        return self._create_tokens(user.id)

    def login(self, username: str, password: str) -> Token:
        user = self.user_repo.get_by_username(username) or self.user_repo.get_by_email(username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
        return self._create_tokens(user.id)

    def refresh(self, refresh_token: str) -> Token:
        stored_token = self.token_repo.get_by_token(refresh_token)
        if not stored_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        self.token_repo.delete(stored_token.id)
        return self._create_tokens(stored_token.user_id)

    def logout(self, user_id: int):
        self.token_repo.revoke_user_tokens(user_id)

    def _create_tokens(self, user_id: int) -> Token:
        access_token = create_access_token(data={"sub": str(user_id)})
        refresh_token = create_refresh_token(data={"sub": str(user_id)})
        expires_in = timedelta(days=7)
        self.token_repo.create(
            user_id=user_id,
            token=refresh_token,
            expires_at=datetime.now(timezone.utc) + expires_in
        )
        return Token(access_token=access_token, refresh_token=refresh_token)
