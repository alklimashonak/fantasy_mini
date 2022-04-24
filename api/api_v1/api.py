from fastapi import APIRouter

from api.api_v1.endpoints import users, drivers, teams, login

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(drivers.router, prefix="/drivers", tags=["drivers"])
api_router.include_router(teams.router, prefix="/teams", tags=["teams"])
