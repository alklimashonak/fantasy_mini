from typing import List

from pydantic import BaseModel, Field

from .driver_schemas import Driver


class TeamBase(BaseModel):
    name: str = Field(..., max_length=48)


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: str
    owner_id: str
    drivers: List[Driver] = []

    class Config:
        orm_mode = True
