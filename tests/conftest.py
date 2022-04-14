import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database
from starlette.testclient import TestClient

import schemas
from crud import create_driver, create_team, create_user
from db.database import Base
from dependencies import get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test2.db"


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    connection.begin()

    db = Session(bind=connection)

    yield db

    db.rollback()
    connection.close()


# 
@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c


@pytest.fixture
def create_two_drivers(db):
    create_driver(db, schemas.DriverCreate(first_name='Lewis',
                                           last_name='Hamilton',
                                           number=44))
    create_driver(db, schemas.DriverCreate(first_name='Max',
                                           last_name='Verstappen',
                                           number='1'))


@pytest.fixture
def create_two_teams(db):
    user = create_user(db, schemas.UserCreate(username='user', password='1234'))
    create_team(db, user.id, schemas.TeamCreate(name='team 1'))
    create_team(db, user.id, schemas.TeamCreate(name='team 2'))