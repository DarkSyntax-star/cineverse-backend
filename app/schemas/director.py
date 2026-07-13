from pydantic import BaseModel

class DirectorBase(BaseModel):
    name: str

class DirectorCreate(DirectorBase):
    pass

class DirectorResponse(DirectorBase):
    id: int

    class Config:
        from_attributes = True
