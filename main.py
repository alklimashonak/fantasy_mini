from fastapi import FastAPI

from routers import router
from db.base import Base
from db.database import engine


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(router)
