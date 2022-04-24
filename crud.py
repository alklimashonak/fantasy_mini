from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import utils
from models import User, Team, Driver
from schemas import UserCreate, TeamCreate, DriverCreate


def get_all_users(db: Session):
    users = db.query(User).all()
    return users


def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No user with this ID')
    return user


def get_user_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No user with this username')
    return user


def create_user(db: Session, user: UserCreate):
    hashed_password = utils.get_password_hash(user.password)
    new_user = User(**user.dict(exclude={'password'}), hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_teams(db: Session):
    teams = db.query(Team).all()
    return teams


def get_team_by_id(db: Session, team_id: int):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No team with this ID')
    return team


def create_team(db: Session, user_id: str, team: TeamCreate):
    new_team = Team(**team.dict(), owner_id=user_id)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team


def update_team(db: Session, team_id: int, team: TeamCreate):
    current_team = db.query(Team).filter(Team.id == team_id).first()
    current_team.name = team.name
    db.add(current_team)
    db.commit()
    db.refresh(current_team)
    return current_team


def get_all_drivers(db: Session):
    drivers = db.query(Driver).all()
    return drivers


def get_driver_by_id(db: Session, driver_id: int):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No driver with this ID')
    return driver


def create_driver(db: Session, driver: DriverCreate):
    new_driver = Driver(**driver.dict())
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver


def update_driver(db: Session, driver_id: int, driver: DriverCreate):
    current_driver = db.query(Driver).filter(Driver.id == driver_id).first()
    current_driver.first_name = driver.first_name
    current_driver.last_name = driver.last_name
    current_driver.number = driver.number
    db.add(current_driver)
    db.commit()
    db.refresh(current_driver)
    return current_driver
