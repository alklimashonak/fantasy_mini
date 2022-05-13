from typing import Optional, List

from pydantic import BaseModel, Field

from .team_schemas import Team


class UserBase(BaseModel):
    username: str = Field(..., max_length=24)
    email: Optional[str] = Field(None, max_length=48)


class UserCreate(UserBase):
    password: str = Field(..., max_length=24)


class User(UserBase):
    id: str
    is_superuser: bool
    is_moderator: bool
    teams: List[Team] = []

    class Config:
        orm_mode = True


class UserDB(User):
    hashed_password: str
