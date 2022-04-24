from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from crud import driver_crud
from api import dependencies
from schemas import driver_schemas


router = APIRouter()


@router.get('/', response_model=List[driver_schemas.DriverDB])
async def read_all_drivers(db: Session = Depends(dependencies.get_db)):
    drivers = driver_crud.get_all_drivers(db=db)
    return drivers


@router.get('/{driver_id}', response_model=driver_schemas.DriverDB)
async def read_driver(driver_id: int, db: Session = Depends(dependencies.get_db)):
    driver = driver_crud.get_driver_by_id(db=db, driver_id=driver_id)
    return driver


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=driver_schemas.DriverDB)
async def create_driver(driver: driver_schemas.DriverCreate, db: Session = Depends(dependencies.get_db)):
    new_driver = driver_crud.create_driver(db=db, driver=driver)
    return new_driver


@router.put('/{driver_id}', status_code=status.HTTP_200_OK, response_model=driver_schemas.DriverDB)
async def update_driver(driver_id: int, driver: driver_schemas.DriverCreate, db: Session = Depends(dependencies.get_db)):
    updated_driver = driver_crud.update_driver(db=db, driver_id=driver_id, driver=driver)
    return updated_driver
