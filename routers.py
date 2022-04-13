from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import crud
import dependencies
from schemas import UserDB, UserCreate, TeamDB, TeamDBFull, UserDBFull, DriverDB, DriverDBFull, DriverCreate, TeamCreate

router = APIRouter()


@router.get('/users', response_model=List[UserDB])
async def read_all_users(db: Session = Depends(dependencies.get_db)):
    users = crud.get_all_users(db=db)
    return users


@router.get('/users/{user_id}', response_model=UserDBFull)
async def read_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    user = crud.get_user_by_id(db=db, user_id=user_id)
    return user


@router.post('/users', response_model=UserDB)
async def create_user(user: UserCreate, db: Session = Depends(dependencies.get_db)):
    new_user = crud.create_user(db=db, user=user)
    return new_user


@router.get('/teams', response_model=List[TeamDB])
async def read_all_teams(db: Session = Depends(dependencies.get_db)):
    teams = crud.get_all_teams(db=db)
    return teams


@router.get('/teams/{team_id}', response_model=TeamDBFull)
async def read_team(team_id: int, db: Session = Depends(dependencies.get_db)):
    team = crud.get_team_by_id(db=db, team_id=team_id)
    return team


@router.post('/teams', status_code=status.HTTP_201_CREATED, response_model=TeamDB)
async def create_team(user_id: int, team: TeamCreate, db: Session = Depends(dependencies.get_db)):
    new_team = crud.create_team(db=db, user_id=user_id, team=team)
    return new_team


@router.get('/drivers', response_model=List[DriverDB])
async def read_all_drivers(db: Session = Depends(dependencies.get_db)):
    drivers = crud.get_all_drivers(db=db)
    return drivers


@router.get('/drivers/{driver_id}', response_model=DriverDBFull)
async def read_driver(driver_id: int, db: Session = Depends(dependencies.get_db)):
    driver = crud.get_driver_by_id(db=db, driver_id=driver_id)
    return driver


@router.post('/drivers', status_code=status.HTTP_201_CREATED, response_model=DriverDB)
async def create_driver(driver: DriverCreate, db: Session = Depends(dependencies.get_db)):
    new_driver = crud.create_driver(db=db, driver=driver)
    return new_driver
