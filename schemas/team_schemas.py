from typing import List

from pydantic import BaseModel, Field

from .driver_schemas import DriverDB


class TeamBase(BaseModel):
    name: str = Field(..., max_length=48)


class TeamCreate(TeamBase):
    pass


class TeamDB(TeamBase):
    id: int
    owner_id: str

    class Config:
        orm_mode = True


class TeamDBFull(TeamDB):
    drivers: List[DriverDB] = []
