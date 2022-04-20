from typing import Optional, List

from pydantic import BaseModel, Field


class DriverBase(BaseModel):
    first_name: str = Field(..., max_length=24)
    last_name: str = Field(..., max_length=24)
    number: int = Field(..., lt=100)


class DriverCreate(DriverBase):
    pass


class DriverDB(DriverBase):
    id: int

    class Config:
        orm_mode = True


class DriverDBFull(DriverDB):
    pass


class TeamBase(BaseModel):
    name: str = Field(..., max_length=48)


class TeamCreate(TeamBase):
    pass


class TeamDB(TeamBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str = Field(..., max_length=24)


class UserCreate(UserBase):
    password: str = Field(..., max_length=24)


class UserDB(UserBase):
    id: int
    email: Optional[str] = Field(None, max_length=48)

    class Config:
        orm_mode = True


class UserDBFull(UserDB):
    teams: List[TeamDB] = []


class TeamDBFull(TeamDB):
    drivers: List[DriverDB] = []
