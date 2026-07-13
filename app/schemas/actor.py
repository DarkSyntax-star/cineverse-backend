from pydantic import BaseModel
from typing import Optional

class ActorBase(BaseModel):
    name: str
    profile_url: Optional[str] = None

class ActorCreate(ActorBase):
    pass

class ActorResponse(ActorBase):
    id: int

    class Config:
        from_attributes = True
