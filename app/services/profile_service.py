from typing import Optional
from sqlalchemy.orm import Session
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserUpdate
from ..core.security import get_password_hash

class ProfileService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def update_profile(self, user_id: int, data: UserUpdate):
        update_data = data.dict(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        return self.repo.update(user_id, **update_data)