from pydantic import BaseModel, Field


class DriverBase(BaseModel):
    first_name: str = Field(..., max_length=24)
    last_name: str = Field(..., max_length=24)
    number: int = Field(..., lt=100)


class DriverCreate(DriverBase):
    pass


class Driver(DriverBase):
    id: str

    class Config:
        orm_mode = True
