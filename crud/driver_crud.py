from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Driver
from schemas import driver_schemas


def get_all_drivers(db: Session):
    drivers = db.query(Driver).all()
    return drivers


def get_driver_by_id(db: Session, driver_id: int):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No driver with this ID')
    return driver


def create_driver(db: Session, driver: driver_schemas.DriverCreate):
    new_driver = Driver(**driver.dict())
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver


def update_driver(db: Session, driver_id: int, driver: driver_schemas.DriverCreate):
    current_driver = db.query(Driver).filter(Driver.id == driver_id).first()
    current_driver.first_name = driver.first_name
    current_driver.last_name = driver.last_name
    current_driver.number = driver.number
    db.add(current_driver)
    db.commit()
    db.refresh(current_driver)
    return current_driver


def delete_driver(db: Session, driver_id: int):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    db.delete(driver)
    db.commit()
    return driver
