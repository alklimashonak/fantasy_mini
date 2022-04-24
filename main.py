from fastapi import FastAPI

from api.api_v1.api import api_router
from db.base import Base
from db.database import engine


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)
