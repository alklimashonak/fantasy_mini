from typing import Optional, List

from pydantic import BaseModel, Field

from .team_schemas import TeamDB


class UserBase(BaseModel):
    username: str = Field(..., max_length=24)
    email: Optional[str] = Field(None, max_length=48)


class UserCreate(UserBase):
    password: str = Field(..., max_length=24)


class UserDB(UserBase):
    id: str
    hashed_password: str
    is_superuser: bool
    is_moderator: bool

    class Config:
        orm_mode = True


class UserDBFull(UserDB):
    teams: List[TeamDB] = []
