from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from crud import driver_crud
from api import dependencies
from schemas import driver_schemas, user_schemas

router = APIRouter()


@router.get('/', response_model=List[driver_schemas.Driver])
async def read_all_drivers(db: Session = Depends(dependencies.get_db)):
    drivers = driver_crud.get_all_drivers(db=db)
    return drivers


@router.get('/{driver_id}', response_model=driver_schemas.Driver)
async def read_driver(driver_id: int, db: Session = Depends(dependencies.get_db)):
    driver = driver_crud.get_driver_by_id(db=db, driver_id=driver_id)
    return driver


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=driver_schemas.Driver)
async def create_driver(
        driver: driver_schemas.DriverCreate,
        current_user: user_schemas.User = Depends(dependencies.get_current_user),
        db: Session = Depends(dependencies.get_db)
):
    if not current_user.is_moderator:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only moderator can create new driver')
    new_driver = driver_crud.create_driver(db=db, driver=driver)
    return new_driver


@router.put('/{driver_id}', status_code=status.HTTP_200_OK, response_model=driver_schemas.Driver)
async def update_driver(
        driver_id: int,
        driver: driver_schemas.DriverCreate,
        current_user: user_schemas.User = Depends(dependencies.get_current_user),
        db: Session = Depends(dependencies.get_db)
):
    if not current_user.is_moderator:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only moderator can update driver')
    updated_driver = driver_crud.update_driver(db=db, driver_id=driver_id, driver=driver)
    return updated_driver


@router.delete('/{driver_id}', status_code=status.HTTP_200_OK, response_model=driver_schemas.Driver)
async def delete_driver(
        driver_id: int,
        current_user: user_schemas.User = Depends(dependencies.get_current_user),
        db: Session = Depends(dependencies.get_db)
):
    if not current_user.is_moderator:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only moderator can delete driver')
    deleted_driver = driver_crud.delete_driver(db=db, driver_id=driver_id)
    return deleted_driver
