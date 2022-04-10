from typing import Optional, List

from pydantic import BaseModel


class DriverBase(BaseModel):
    first_name: str
    last_name: str
    number: int


class DriverCreate(DriverBase):
    pass


class DriverDB(DriverBase):
    id: int

    class Config:
        orm_mode = True


class DriverDBFull(DriverDB):
    pass


class TeamBase(BaseModel):
    name: str


class TeamCreate(TeamBase):
    pass


class TeamDB(TeamBase):
    id: int

    class Config:
        orm_mode = True


class TeamDBFull(TeamDB):
    drivers: List[DriverDB]
    owner_id: int


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserDB(UserBase):
    id: int
    email: Optional[str] = None

    class Config:
        orm_mode = True


class UserDBFull(UserDB):
    teams: List[TeamDB]
