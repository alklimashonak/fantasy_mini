from sqlalchemy.orm import Session

from models import User, Team, Driver
from schemas import UserCreate, TeamCreate, DriverCreate


def get_all_users(db: Session):
    users = db.query(User).all()
    return users


def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    return user


def create_user(db: Session, user: UserCreate):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_teams(db: Session):
    teams = db.query(Team).all()
    return teams


def get_team_by_id(db: Session, team_id: int):
    team = db.query(Team).filter(Team.id == team_id).first()
    return team


def create_team(db: Session, user_id: int, team: TeamCreate):
    new_team = Team(**team.dict(), owner_id=user_id)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team


def get_all_drivers(db: Session):
    drivers = db.query(Driver).all()
    return drivers


def get_driver_by_id(db: Session, driver_id: int):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    return driver


def create_driver(db: Session, driver: DriverCreate):
    new_driver = Driver(**driver.dict())
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver
